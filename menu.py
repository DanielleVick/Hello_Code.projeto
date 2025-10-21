# ------------------- IMPORTS -------------------
import re
import sys
import time
import json
import os
from datetime import datetime

from core import tutorial
from core.fase1 import fase_1
from core.fase2 import fase_2
from core.main import teste_nivel

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
meta_xp = 60
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

# ------------------- MENU INICIAL -------------------
def menu_inicial():
    global logado
    limpar_tela()
    print("Bem-vindo(a) ao Hello Code!")
    print("\n===== MENU INICIAL =====")
    print("1. Cadastro")
    print("2. Login")
    print("3. Sair")

# ------------------- MENU PRINCIPAL -------------------
def menu_principal():
    fase2_liberada = False
    while True:
        limpar_tela()
        print("\n===== MENU PRINCIPAL =====")
        print("1. Selecionar o nível de conhecimento")
        print("2. Seguir para tutorial adaptado")
        print("3. Ir para Fase 1")
        print(f"4. Ir para Fase 2 {'(Bloqueada)' if not fase2_liberada else ''}")
        print("5. Sair")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            teste_nivel()
        elif opcao == "2":
            tutorial()
        elif opcao == "3":
            fase_1()
            fase2_liberada = True
        elif opcao == "4":
            if not fase2_liberada:
                print("\nA fase 2 ainda não está liberada! Complete a fase 1 primeiro.")
            else:
                fase_2()
        elif opcao == "5":
            print("Saindo do jogo...")
            sys.exit()
        else:
            print("Opção inválida. Digite novamente.")