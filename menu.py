# ------------------- IMPORTS -------------------
import sys
import time
# ------------------- VARIÁVEIS GLOBAIS -------------------
logado = False
# ----------------- FUNÇÕES -----------------
from utils import limpar_tela
from auth import atualizar_jogador
from niveis_conhecimento import teste_nivel
from tutorial import tutorial 
from fase1 import fase_1
from fase2 import fase_2

# -------------------- COLORIR TEXTO ------------------------
from utils import cor

# ------------------- MENU INICIAL -------------------
def menu_inicial():
    global logado
    limpar_tela()
    print(cor("Bem-vindo(a) ao Hello Code!", "roxo"))
    print(cor("\n===== MENU INICIAL =====", "rosa"))
    print("1. Cadastro")
    print("2. Login")
    print("3. Sair")

# ------------------- MENU PRINCIPAL -------------------
def menu_principal():
    fase2_liberada = False
    while True:
        limpar_tela()
        print(cor("\n===== MENU PRINCIPAL =====", "rosa"))
        print("1. Selecionar o nível de conhecimento")
        print("2. Seguir para tutorial adaptado")
        print("3. Ir para Fase 1")
        print(f"4. Ir para Fase 2 {'(Bloqueada)' if not fase2_liberada else ''}")
        print("5. Sair")
        opcao = input(cor("Escolha: ", "azul")).strip()

        if opcao == "1":
            teste_nivel()
        elif opcao == "2":
            tutorial()
        elif opcao == "3":
            fase_1()
            fase2_liberada = True
        elif opcao == "4":
            if not fase2_liberada:
                print(cor("\nA fase 2 ainda não está liberada! Complete a fase 1 primeiro.", "vermelho"))
                input("Pressione Enter para escolher uma opção válida")
            else:
                fase_2()
        elif opcao == "5":
            print(cor("Saindo do jogo...", "azul"))
            sys.exit()
        else:
            print(cor("Opção inválida. Digite novamente.", "vermelho"))

# ------------------- MENU DE JOGADORES -------------------
def menu():
    limpar_tela()
    while True:
        print(cor("\n===== MENU DE JOGADORES =====", "rosa"))
        print("1. Atualizar jogador")
        print("2. Ir para o menu principal")
        print("3. Sair")
        opcao = input(cor("Escolha uma opção: ", "azul")).strip()

        if opcao == "1":
            atualizar_jogador()
        elif opcao == "2":
            menu_principal()
            break
        elif opcao == "3":
            print(cor("Saindo do jogo...", "azul"))
            sys.exit()
        else:
            print(cor("Opção inválida. Digite novamente.", "vermelho"))