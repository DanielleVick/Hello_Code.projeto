# ------------------- IMPORTS -------------------
import re
import sys
import time
import json
import os
from datetime import datetime

# ------------------- JSON --------------------------------
def carregar_jogadores():
    global jogadores
    if os.path.exists("jogadores.json"):
        with open("jogadores.json", "r") as arquivo:
            try:
                jogadores = json.load(arquivo)
                print("Carregando dados salvos...")
                time.sleep(2.0)
            except json.JSONDecodeError:
                print("Arquivo corrompido. Iniciando vazio...")
                jogadores = {}
    else:
        print("Arquivo não encontrado. Iniciando vazio...")
        time.sleep(2.0)
        jogadores = {}

def salvar_jogadores():
    with open("jogadores.json", "w") as arquivo:
        json.dump(jogadores, arquivo, indent=4)

# ------------------- VARIÁVEIS GLOBAIS -------------------
jogadores = {}
historico = []
xp = 0
nivel = 1
meta_xp = 100
logado = False

# ------------------- FUNÇÕES DE UTILIDADE -------------------
def limpar_tela():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

        # ------------------- INÍCIO -------------------
def iniciar_jogo():
    limpar_tela()

    # ------------------- CADASTRO -------------------
def validar_data_nascimento(data):
    try:
        datetime.strptime(data, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def validar_senha(senha):
    import re
    return 6 <= len(senha) <= 10 and re.search(r"[A-Z]", senha) and re.search(r"[^A-Za-z0-9]", senha)

def cadastro():
    limpar_tela()
    print("===== CADASTRO =====")
    while True:
        nome = input("Nome do jogador: ").strip().upper()
        if nome in jogadores:
            print("Já existe um jogador com esse nome. Tente outro.")
            continue

        while True:
            data_nascimento = input("Data de nascimento (DD/MM/AAAA): ").strip()
            if validar_data_nascimento(data_nascimento):
                break
            print("Data inválida! Use o formato DD/MM/AAAA.")

        while True:
            senha = input("Senha: ").strip()
            if validar_senha(senha):
                break
            print("Senha inválida! Deve ter de 6 a 10 caracteres, com 1 maiúscula e 1 caractere especial.")

        # Inicializando nível e fase
        jogadores[nome] = {
            "data_nascimento": data_nascimento,
            "senha": senha,
            "nivel": 1,
            "fase": 1
        }
        print("\nJogador cadastrado com sucesso!")
        salvar_jogadores()
        input("Pressione Enter para continuar...")
        break

#----------------------- LOGIN -------------------------------
def verificar_usuario(nome, senha):
    return nome in jogadores and jogadores[nome]["senha"] == senha

def login():
    global logado
    limpar_tela()
    print("===== LOGIN =====")
    usuario = input("Digite seu usuário: ").strip()
    senha = input("Digite sua senha: ").strip()

    if verificar_usuario(usuario, senha):
        print("Login bem-sucedido!")
        logado = True
        input("Pressione Enter para continuar...")
    else:
        print("Usuário ou senha incorretos.")
        input("Pressione Enter para tentar novamente...")

# ------------------- ATUALIZAÇÃO -------------------
def atualizar_jogador():
    limpar_tela()
    nome = input("\nNome do jogador para atualizar: ").strip().upper()
    if nome not in jogadores:
        print("Jogador não encontrado.")
        return

    while True:
        print("\nO que deseja atualizar?")
        print("1. Data de nascimento")
        print("2. Senha")
        print("3. Voltar")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            while True:
                nova_data = input("Nova data (DD/MM/AAAA): ").strip()
                if validar_data_nascimento(nova_data):
                    jogadores[nome]["data_nascimento"] = nova_data
                    print("Data atualizada com sucesso!")
                    break
                print("Data inválida! Tente novamente.")
        elif opcao == "2":
            while True:
                nova_senha = input("Nova senha: ").strip()
                if validar_senha(nova_senha):
                    jogadores[nome]["senha"] = nova_senha
                    print("Senha atualizada com sucesso!")
                    break
                print("Senha inválida! Tente novamente.")
        elif opcao == "3":
            break
        else:
            print("Opção inválida.")