# ------------------- IMPORTS -------------------
import re
from datetime import datetime
# ------------------- VARIÁVEIS GLOBAIS -------------------
jogadores = {}
logado = False

# ----------------- LIMPAR TELA -----------------
from utils import limpar_tela, salvar_jogadores, carregar_jogadores

# -------------------- COLORIR TEXTO ------------------------
from utils import cor
 # ------------------- CADASTRO -------------------
def validar_data_nascimento(data):
    try:
        datetime.strptime(data, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def validar_senha(senha):
    return 6 <= len(senha) <= 10 and re.search(r"[A-Z]", senha) and re.search(r"[^A-Za-z0-9]", senha)

def cadastro():
    limpar_tela()
    print(cor("===== CADASTRO =====", "roxo"))
    while True:
        nome = input("Nome do jogador: ").strip().upper()
        if nome in jogadores:
            print(cor("Já existe um jogador com esse nome. Tente outro.", "vermelho"))
            continue

        while True:
            data_nascimento = input("Data de nascimento (DD/MM/AAAA): ").strip()
            if validar_data_nascimento(data_nascimento):
                break
            print(cor("Data inválida! Use o formato DD/MM/AAAA.", "vermelho"))

        while True:
            senha = input("Senha: ").strip()
            if validar_senha(senha):
                break
            print(cor("Senha inválida! Deve ter de 6 a 10 caracteres, com 1 maiúscula e 1 caractere especial.", "vermelho"))

        # Inicializando nível e fase
        jogadores[nome] = {
            "data_nascimento": data_nascimento,
            "senha": senha,
            "nivel": 1,
            "fase": 1
        }
        print(cor("\nJogador cadastrado com sucesso!", "verde"))
        salvar_jogadores()
        input("Pressione Enter para continuar...")
        break

#----------------------- LOGIN -------------------------------
def verificar_usuario(nome, senha):
    return nome in jogadores and jogadores[nome]["senha"] == senha

def login():
    global logado, jogadores
    jogadores = carregar_jogadores() 
    limpar_tela()
    print(cor("===== LOGIN =====", "roxo"))
    usuario = input("Digite seu usuário: ").strip().upper()  
    senha = input("Digite sua senha: ").strip()

    if verificar_usuario(usuario, senha):
        print(cor("Login bem-sucedido!", "verde"))
        logado = True
        input("Pressione Enter para continuar...")
        from menu import menu_principal
        menu_principal()
    else:
        print(cor("Usuário ou senha incorretos.", "vermelho"))
        input("Pressione Enter para tentar novamente...")


# ------------------- ATUALIZAÇÃO -------------------
def atualizar_jogador():
    limpar_tela()
    nome = input("\nNome do jogador para atualizar: ").strip().upper()
    if nome not in jogadores:
        print(cor("Jogador não encontrado.", "vermelho"))
        return

    while True:
        print(cor("\nO que deseja atualizar?", "rosa"))
        print("1. Data de nascimento")
        print("2. Senha")
        print("3. Voltar")
        opcao = input(cor("Escolha: ", "azul")).strip()

        if opcao == "1":
            while True:
                nova_data = input("Nova data (DD/MM/AAAA): ").strip()
                if validar_data_nascimento(nova_data):
                    jogadores[nome]["data_nascimento"] = nova_data
                    print(cor("Data atualizada com sucesso!", "verde"))
                    break
                print(cor("Data inválida! Tente novamente.", "vermelho"))
        elif opcao == "2":
            while True:
                nova_senha = input("Nova senha: ").strip()
                if validar_senha(nova_senha):
                    jogadores[nome]["senha"] = nova_senha
                    print(cor("Senha atualizada com sucesso!", "verde"))
                    break
                print(cor("Senha inválida! Tente novamente.", "vermelho"))
        elif opcao == "3":
            break
        else:
            print(cor("Opção inválida.", "vermelho"))