# ------------------- VARIÁVEIS GLOBAIS -------------------
historico = []
xp = 0
nivel = 1
meta_xp = 60

# ----------------- LIMPAR TELA -----------------
from utils import limpar_tela
# -------------------- COLORIR TEXTO ------------------------
from utils import cor
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
  print(cor("Você passou da fase 1, parabéns!", "verde"))
  input("\nPressione Enter para continuar")

def nivel_1():
    global xp
    while True:
        limpar_tela()
        print(cor("\nBem-vindo(a) ao Nível 1: Cozinha do Caos!", "rosa"))
        print("""\n
Antes de fazer um bolo, precisamos seguir a ordem certa dos passos.
Em programação, fazemos a mesma coisa com os códigos.
Isso se chama lógica e sequência!""")
        print(cor("\nEm uma receita, temos: 3 ovos, 2 xícaras de farinha, 1 xícara de açúcar e 1/2 xícara de leite.", "azul"))
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
        resposta = input(cor("\nDigite a ordem correta dos passos, separados por vírgula: ", "rosa")).strip()

        if resposta == "1,9,4,6,3,7,5,2,8":
            print(cor("\nParabéns! Você acertou!", "verde"))
            xp += 20
            passar_nivel()
            historico.append("Desafio da cozinha do caos completo")
            input("\nPressione Enter para continuar")
            return True
        else:
            print(cor("\nTente novamente!", "vermelho"))
            historico.append("Desafio 1: Não passou")
            input("\nPressione Enter para tentar de novo")

def nivel_2():
    global xp
    while True:
        limpar_tela()
        print(cor("\nBem-vindo(a) ao Nível 2: Mercado Desorganizado!", "rosa"))
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

        resposta = input(cor("\nDigite 1 item que está no lugar errado: ", "rosa")).strip().lower()
        itens_errados = "biscoito", "refrigerante", "detergente", "arroz", "feijão"

        if resposta in itens_errados:
            print(cor("\nParabéns! Você acertou!", "verde"))
            xp += 20
            passar_nivel()
            historico.append(f"Desafio completo! Acertou o item {resposta}")
            input("\nPressione Enter para continuar")
            return True
        else:
            print(cor("\nTente novamente!", "vermelho"))
            historico.append("Desafio 2: Não acertou")
            input("\nPressione Enter para tentar novamente")

def nivel_3():
    global xp
    while True:
        limpar_tela()
        print(cor("\nBem-vindo(a) ao Nível 3: Cidade dos Erros!", "rosa"))
        print("""\n
Na cidade cheia de ruas, escolher o caminho certo é essencial. 
Em programação, usamos decisões para escolher que caminho seguir. 
É assim que o programa pensa!""")
        print(cor("\nEscolha o caminho certo: A, B ou C.", "azul"))
        print("A: Sequência lógica que organiza ideias e verifica erros.")
        print("B: Pule etapas, causando erros.")
        print("C: Repita ações infinitamente, sem fim.")
        resposta = input(cor("\nQual caminho? (A, B ou C): ", "rosa")).strip().upper()

        if resposta == "A":
            print(cor("\nParabéns! Você passou.", "verde"))
            xp += 20
            passar_nivel()
            historico.append("Desafio da cidade dos erros completo")
            input("\nPressione Enter para continuar")
            return True
        else:
            print(cor("\nCaminho errado! Tente novamente.", "vermelho"))
            historico.append("Desafio 3: Não passou")
            input("\nPressione Enter para tentar de novo")