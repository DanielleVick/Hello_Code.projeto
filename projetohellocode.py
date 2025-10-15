# ------------------- IMPORTS -------------------
import re  # Para expressões regulares

# ------------------- VARIÁVEIS GLOBAIS -------------------
jogadores = {}
rodando = True
historico = []
xp = 0
nivel = 1
meta_xp = 100

# ------------------- FUNÇÕES -------------------

def iniciar_jogo():
    print("Bem-vindo(a) ao Hello Code!")

def menu_inicial():
    print("\n===== MENU INICIAL =====")
    print("1. Cadastro")
    print("2. Login")

def login():
    print("Login selecionado.")

# ---------- CADASTRO ----------
def validar_data_nascimento(data):
    return bool(re.match(r"^\d{2}/\d{2}/\d{4}$", data))

def validar_senha(senha):
    if 6 <= len(senha) <= 10 and re.search(r"[A-Z]", senha) and re.search(r"[^A-Za-z0-9]", senha):
        return True
    return False

def cadastro():
    while True:
        nome = input("\nNome do jogador: ").strip()
        if nome in jogadores:
            print("❌ Já existe um jogador com esse nome. Tente outro.")
            continue

        while True:
            data_nascimento = input("Data de nascimento (DD/MM/AAAA): ").strip()
            if validar_data_nascimento(data_nascimento):
                break
            print("❌ Data inválida! Use o formato DD/MM/AAAA.")

        while True:
            senha = input("Senha: ").strip()
            if validar_senha(senha):
                break
            print("❌ Senha inválida! Deve ter de 6 a 10 caracteres, com 1 maiúscula e 1 especial.")

        jogadores[nome] = {"data_nascimento": data_nascimento, "senha": senha}
        print("✅ Jogador cadastrado com sucesso!")
        break

# ---------- ATUALIZAÇÃO ----------
def atualizar_jogador():
    nome = input("\nNome do jogador para atualizar: ").strip()
    if nome not in jogadores:
        print("❌ Jogador não encontrado.")
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
                    print("✅ Data atualizada com sucesso!")
                    break
                print("❌ Data inválida! Tente novamente.")
        elif opcao == "2":
            while True:
                nova_senha = input("Nova senha: ").strip()
                if validar_senha(nova_senha):
                    jogadores[nome]["senha"] = nova_senha
                    print("✅ Senha atualizada com sucesso!")
                    break
                print("❌ Senha inválida! Tente novamente.")
        elif opcao == "3":
            break
        else:
            print("❌ Opção inválida.")

# ---------- MENU PRINCIPAL ----------
def menu_principal():
    while True:
        print("\n===== MENU PRINCIPAL =====")
        print("1. Selecionar o nível de conhecimento")
        print("2. Seguir para tutorial adaptado")
        print("3. Ir para Fase 1")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            print("Função nivel_conhecimento() não implementada.")  # placeholder
        elif opcao == "2":
            print("Função tutorial_adaptado() não implementada.")  # placeholder
        elif opcao == "3":
            break
        else:
            print("❌ Opção inválida.")

# ---------- MENU DE JOGADORES ----------
def menu():
    while True:
        print("\n===== MENU DE JOGADORES =====")
        print("1. Cadastrar jogador")
        print("2. Atualizar jogador")
        print("3. Ir para o menu principal")
        print("4. Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastro()
        elif opcao == "2":
            atualizar_jogador()
        elif opcao == "3":
            menu_principal()
            break  # sai do menu de jogadores e vai pros níveis
        elif opcao == "4":
            print("👋 Saindo do sistema...")
            exit()
        else:
            print("❌ Opção inválida.")

# ---------- FUNÇÕES DAS FASES ----------
def passar_nivel():
    global nivel, xp, meta_xp
    if xp >= meta_xp:
        nivel += 1
        xp -= meta_xp
        meta_xp += 100
        print(f"Parabéns! Você subiu para o nível {nivel}!")
        print(f"Próximo nível em {meta_xp} XP.")

def nivel_1():
    print("Bem-vindo(a) ao Nível 1: Cozinha do Caos!")
    print("Em uma receita, temos: 3 ovos, 2 xícaras de farinha, 1 xícara de açúcar e 1/2 xícara de leite.")
    print("Qual a ordem correta de passos para fazer um bolo?")
    print("""
    1- Pegar um recipiente
    2- Colocar a forma no forno
    3- Untar a forma
    4- Adicionar os ovos
    5- Ligar o forno
    6- Adicionar os ingredientes líquidos
    7- Colocar a massa na forma
    8- Retirar do forno
    9- Adicionar os ingredientes secos
    """)
    resposta = input("Digite a ordem correta dos passos, separados por vírgula: ").strip()
    global xp
    if resposta == "1,9,4,6,3,7,5,2,8":
        print("Parabéns! Você acertou!")
        xp += 20
        passar_nivel()
        historico.append("Desafio 1: Passou")
        return True
    else:
        print("Tente novamente!")
        historico.append("Desafio 1: Não passou")
        return False

def nivel_2():
    print("Bem-vindo(a) ao Nível 2: Mercado Desorganizado!")
    prateleiras = {
        "frutas": ["maça", "banana", "biscoito", "laranja"],
        "verduras": ["alface", "tomate", "cenoura", "refrigerante"],
        "carnes": ["frango", "carne bovina", "peixe", "detergente"],
        "doces": ["chocolate", "bala", "sorvete", "arroz"],
        "produtos de limpeza": ["sabão", "desinfetante", "amaciante", "feijão"]
    }
    for categoria in prateleiras:
        print(f"{categoria.capitalize()}: {', '.join(prateleiras[categoria])}")

    resposta = input("Digite 1 item que está no lugar errado: ").strip().lower()
    itens_errados = "biscoito", "refrigerante", "detergente", "arroz", "feijão"
    global xp
    if resposta in itens_errados:
        print("Parabéns! Você acertou!")
        xp += 20
        passar_nivel()
        historico.append(f"Desafio 2: Acertou o item {resposta}")
        return True
    else:
        print("Tente novamente!")
        historico.append("Desafio 2: Não acertou")
        return False

def nivel_3():
    print("Bem-vindo(a) ao Nível 3: Cidade dos Erros!")
    print("Escolha o caminho certo: A, B ou C.")
    print("A: Sequência lógica que organiza ideias e verifica erros.")
    print("B: Pule etapas, causando erros.")
    print("C: Repita ações infinitamente, sem fim.")
    resposta = input("Qual caminho? (A, B ou C): ").strip().upper()
    global xp
    if resposta == "A":
        print("Parabéns! Você passou.")
        xp += 20
        passar_nivel()
        historico.append("Desafio 3: Passou")
        return True
    else:
        print("Caminho errado!")
        historico.append("Desafio 3: Não passou")
        return False

# ------------------- EXECUÇÃO PRINCIPAL -------------------

iniciar_jogo()

# Menu inicial
while True:
    menu_inicial()
    escolha = input("Escolha uma opção: ").strip()
    if escolha == "1":
        cadastro()
        break
    elif escolha == "2":
        login()
        break
    else:
        print("Opção inválida. Tente novamente.")

# Menu de jogadores
menu()

# Loop das fases
while rodando and nivel <= 3:
    if nivel == 1:
        if nivel_1():
            nivel += 1
    elif nivel == 2:
        if nivel_2():
            nivel += 1
    elif nivel == 3:
        if nivel_3():
            nivel += 1
            rodando = False

print("Você passou da fase 1, parabéns!")
