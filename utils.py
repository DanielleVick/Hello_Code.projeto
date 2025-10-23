# ------------------- IMPORTS -------------------
import time
import os
import json
from colorama import Fore, Style, init
# ------------------- JSON --------------------------------
def carregar_jogadores():
    global jogadores
    if os.path.exists("jogadores.json"):
        with open("jogadores.json", "r") as arquivo:
            try:
                jogadores = json.load(arquivo)
                print(cor("Carregando dados salvos...", "verde"))
                time.sleep(2.0)
            except json.JSONDecodeError:
                print(cor("Arquivo corrompido. Iniciando vazio...", "vermelho"))
                jogadores = {}
    else:
        print(cor("Arquivo não encontrado. Iniciando vazio...", "vermelho"))
        time.sleep(2.0)
        jogadores = {}

def salvar_jogadores():
    with open("jogadores.json", "w") as arquivo:
        json.dump(jogadores, arquivo, indent=4)
        
# ------------------- FUNÇÃO DE LIMPAR A TELA -------------------

def limpar_tela():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# ------------------- Iniciar jogo -------------------
def iniciar_jogo():
    print(cor("Iniciando o jogo...", "azul"))
    time.sleep(2.0)
    limpar_tela()

# ------------------- COLORAMA ----------------------
init(autoreset=True)

def cor(texto, cor_texto):
    match cor_texto.lower():
        case "rosa": 
            cor_texto = Fore.LIGHTMAGENTA_EX
        case "roxo":
            cor_texto = Fore.MAGENTA
        case "verde":
            cor_texto = Fore.GREEN
        case "vermelho":
            cor_texto = Fore.RED
        case "azul":
            cor_texto = Fore.BLUE
        case _: 
            cor_texto = Fore.RESET
    return f"{cor_texto}{texto}{Style.RESET_ALL}"
            
