# -------------------- COLORIR TEXTO ------------------------
from utils import cor
#------------------------ NÍVEL DE CONHECIMENTO --------------------------
def teste_nivel():
    print(cor("===== TESTE DE NÍVEL DE CONHECIMENTO =====\n", "roxo"))
    score = 0

    print(cor("1) O que é uma variável em programação?", "rosa"))
    print("a) Um número fixo")
    print("b) Um espaço que armazena dados")
    print("c) Um tipo de loop")
    resposta = input(cor("Escolha a letra correta: ", "azul")).strip().lower()

    if resposta == "b":
        score += 1

    print(cor("\n2) Qual operador é usado para multiplicação?", "rosa"))
    print("a) +")
    print("b) -")
    print("c) *")
    resposta = input(cor("Escolha a letra correta: ", "azul")).strip().lower()
    if resposta == "c":
        score += 1

    print(cor("\n3) O que significa 'if' em Python?", "rosa"))
    print("a) Estrutura de repetição")
    print("b) Estrutura condicional")
    print("c) Declaração de função")
    resposta = input(cor("Escolha a letra correta: ", "azul")).strip().lower()
    if resposta == "b":
        score += 1

  # AVALIAÇÃO FINAL
    print(cor("\n===== RESULTADO =====", "verde"))
    if score == 3:
        print("Nível: Avançado")
    elif score == 2:
        print("Nível: Intermediário")
    else:
        print("Nível: Iniciante")
    
    input("Pressione Enter para voltar ao menu...")