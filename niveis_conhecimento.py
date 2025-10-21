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


#------------------------ NÍVEL DE CONHECIMENTO --------------------------
def teste_nivel():
    print("===== TESTE DE NÍVEL DE CONHECIMENTO =====\n")
    score = 0

    print("1) O que é uma variável em programação?")
    print("a) Um número fixo")
    print("b) Um espaço que armazena dados")
    print("c) Um tipo de loop")
    resposta = input("Escolha a letra correta: ").strip().lower()

    if resposta == "b":
        score += 1

    print("\n2) Qual operador é usado para multiplicação?")
    print("a) +")
    print("b) -")
    print("c) *")
    resposta = input("Escolha a letra correta: ").strip().lower()
    if resposta == "c":
        score += 1

    print("\n3) O que significa 'if' em Python?")
    print("a) Estrutura de repetição")
    print("b) Estrutura condicional")
    print("c) Declaração de função")
    resposta = input("Escolha a letra correta: ").strip().lower()
    if resposta == "b":
        score += 1

  # AVALIAÇÃO FINAL
    print("\n===== RESULTADO =====")
    if score == 3:
        print("Nível: Avançado")
    elif score == 2:
        print("Nível: Intermediário")
    else:
        print("Nível: Iniciante")
    
    input("Pressione Enter para voltar ao menu...")