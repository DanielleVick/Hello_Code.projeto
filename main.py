# ------------------- IMPORTS -------------------
import re
import sys
import time
import json
import os
from datetime import datetime, date

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
        print("Nenhum dado encontrado. Iniciando vazio...")
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

# ------------------- CADASTRO -------------------
def validar_data_nascimento(data):
    try:
        data_nascimento = datetime.strptime(data, "%d/%m/%Y").date()
        hoje = date.today()

        if data_nascimento > hoje:
            return False
        else:
            return True
    except ValueError:
        return False
def solicitar_data(): 
    while True:
      data_nascimento = input("Data de nascimento (DD/MM/AAAA): ").strip()
      if validar_data_nascimento(data_nascimento):
        print("Data válida!")
        break
      else:
       print("Data inválida! Use o formato DD/MM/AAAA e uma data real.")

def validar_senha(senha):
    return 6 <= len(senha) <= 10 and re.search(r"[A-Z]", senha) and re.search(r"[^A-Za-z0-9]", senha)

def cadastro():
    limpar_tela()
    print("===== CADASTRO =====")
    while True:
        nome = input("Nome do jogador: ").strip().upper()
        if nome in jogadores:
            print("Já existe um jogador com esse nome. Tente outro.")
            continue

        data_nascimento = solicitar_data()

        while True:
            senha = input("Senha: ").strip()
            if validar_senha(senha):
                break
            print("Senha inválida! Deve ter de 6 a 10 caracteres, com 1 maiúscula e 1 caractere especial.")

        jogadores[nome] = {
            "data_nascimento": data_nascimento,
            "senha": senha,
            "nivel": 1,
            "fase": 1
        }
        print("\nJogador cadastrado com sucesso!")
        salvar_jogadores()
        input("Pressione Enter para continuar...")
        break


#----------------------- LOGIN -------------------------------
def verificar_usuario(nome, senha):
    return nome in jogadores and jogadores[nome]["senha"] == senha

def login():
    global logado
    limpar_tela()
    print("===== LOGIN =====")
    usuario = input("Digite seu usuário: ").strip()
    senha = input("Digite sua senha: ").strip()

    if verificar_usuario(usuario, senha):
        print("Login bem-sucedido!")
        logado = True
        input("Pressione Enter para continuar...")
    else:
        print("Usuário ou senha incorretos.")
        input("Pressione Enter para tentar novamente...")

# ------------------- ATUALIZAÇÃO -------------------
def atualizar_jogador():
    limpar_tela()
    nome = input("\nNome do jogador para atualizar: ").strip().upper()
    if nome not in jogadores:
        print("Jogador não encontrado.")
        return

    while True:
        print("\nO que deseja atualizar?")
        print("1. Data de nascimento")
        print("2. Senha")
        print("3. Voltar")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            while True:
                nova_data = input("Nova data (DD/MM/AAAA): ").strip()
                if validar_data_nascimento(nova_data):
                    jogadores[nome]["data_nascimento"] = nova_data
                    print("Data atualizada com sucesso!")
                    break
                print("Data inválida! Tente novamente.")
        elif opcao == "2":
            while True:
                nova_senha = input("Nova senha: ").strip()
                if validar_senha(nova_senha):
                    jogadores[nome]["senha"] = nova_senha
                    print("Senha atualizada com sucesso!")
                    break
                print("Senha inválida! Tente novamente.")
        elif opcao == "3":
            break
        else:
            print("Opção inválida.")
            
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

# ------------------- MENU DE JOGADORES -------------------
def menu():
    limpar_tela()
    while True:
        print("\n===== MENU DE JOGADORES =====")
        print("1. Atualizar jogador")
        print("2. Ir para o menu principal")
        print("3. Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            atualizar_jogador()
        elif opcao == "2":
            menu_principal()
            break
        elif opcao == "3":
            print("Saindo do sistema...")
            sys.exit()
        else:
            print("Opção inválida.")

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
        print("\nBem-vindo(a) à fase 1")
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
    print("Você passou da fase 2, parabéns! Aguarde até as próximas fases!")
    input("Pressione Enter para continuar")
    
def nivel_1_fase2():
    global xp
    while True:
        limpar_tela()
        print("\nBem-vindo(a) à fase 2")
        print("\nBem-vindo(a) ao Nível 1: Laboratório Maluco!")
        print("""\n
Neste laboratório, cada frasco guarda um valor.
Assim como misturar ingredientes, um programa usa variáveis para armazenar e usar dados depois. 
Cuidado com as combinações!""") 
        print("\nVocê precisa combinar dois frascos usando uma operação matemática correta para criar a fórmula.\n")
        frascos = {'A': 5, 'B': 10, 'C': 3}
        for f, v in frascos.items():
            print(f"{f}: {v}")

        operacao = input("\nEscolha a operação (somar/multiplicar): ").strip().lower()
        f1 = input("Escolha o primeiro frasco (A/B/C): ").strip().upper()
        f2 = input("Escolha o segundo frasco (A/B/C): ").strip().upper()

        if f1 not in frascos or f2 not in frascos or operacao not in ['somar','multiplicar']:
            print("PUF...! Algo está errado! Tente novamente.")
            continue

        if operacao == 'somar':
            resultado = frascos[f1] + frascos[f2]
            print("BOOM!!!")
            print(f"Resultado = {frascos[f1]} + {frascos[f2]} = {resultado}")
           
        else:
            resultado = frascos[f1] * frascos[f2]
            print("TCHARAAAN!!")
            print(f"Resultado = {frascos[f1]} * {frascos[f2]} = {resultado}")

        print("\nParabéns! Você completou o desafio do laboratório.")
        xp += 20
        passar_nivel()
        input("\nPressione Enter para continuar")
        return True

def nivel_2_fase2():
    global xp
    while True:
        limpar_tela()
        print("\nBem-vindo(a) ao Nível 2: Ilha dos Tesouros!")
        print("""\n
Para achar o tesouro, você precisa calcular o caminho certo.
Em programação, usamos operações para transformar valores e descobrir resultados. 
Um símbolo errado… e você fica preso na ilha!\n""")
        baus = {1: 5, 2: 8, 3: 2}
        for b, v in baus.items():
            print(f"Baú {b}: {v} moedas")

        operacao = input("\nEscolha a operação (somar/multiplicar/resto): ").strip().lower()
        try:
            b1 = int(input("Escolha o primeiro baú (1/2/3): ").strip())
            b2 = int(input("Escolha o segundo baú (1/2/3): ").strip())
        except ValueError:
            print("Entrada inválida. Digite números válidos.")
            continue

        if b1 not in baus or b2 not in baus or operacao not in ['somar','multiplicar','resto']:
            print("Algo está errado! Tente novamente.")
            continue

        if operacao == 'somar':
            resultado = baus[b1] + baus[b2]
            print(f"Resultado = {baus[b1]} + {baus[b2]} = {resultado}")
        elif operacao == 'multiplicar':
            resultado = baus[b1] * baus[b2]
            print(f"Resultado = {baus[b1]} * {baus[b2]} = {resultado}")
        elif operacao == 'resto':
            if baus[b2] == 0:
                print("Não é possível dividir por zero.")
                continue
            resultado = baus[b1] % baus[b2]

        print(f"Resultado da operação: {resultado}")
        print("\nParabéns! Você completou o desafio da ilha.")
        xp += 20
        passar_nivel()
        input("\nPressione Enter para continuar")
        return True

def nivel_3_fase2():
    global xp
    while True:
        limpar_tela()
        print("\nBem-vindo(a) ao Nível 3: Salão Mágico do Guardião!")
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
            print("Digite apenas números. Tente novamente.")
            continue
        if {valor1, valor2} == {7,9} and resposta == 16:
            print(f"\nResultado = {valor1} + {valor2} = {resposta}")
            print("\nParabéns! Você entendeu o conceito de função.")
            xp += 20
            passar_nivel()
            print("\nVocê concluiu a Fase 2! Retornando ao menu...")
            input("\nPressione Enter para continuar")
            return True
        else:
            print("Resposta incorreta. Tente novamente.")
            input("\nPressione Enter para tentar de novo...")
            break
        
# ------------------- EXECUÇÃO PRINCIPAL -------------------

carregar_jogadores()  

while True:
    menu_inicial()
    escolha = input("Escolha uma opção: ").strip()
    if escolha == "1":
        cadastro()       
        iniciar_jogo()
        break  
    elif escolha == "2":
        login()
        if logado: 
            menu_principal()  
    elif escolha == "3":
        print("Saindo do jogo...")
        sys.exit()
    else:
        print("Opção inválida. Tente novamente.")

# Menu de jogadores 
menu()  

