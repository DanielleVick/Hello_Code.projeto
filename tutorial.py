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

#-------------------- TUTORIAL ADAPTADO DE ACORDO COM A FASE ------------------------
def mostrar_texto_pausado(texto):
    """Mostra um texto longo e espera o jogador apertar Enter para continuar."""
    print("\n" + texto + "\n")
    input("Pressione Enter para voltar às instruções...")

def tutorial():
    print("=========TUTORIAL DO JOGO=========")
    print("=========Fase 01: Lógica de programação==========")
    print("1 - Nível 01: Organizar passos em ordem lógica (como uma receita).")
    print("2 - Nível 02: Cartas viradas com conceitos básicos ou símbolos.")
    print("3 - Nível 03: Seguir uma sequência lógica de raciocínio, verificando cada passo para evitar falhas.")
    print("=========Fase 02: Lógica de programação==========")
    print("4 - Nível 01: Combine os frascos corretamente para criar a fórmula usando operações matemáticas.")
    print("5 - Nível 02: Use operadores matemáticos para combinar os valores dos baús e descobrir o total de moedas da ilha.")
    print("6 - Nível 03: Aprenda a usar funções criando blocos de código que recebem valores e retornam resultados, como misturar cristais ou poções..")
    print("7 - Sair")
    input("Pressione Enter para continuar...")

    limpar_tela()

    while True:
        escolha = input("Escolha uma opção (1-7): ").strip()

        if escolha == "1":
            texto = (
                "Para resolver este desafio, você precisa organizar os passos na ordem correta.\n"
                "Assim como em uma receita, cada ação deve acontecer na sequência certa.\n"
                "Leia os passos e numere do primeiro até o último.\n"
                "Errar a ordem significa que o resultado final não funciona!"
            )
            mostrar_texto_pausado(texto)
            limpar_tela()
        elif escolha == "2":
            texto = (
                "Este é um jogo de lógica e memória!\n"
                "As cartas estão viradas e cada uma tem um par.\n"
                "Escolha um número para revelar a carta e tente lembrar onde está o par correspondente.\n"
                "Seu objetivo é formar todos os pares usando a menor quantidade de tentativas.\n"
                "Pense bem… lógica também é lembrar e conectar informações!"
            )
            mostrar_texto_pausado(texto)
            limpar_tela()
        elif escolha == "3":
            texto = (
                "Na Cidade dos Erros, você se depara com três caminhos diferentes: A, B e C.\n"
                "O objetivo é escolher o caminho correto para chegar ao destino sem cometer erros.\n"
                "O caminho A representa uma sequência lógica, guiando você passo a passo.\n"
                "O caminho B pula etapas, causando erros e dificultando a conclusão.\n"
                "O caminho C repete ações infinitamente, prendendo você em um ciclo sem fim.\n"
            )
            mostrar_texto_pausado(texto)
            limpar_tela()
        elif escolha == "4":
            texto = (
                "No Laboratório Maluco, você encontra frascos com valores diferentes.\n"
                "Seu desafio é combinar dois frascos usando operações matemáticas para criar a fórmula correta.\n"
                "Escolha entre somar ou multiplicar os valores dos frascos para obter o resultado desejado.\n"
                "Preste atenção às operações e aos valores para completar o desafio com sucesso!"
            )
            mostrar_texto_pausado(texto)
            limpar_tela()
        elif escolha == "5":
            texto = (
                "Na Ilha dos Tesouros, você encontra baús contendo moedas.\n"
                "Seu desafio é usar operadores matemáticos para combinar os valores dos baús e descobrir o total de moedas.\n"
                "Escolha entre somar, multiplicar ou calcular o resto da divisão para obter o resultado correto.\n"
                "Use suas habilidades matemáticas para desvendar os segredos da ilha!"
            )
            mostrar_texto_pausado(texto)
            limpar_tela()
        elif escolha == "6":
            texto = (
                "No Salão Mágico do Guardião, você aprende a usar funções.\n"
                "Funções são blocos de código que recebem valores, realizam cálculos e retornam resultados.\n"
                "Por exemplo, uma função pode somar dois números e retornar o resultado.\n"
                "Use suas habilidades para criar funções que misturam cristais ou poções, obtendo resultados mágicos!"
            )
            mostrar_texto_pausado(texto)
            limpar_tela()
        elif escolha == "7":
            print("\n Voltando ao menu principal...\n")
            break
        else:
            print("\n Opção inválida! Tente novamente. \n")