# auth.py (COMPLETO)
import re
from datetime import datetime
from typing import Dict, Optional

from player import Jogador 


def atualizar_jogador(jogadores: Dict[str, dict], nome: str, novos_dados: dict,
                      salvar_jogadores=None) -> None:
    nome_up = nome.strip().upper()
    if nome_up not in jogadores:
        raise KeyError(f"Jogador '{nome_up}' não existe.")
    jogadores[nome_up].update(novos_dados)
    if salvar_jogadores:
        salvar_jogadores(jogadores)


class Auth:
    def __init__(self, limpar_tela, cor, jogadores: Dict[str, dict], salvar_jogadores):
        """
        limpar_tela: função que limpa a tela (usado na CLI)
        cor: função cor(texto, nome_cor) (usado na CLI)
        jogadores: referência ao dict de jogadores (nome -> dados)
        salvar_jogadores: função salvar_jogadores(jogadores: dict)
        """
        self.limpar_tela = limpar_tela
        self.cor = cor
        self.jogadores = jogadores
        self.salvar_jogadores = salvar_jogadores
        self.jogador_atual = None

    @staticmethod
    def validar_data_nascimento(data: str) -> bool:
        try:
            datetime.strptime(data, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    @staticmethod
    def validar_senha(senha: str) -> bool:
        # 6-10 chars, ao menos 1 maiúscula e 1 caractere especial (não alfanumérico)
        if not (6 <= len(senha) <= 10):
            return False
        if not re.search(r"[A-Z]", senha):
            return False
        if not re.search(r"[^A-Za-z0-9]", senha):
            return False
        return True

    # ==========================================================
    # 🌟 NOVOS MÉTODOS PARA INTERFACE GRÁFICA (GUI)
    # ==========================================================

    def cadastro_gui(self, nome: str, senha: str, data_nascimento: str) -> Optional[Jogador]:
        """ Tenta cadastrar o usuário. Chamado pela GUI. """
        nome_up = nome.strip().upper()
        
        # Validação básica de nome (assumindo que as validações complexas estão na GUI)
        if not nome_up or nome_up in self.jogadores:
            return None 

        if not self.validar_data_nascimento(data_nascimento):
            return None 

        if not self.validar_senha(senha):
            return None

        novo_jogador = Jogador(nome_up, data_nascimento,
                               senha, nivel=1, fase=1, xp=0)
        self.jogadores[nome_up] = novo_jogador.to_dict()
        self.salvar_jogadores(self.jogadores)
        return novo_jogador

    def login_gui(self, usuario: str, senha: str) -> Optional[Jogador]:
        """ Tenta fazer login. Chamado pela GUI. """
        usuario_up = usuario.strip().upper()

        if usuario_up not in self.jogadores or self.jogadores[usuario_up].get("senha") != senha:
            return None

        # Carrega o objeto Jogador (lógica de login robusta mantida)
        dados = self.jogadores[usuario_up]
        ctor = getattr(Jogador, "from_dict", None)
        
        if ctor is None:
            jogador_obj = Jogador(usuario_up, dados.get("data_nascimento"), dados.get("senha"),
                                  dados.get("nivel", 1), dados.get("fase", 1), dados.get("xp", 0))
        else:
            try:
                jogador_obj = Jogador.from_dict(usuario_up, dados)
            except TypeError:
                jogador_obj = Jogador.from_dict(dados)

        self.jogador_atual = jogador_obj
        return jogador_obj


    # ==========================================================
    # 🌟 MÉTODOS ORIGINAIS (CLI) - Mantidos por compatibilidade
    # ==========================================================

    def cadastro(self) -> Optional[Jogador]:
        self.limpar_tela()
        print(self.cor("===== CADASTRO =====", "roxo"))

        while True:
            nome = input("Nome do jogador: ").strip().upper()
            if not nome:
                print(self.cor("Nome vazio. Tente novamente.", "vermelho"))
                continue

            if nome in self.jogadores:
                print(
                    self.cor("Já existe um jogador com esse nome. Tente outro.", "vermelho"))
                continue

            while True:
                data_nascimento = input(
                    "Data de nascimento (DD/MM/AAAA): ").strip()
                if self.validar_data_nascimento(data_nascimento):
                    break
                print(self.cor("Data inválida! Use o formato DD/MM/AAAA.", "vermelho"))

            while True:
                senha = input("Senha: ").strip()
                if self.validar_senha(senha):
                    break
                print(self.cor(
                    "Senha inválida! Deve ter de 6 a 10 caracteres, com 1 maiúscula e 1 caractere especial.",
                    "vermelho"
                ))

            novo_jogador = Jogador(nome, data_nascimento,
                                   senha, nivel=1, fase=1, xp=0)
            self.jogadores[nome] = novo_jogador.to_dict()
            self.salvar_jogadores(self.jogadores)

            print(self.cor("\nJogador cadastrado com sucesso!", "verde"))
            input("Pressione Enter para continuar...")
            return novo_jogador

    def verificar_usuario(self, nome: str, senha: str) -> bool:
        nome_up = nome.strip().upper()
        return nome_up in self.jogadores and self.jogadores[nome_up].get("senha") == senha

    def login(self) -> Optional[Jogador]:
        """ Faz login interativo (CLI). Retorna Jogador se sucesso, None caso contrário. """
        self.limpar_tela()
        print(self.cor("===== LOGIN =====", "roxo"))

        usuario = input("Digite seu usuário: ").strip().upper()
        senha = input("Digite sua senha: ").strip()

        if usuario not in self.jogadores or self.jogadores[usuario].get("senha") != senha:
            print(self.cor("Usuário ou senha incorretos.", "vermelho"))
            input("Pressione Enter para tentar novamente...")
            return None

        # Carrega o objeto Jogador
        dados = self.jogadores[usuario]

        ctor = getattr(Jogador, "from_dict", None)
        if ctor is None:
            jogador_obj = Jogador(usuario,
                                  dados.get("data_nascimento"),
                                  dados.get("senha"),
                                  dados.get("nivel", 1),
                                  dados.get("fase", 1),
                                  dados.get("xp", 0))
        else:
            try:
                jogador_obj = Jogador.from_dict(usuario, dados)
            except TypeError:
                jogador_obj = Jogador.from_dict(dados)

        self.jogador_atual = jogador_obj
        print(self.cor("Login bem-sucedido!", "verde"))
        input("Pressione Enter para continuar...")
        return jogador_obj

    def atualizar(self, nome: str, novos_dados: dict) -> None:
        nome_up = nome.strip().upper()
        if nome_up not in self.jogadores:
            raise KeyError(f"Jogador '{nome_up}' não encontrado.")
        self.jogadores[nome_up].update(novos_dados)
        self.salvar_jogadores(self.jogadores)

    def carregar_jogador_obj(self, nome: str) -> Optional[Jogador]:
        nome_up = nome.strip().upper()
        if nome_up not in self.jogadores:
            return None
        return Jogador.from_dict(nome_up, self.jogadores[nome_up])