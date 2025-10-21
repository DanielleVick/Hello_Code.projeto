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

# ------------------- FASES -------------------
def passar_nivel():
    global nivel, xp, meta_xp
    if xp >= meta_xp:
        nivel += 1
        xp -= meta_xp
        meta_xp += 100
        print(f"Parabéns! Você subiu para o nível {nivel}!")
        print(f"Próximo nível em {meta_xp} XP.")

# ------------------ FASE 1 ----------------------
def fase_1():
  global nivel
  nivel = 1  
  if nivel_1():  
    nivel += 1
  if nivel_2(): 
    nivel += 1
  if nivel_3():  
    nivel += 1
  print("Você passou da fase 1, parabéns!")
  input("Pressione Enter para continuar")

def nivel_1():
    global xp
    while True:
        limpar_tela()
        print("\nBem-vindo(a) ao Nível 1: Cozinha do Caos!")
        print("""\n
Antes de fazer um bolo, precisamos seguir a ordem certa dos passos.
Em programação, fazemos a mesma coisa com os códigos.
Isso se chama lógica e sequência!""")
        print("\nEm uma receita, temos: 3 ovos, 2 xícaras de farinha, 1 xícara de açúcar e 1/2 xícara de leite.")
        print("Qual a ordem correta de passos para fazer um bolo?")
        print("""\n1- Pegar um recipiente
2- Colocar a forma no forno
3- Untar a forma
4- Adicionar os ovos
5- Ligar o forno
6- Adicionar os ingredientes líquidos
7- Colocar a massa na forma
8- Retirar do forno
9- Adicionar os ingredientes secos""")
        resposta = input("\nDigite a ordem correta dos passos, separados por vírgula: ").strip()

        if resposta == "1,9,4,6,3,7,5,2,8":
            print("\nParabéns! Você acertou!")
            xp += 20
            passar_nivel()
            historico.append("Desafio 1: Passou")
            input("\nPressione Enter para continuar")
            return True
        else:
            print("\nTente novamente!")
            historico.append("Desafio 1: Não passou")
            input("\nPressione Enter para tentar de novo")

def nivel_2():
    global xp
    while True:
        limpar_tela()
        print("\nBem-vindo(a) ao Nível 2: Mercado Desorganizado!")
        print("""\n
Tudo tem um lugar certo! Assim como no mercado, 
um programa precisa verificar se algo está certo ou errado. 
Essa checagem é parte importante da lógica.""")
        prateleiras = {
            "\nfrutas": ["maça", "banana", "biscoito", "laranja"],
            "verduras": ["alface", "tomate", "cenoura", "refrigerante"],
            "carnes": ["frango", "carne bovina", "peixe", "detergente"],
            "doces": ["chocolate", "bala", "sorvete", "arroz"],
            "produtos de limpeza": ["sabão", "desinfetante", "amaciante", "feijão"]
        }
        for categoria in prateleiras:
            print(f"{categoria.capitalize()}: {', '.join(prateleiras[categoria])}")

        resposta = input("\nDigite 1 item que está no lugar errado: ").strip().lower()
        itens_errados = "biscoito", "refrigerante", "detergente", "arroz", "feijão"

        if resposta in itens_errados:
            print("\nParabéns! Você acertou!")
            xp += 20
            passar_nivel()
            historico.append(f"Desafio 2: Acertou o item {resposta}")
            input("\nPressione Enter para continuar")
            return True
        else:
            print("\nTente novamente!")
            historico.append("Desafio 2: Não acertou")
            input("\nPressione Enter para tentar novamente")

def nivel_3():
    global xp
    while True:
        limpar_tela()
        print("\nBem-vindo(a) ao Nível 3: Cidade dos Erros!")
        print("""\n
Na cidade cheia de ruas, escolher o caminho certo é essencial. 
Em programação, usamos decisões para escolher que caminho seguir. 
É assim que o programa pensa!""")
        print("\nEscolha o caminho certo: A, B ou C.")
        print("A: Sequência lógica que organiza ideias e verifica erros.")
        print("B: Pule etapas, causando erros.")
        print("C: Repita ações infinitamente, sem fim.")
        resposta = input("\nQual caminho? (A, B ou C): ").strip().upper()

        if resposta == "A":
            print("\nParabéns! Você passou.")
            xp += 20
            passar_nivel()
            historico.append("Desafio 3: Passou")
            input("\nPressione Enter para continuar")
            return True
        else:
            print("\nCaminho errado! Tente novamente.")
            historico.append("Desafio 3: Não passou")
            input("\nPressione Enter para tentar de novo")