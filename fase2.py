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
        print(cor(f"Parabéns! Você subiu para o nível {nivel}!", "verde"))

# ----------------- FASE 2 --------------------
def fase_2():
    global nivel
    nivel = 1 
    if nivel_1_fase2(): 
      nivel += 1
    if nivel_2_fase2():  
      nivel += 1
    if nivel_3_fase2():  
      nivel += 1
    print(cor("Você passou da fase 2, parabéns! Aguarde até as próximas fases!", "verde"))
    input("Pressione Enter para continuar")
    
def nivel_1_fase2():
    global xp
    while True:
        limpar_tela()
        print(cor("\nBem-vindo(a) ao Nível 1: Laboratório Maluco!", "rosa"))
        print("""\n
Neste laboratório, cada frasco guarda um valor.
Assim como misturar ingredientes, um programa usa variáveis para armazenar e usar dados depois. 
Cuidado com as combinações!""") 
        print(cor("\nVocê precisa combinar dois frascos usando uma operação matemática correta para criar a fórmula.\n", "azul"))
        frascos = {'A': 5, 'B': 10, 'C': 3}
        for f, v in frascos.items():
            print(f"{f}: {v}")

        operacao = input(cor("\nEscolha a operação (somar/multiplicar): ", "azul")).strip().lower()
        f1 = input("Escolha o primeiro frasco (A/B/C): ").strip().upper()
        f2 = input("Escolha o segundo frasco (A/B/C): ").strip().upper()

        if f1 not in frascos or f2 not in frascos or operacao not in ['somar','multiplicar']:
            print(cor("PUF...! Algo está errado! Tente novamente.", "vermelho"))
            continue

        if operacao == 'somar':
            resultado = frascos[f1] + frascos[f2]
            print(cor("BOOM!!!", "verde"))
            print(f"Resultado = {frascos[f1]} + {frascos[f2]} = {resultado}")
           
        else:
            resultado = frascos[f1] * frascos[f2]
            print(cor("TCHARAAAN!!", "verde"))
            print(f"Resultado = {frascos[f1]} * {frascos[f2]} = {resultado}")

        print(cor("\nParabéns! Você completou o desafio do laboratório.", "verde"))
        xp += 20
        passar_nivel()
        historico.append("Desafio do laboratório maluco completo.")
        input("\nPressione Enter para continuar")
        return True

def nivel_2_fase2():
    global xp
    while True:
        limpar_tela()
        print(cor("\nBem-vindo(a) ao Nível 2: Ilha dos Tesouros!", "rosa"))
        print("""\n
Para achar o tesouro, você precisa calcular o caminho certo.
Em programação, usamos operações para transformar valores e descobrir resultados. 
Um símbolo errado… e você fica preso na ilha!\n""")
        baus = {1: 5, 2: 8, 3: 2}
        for b, v in baus.items():
            print(f"Baú {b}: {v} moedas")

        operacao = input(cor("\nEscolha a operação (somar/multiplicar/resto): ", "azul")).strip().lower()
        try:
            b1 = int(input("Escolha o primeiro baú (1/2/3): ").strip())
            b2 = int(input("Escolha o segundo baú (1/2/3): ").strip())
        except ValueError:
            print(cor("Entrada inválida. Digite números válidos.", "vermelho"))
            continue

        if b1 not in baus or b2 not in baus or operacao not in ['somar','multiplicar','resto']:
            print(cor("Algo está errado! Tente novamente.", "vermelho"))
            continue

        if operacao == 'somar':
            resultado = baus[b1] + baus[b2]
            print(f"Resultado = {baus[b1]} + {baus[b2]} = {resultado}")
        elif operacao == 'multiplicar':
            resultado = baus[b1] * baus[b2]
            print(f"Resultado = {baus[b1]} * {baus[b2]} = {resultado}")
        elif operacao == 'resto':
            if baus[b2] == 0:
                print(cor("Não é possível dividir por zero.", "vermelho"))
                continue
            resultado = baus[b1] % baus[b2]

        print(f"Resultado da operação: {resultado}")
        print(cor("\nParabéns! Você completou o desafio da ilha.", "verde"))
        xp += 20
        passar_nivel()
        historico.append("Desafio da ilha dos tesouros completo.")
        input("\nPressione Enter para continuar")
        return True

def nivel_3_fase2():
    global xp
    while True:
        limpar_tela()
        print(cor("\nBem-vindo(a) ao Nível 3: Salão Mágico do Guardião!", "rosa"))
        print("""\n
O Guardião quer saber se você entende as funções. 
Quando você envia valores, uma função pensa e devolve uma resposta. 
Se enviar os ingredientes certos… ela te dará o número final!\n""")
        print("Por exemplo: se somarmos 4 e 6, a função retornaria 10.")
        print("""
              \nValores recebidos: 4 e 6
              Cálculo realizado: soma
              Resultado = 4 + 6 = 10""")
        print("""\n
Agora é a sua vez! Envie os valores 7 e 9 
para a função e solucione o resultado.""")
        try:
            valor1 = int(input("Digite o primeiro valor recebido: "))   
            valor2 = int(input("Digite o segundo valor recebido: "))
            resposta = int(input("Digite o resultado da mistura de 7 e 9: ").strip())
        except ValueError:
            print(cor("Digite apenas números. Tente novamente.", "vermelho"))
            continue
        if {valor1, valor2} == {7,9} and resposta == 16:
            print(f"\nResultado = {valor1} + {valor2} = {resposta}")
            print(cor("\nParabéns! Você entendeu o conceito de função.", "verde"))
            xp += 20
            passar_nivel()
            historico.append("Desafio do salão mágico completo.")
            print(cor("\nVocê concluiu a Fase 2! Retornando ao menu...", "verde"))
            input("\nPressione Enter para continuar")
            return True
        else:
            print(cor("Resposta incorreta. Tente novamente.", "vermelho"))
            input("\nPressione Enter para tentar de novo...")
            break
        