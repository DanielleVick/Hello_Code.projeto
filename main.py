# ------------------- BIBLIOTECAS UTILIZADAS -------------------
import re
import sys
import time
import json
import os
from colorama import Fore, Style
from datetime import datetime
     
# ------------------- IMPORTAÇÃO DE MÓDULOS -------------------
from utils import carregar_jogadores, salvar_jogadores, iniciar_jogo, limpar_tela, cor
from tutorial import tutorial, mostrar_texto_pausado
from niveis_conhecimento import teste_nivel
from fase1 import passar_nivel, fase_1, nivel_1, nivel_2, nivel_3
from fase2 import passar_nivel, fase_2, nivel_1_fase2, nivel_2_fase2, nivel_3_fase2
from auth import validar_data_nascimento, validar_senha, cadastro, verificar_usuario, login, atualizar_jogador 
from menu import menu_inicial, menu, menu_principal

# ------------------- VARIÁVEIS GLOBAIS -------------------
jogadores = {}
historico = []
xp = 0
nivel = 1
meta_xp = 60
logado = False

# ------------------- EXECUÇÃO PRINCIPAL -------------------
iniciar_jogo()
carregar_jogadores()  

while True:
    menu_inicial()
    escolha = input(cor("Escolha uma opção: ", "azul")).strip()
    if escolha == "1":
        cadastro()       
        iniciar_jogo()
        break  
    elif escolha == "2":
        login()
        if logado: 
            menu_principal()  
    elif escolha == "3":
        print(cor("Saindo do jogo...", "azul"))
        sys.exit()
    else:
        print(cor("Opção inválida. Tente novamente.", "vermelho"))

# Menu de jogadores 
menu()  

