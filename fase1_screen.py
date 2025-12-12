# fase1_screen.py (COMPLETO E FINALIZADO)

import pygame
import os
from typing import Dict, Any, List, Optional, Tuple
from player import Jogador
from screens import InputBox, CINZENTO, VERDE_NEON, ROSA_NEON, AZUL_NEON, BRANCO, PRETO

# 🌟 CORREÇÃO DE CRASH: Bloco defensivo para dependências de áudio
try:
    from utils_audio import play_sound
except ImportError:
    def play_sound(name):
        pass

# ----------------------------------------------------
# DEFINIÇÕES LOCAIS E CONTEÚDO
# ----------------------------------------------------
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
PIXEL_FONT_PATH = os.path.join(ASSETS_DIR, "PressStart2P-Regular.ttf")

# Desafios de Nível 1 da Fase 1 (Ordem Lógica)
CHALLENGE_1 = {
    "id": 1,
    "titulo": "Nível 1: Cozinha do Caos!",
    "receita": "Receita: 3 ovos, farinha, açúcar e leite.",
    "instrucao_principal": "Digite a ordem correta como no exemplo (ex: 1,2,3...):",
    "instrucao_exemplo": "",
    "passos": [
        "1. Untar a forma", "2. Levar ao forno e esperar ficar pronto",
        "3. Pegar um recipiente", "4. Colocar a massa na forma",
        "5. Adicionar e misturar os ingredientes (ovos + secos + líquidos)",
        "6. Retirar do forno"
    ],
    "resposta": "3,5,1,4,2,6",
    "xp": 20
}
CHALLENGE_2 = {
    "id": 2,
    "titulo": "Nível 2: Mercado Desorganizado!",
    "receita": "Encontre o item que está na prateleira errada:",
    "instrucao_principal": "Digite o nome do item que está na prateleira errada:",
    "instrucao_exemplo": "",
    "prateleiras": {
        "frutas": ["maçã", "banana", "biscoito", "laranja"],
        "verduras": ["alface", "tomate", "cenoura", "refrigerante"],
        "carnes": ["frango", "carne bovina", "peixe", "detergente"],
    },
    "resposta": ["biscoito", "refrigerante", "detergente"],
    "xp": 20
}
CHALLENGE_3 = {
    "id": 3,
    "titulo": "Nível 3: Cidade dos Erros!",
    "receita": "Escolha o caminho certo para chegar ao destino sem erros:",
    "instrucao_principal": "Qual caminho? (A/B/C):",
    "instrucao_exemplo": "",
    "opcoes": [
        "A: Sequência lógica que organiza ideias e verifica erros.",
        "B: Pular etapas, causando erros.",
        "C: Repetir ações infinitamente, sem fim."
    ],
    "resposta": "A",
    "xp": 20
}

ALL_CHALLENGES = [CHALLENGE_1, CHALLENGE_2, CHALLENGE_3]

# ----------------------------------------------------
# CLASSE PRINCIPAL
# ----------------------------------------------------


class Fase1Screen:
    def __init__(self, largura: int, altura: int, jogador: Jogador, salvar_jogadores, jogadores_dict):
        self.largura = largura
        self.altura = altura
        self.jogador = jogador
        self.salvar_jogadores = salvar_jogadores
        self.jogadores_dict = jogadores_dict

        try:
            self.fonte_padrao = pygame.font.Font(PIXEL_FONT_PATH, 14)
            self.fonte_titulo = pygame.font.Font(PIXEL_FONT_PATH, 24)
        except Exception:
            self.fonte_padrao = pygame.font.Font(None, 24)
            self.fonte_titulo = pygame.font.Font(None, 32)

        # 1. Estado da Fase
        self.nivel_atual_idx = 0
        self.desafio_atual = ALL_CHALLENGES[self.nivel_atual_idx]
        self.mensagem = ""
        self.mensagem_cor = ROSA_NEON
        self.desafio_concluido_sucesso = False
        self.fase_concluida = False

        # 2. Fundo (Usando um cenário genérico)
        try:
            caminho_fundo = os.path.join(ASSETS_DIR, "cenario.png")
            self.fundo = pygame.image.load(caminho_fundo).convert_alpha()
            self.fundo = pygame.transform.scale(self.fundo, (largura, altura))
        except pygame.error:
            self.fundo = None

        # 3. Campo de Input
        w_input = 350
        x_center = largura // 2

        self.input_resposta = InputBox(
            x_center - w_input // 2, 440, w_input, 32, 'RESPOSTA AQUI...')
        self.input_resposta.color_inactive = AZUL_NEON
        self.input_resposta.color = AZUL_NEON

        # 4. Botões
        w_btn, h_btn = 150, 40
        x_center = largura // 2
        self.botao_submeter_rect = pygame.Rect(
            x_center - w_btn - 10, altura - 70, w_btn, h_btn)
        self.botao_proximo_rect = pygame.Rect(
            x_center + 10, altura - 70, w_btn, h_btn)

    def _avancar_nivel(self):
        """Prepara o estado para o próximo nível, adicionando XP e salvando o progresso."""

        # 🌟 CORREÇÃO 2: ADICIONA XP AQUI (PÓS-RECOMPENSA)
        self._adicionar_xp_e_salvar(self.desafio_atual["xp"])

        self.nivel_atual_idx += 1

        if self.nivel_atual_idx < len(ALL_CHALLENGES):
            self.desafio_atual = ALL_CHALLENGES[self.nivel_atual_idx]
            self.desafio_concluido_sucesso = False
            self.mensagem = f"Nível {self.desafio_atual['id']} desbloqueado!"
            self.input_resposta.text = ""
        else:
            self.fase_concluida = True
            self.jogador.fase = 2  # Libera a próxima fase
            self._salvar_progresso()

    def _processar_resposta(self, resposta_usuario: str):
        if self.desafio_concluido_sucesso:
            return

        resposta_usuario = resposta_usuario.replace(" ", "").upper()

        # Lógica de Checagem Unificada (Corrigida a checagem de nível 2)
        if self.desafio_atual["id"] == 1:
            correto = (resposta_usuario == self.desafio_atual["resposta"])
        elif self.desafio_atual["id"] == 2:
            correto = (resposta_usuario in [r.upper()
                       for r in self.desafio_atual["resposta"]])
        elif self.desafio_atual["id"] == 3:
            correto = (resposta_usuario == self.desafio_atual["resposta"])
        else:
            correto = False

        if correto:
            self.mensagem = "Parabéns! Desafio concluído!"
            play_sound("point")
            self.mensagem_cor = VERDE_NEON
            self.desafio_concluido_sucesso = True

            # 🌟 CORREÇÃO 1: RETORNA O SINAL DE RECOMPENSA (Não adiciona XP aqui)
            return ("REWARD", (1, self.nivel_atual_idx))
        else:
            play_sound("error")
            self.mensagem = "Resposta incorreta! Tente novamente."
            self.mensagem_cor = ROSA_NEON

        return None

    def _adicionar_xp_e_salvar(self, xp_ganho):
        self.jogador.xp += xp_ganho
        self.jogadores_dict[self.jogador.nome] = self.jogador.to_dict()
        self.salvar_jogadores(self.jogadores_dict)

    def _salvar_progresso(self):
        self.jogadores_dict[self.jogador.nome] = self.jogador.to_dict()
        self.salvar_jogadores(self.jogadores_dict)

    def lidar_com_eventos(self, event) -> Optional[Tuple[str, Optional[Jogador]]]:
        res = self.input_resposta.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if self.botao_submeter_rect.collidepoint(mouse_pos) and not self.desafio_concluido_sucesso:
                result = self._processar_resposta(
                    self.input_resposta.get_text())
                if result:
                    return result

            elif self.botao_proximo_rect.collidepoint(mouse_pos):
                if self.desafio_concluido_sucesso:
                    if self.fase_concluida:
                        return ("MENU_PRINCIPAL", self.jogador)
                    else:
                        # 🌟 Envia o sinal REWARD, que depois chamará _avancar_nivel
                        return ("REWARD", (1, self.nivel_atual_idx))
                else:
                    return ("MENU_PRINCIPAL", self.jogador)

        if res is not None and not self.desafio_concluido_sucesso:
            result = self._processar_resposta(res)
            if result:
                return result

        return None

    def atualizar(self):
        pass

    def desenhar(self, tela):
        # 1. Desenhar o Fundo
        if self.fundo:
            tela.blit(self.fundo, (0, 0))
        else:
            tela.fill(PRETO)

        # 2. Título do Desafio
        texto_titulo = self.fonte_titulo.render(
            self.desafio_atual["titulo"], True, ROSA_NEON)
        tela.blit(texto_titulo, (self.largura // 2 -
                  texto_titulo.get_width() // 2, 30))

        # 3. Desenhar Instruções e Passos
        self.desenhar_desafio_especifico(tela)

        # 4. Input e Feedback

        # VISIBILIDADE FIX: Desenha um retângulo preenchido por trás do input
        input_bg_rect = self.input_resposta.rect.inflate(10, 10)
        pygame.draw.rect(tela, (30, 30, 30), input_bg_rect, 0, 5)

        # 4A. Desenhar a Instrução do Desafio logo acima do input
        texto_instrucao_input = self.fonte_padrao.render(
            self.desafio_atual.get("instrucao_principal", ""), True, AZUL_NEON)
        x_centered_inst_main = self.largura // 2 - \
            texto_instrucao_input.get_width() // 2
        tela.blit(texto_instrucao_input, (x_centered_inst_main, 380))

        # 4B. Desenhar o Exemplo de Formato logo abaixo
        texto_exemplo_input = self.fonte_padrao.render(
            self.desafio_atual.get("instrucao_exemplo", ""), True, BRANCO)
        x_centered_inst_ex = self.largura // 2 - texto_exemplo_input.get_width() // 2
        tela.blit(texto_exemplo_input, (x_centered_inst_ex, 410))

        self.input_resposta.draw(tela)

        if self.mensagem:
            texto_msg = self.fonte_padrao.render(
                self.mensagem, True, self.mensagem_cor)
            tela.blit(texto_msg, (self.largura // 2 -
                      texto_msg.get_width() // 2, 500))

        # 5. Botões
        cor_submeter = VERDE_NEON if not self.desafio_concluido_sucesso else CINZENTO

        pygame.draw.rect(tela, cor_submeter, self.botao_submeter_rect)
        texto_submeter = self.fonte_padrao.render("SUBMETER", True, PRETO)
        tela.blit(texto_submeter, (self.botao_submeter_rect.x +
                  10, self.botao_submeter_rect.y + 10))

        # Botão PRÓXIMO / VOLTAR
        if self.desafio_concluido_sucesso:
            label_proximo = "PRÓXIMO" if not self.fase_concluida else "MENU"
            cor_proximo = AZUL_NEON
        else:
            label_proximo = "VOLTAR"
            cor_proximo = ROSA_NEON

        pygame.draw.rect(tela, cor_proximo, self.botao_proximo_rect)
        texto_proximo = self.fonte_padrao.render(label_proximo, True, PRETO)
        tela.blit(texto_proximo, (self.botao_proximo_rect.x +
                  10, self.botao_proximo_rect.y + 10))

    def desenhar_desafio_especifico(self, tela):
        """Desenha o conteúdo visual específico para o Nível atual."""
        y_start = 80
        gap = 20
        # X_POS CORRIGIDO: Centraliza a lista, dando espaço na margem
        x_list_start = self.largura // 2 - 220

        # Instrução Principal da Receita (acima dos passos)
        texto_receita = self.fonte_padrao.render(
            self.desafio_atual.get("receita", ""), True, AZUL_NEON)

        # Centraliza a instrução principal
        x_centered_receita = self.largura // 2 - texto_receita.get_width() // 2
        tela.blit(texto_receita, (x_centered_receita, y_start + 40))

        # Desenho Específico por Nível
        if self.desafio_atual["id"] == 1:
            # Nível 1: Cozinha do Caos (Lista de Passos)

            # Desenha Instrução de Ordem (CENTRALIZADA)
            texto_instrucao = self.fonte_padrao.render(
                self.desafio_atual.get("instrucao_principal", ""), True, BRANCO)
            x_centered_inst = self.largura // 2 - texto_instrucao.get_width() // 2
            tela.blit(texto_instrucao, (x_centered_inst, y_start + 80))

            # Desenhar Passos Numerados (USANDO x_list_start)
            y_current = y_start + 110
            for i, passo in enumerate(self.desafio_atual["passos"]):
                if i == 4:  # Passo 5

                    # QUEBRA DE LINHA MANUAL PARA O PASSO 5
                    line1 = "5. Adicionar e misturar os ingredientes"
                    line2 = "(ovos + secos + líquidos)"

                    texto_line1 = self.fonte_padrao.render(line1, True, BRANCO)
                    tela.blit(texto_line1, (x_list_start, y_current))
                    y_current += gap  # Avança a linha

                    texto_line2 = self.fonte_padrao.render(line2, True, BRANCO)
                    # Adiciona um pequeno recuo para a segunda linha
                    tela.blit(texto_line2, (x_list_start + 20, y_current))
                    y_current += gap  # Avança a linha

                else:
                    # Desenhar passos normais (1, 2, 3, 4, 6)
                    texto_passo = self.fonte_padrao.render(passo, True, BRANCO)
                    tela.blit(texto_passo, (x_list_start, y_current))
                    y_current += gap

            self.input_resposta.label_text = 'DIGITE A ORDEM (3,5,1...)'
        elif self.desafio_atual["id"] == 2:
            # Nível 2: Mercado Desorganizado (Lista de Prateleiras)
            # Centraliza a instrução principal (já feito antes, repetimos para clareza)
            texto_instrucao = self.fonte_padrao.render(
                self.desafio_atual.get("instrucao_principal", ""), True, BRANCO)
            x_centered_inst = self.largura // 2 - texto_instrucao.get_width() // 2
            tela.blit(texto_instrucao, (x_centered_inst, y_start + 80))

            # Espaçamento inicial
            y_current = y_start + 110
            gap = 22  # espaçamento entre linhas

            # Função local para quebra de texto respeitando largura máxima
            def wrap_text_to_lines(font, text, max_width):
                """Retorna lista de linhas que caibam em max_width usando quebras simples."""
                import textwrap
                # tentativa de quebrar por palavras; textwrap usa chars, então ajustamos
                # dividimos em palavras e iterativamente montamos linhas
                words = text.split()
                lines = []
                current = ""
                for w in words:
                    test = (current + " " + w).strip()
                    if font.size(test)[0] <= max_width:
                        current = test
                    else:
                        if current:
                            lines.append(current)
                        current = w
                if current:
                    lines.append(current)
                return lines

            # Largura máxima permitida para o texto da prateleira (80% da tela ou mínimo 400)
            max_text_width = max(400, int(self.largura * 0.8))

            # Desenha cada categoria com itens, centralizando cada linha
            for categoria, itens in self.desafio_atual["prateleiras"].items():
                # monta a string: "CATEGORIA: item1, item2, item3"
                linha = f"{categoria.upper()}: {', '.join(itens)}"

                # quebra em linhas se necessário
                linhas = wrap_text_to_lines(
                    self.fonte_padrao, linha, max_text_width)

                # desenha cada sublinha centralizada
                for sublinha in linhas:
                    surf = self.fonte_padrao.render(sublinha, True, BRANCO)
                    rect = surf.get_rect(center=(self.largura // 2, y_current))
                    tela.blit(surf, rect)
                    y_current += gap

                # adiciona um pequeno espaço extra entre categorias
                y_current += 6

            # Atualiza label do input (mantendo o estilo anterior)
            self.input_resposta.label_text = 'ITEM ERRADO...'

        elif self.desafio_atual["id"] == 3:
            # Nível 3: Cidade dos Erros (Opções A, B, C)

            # Desenha Instrução de Ordem (CENTRALIZADA)
            texto_instrucao = self.fonte_padrao.render(
                self.desafio_atual.get("instrucao_principal", ""), True, BRANCO)
            x_centered_inst = self.largura // 2 - texto_instrucao.get_width() // 2
            tela.blit(texto_instrucao, (x_centered_inst, y_start + 80))

            y_current = y_start + 110  # Posição inicial da lista de opções
            x_list_start_wide = self.largura // 2 - 250  # Margem ampla

            for i, opcao in enumerate(self.desafio_atual["opcoes"]):
                if i == 0:  # OPÇÃO A: Aplicar quebra de linha manual
                    line1 = "A: Sequência lógica que organiza ideias"
                    line2 = "   e verifica erros."

                    texto_line1 = self.fonte_padrao.render(line1, True, BRANCO)
                    tela.blit(texto_line1, (x_list_start_wide, y_current))
                    y_current += 30

                    texto_line2 = self.fonte_padrao.render(line2, True, BRANCO)
                    tela.blit(texto_line2, (x_list_start_wide, y_current))
                    y_current += 30
                else:
                    texto_op = self.fonte_padrao.render(opcao, True, BRANCO)
                    tela.blit(texto_op, (x_list_start_wide, y_current))
                    y_current += 30

            self.input_resposta.label_text = 'RESPOSTA (A, B ou C)'
