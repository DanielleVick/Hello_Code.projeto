
import os
import json
from colorama import Fore, Style

# ===========================================
# ARQUIVO JSON DOS JOGADORES
# ===========================================
JOGADORES_JSON = os.path.join(os.path.dirname(__file__), "jogadores.json")


# ===========================================
# LIMPAR TELA
# ===========================================
def limpar_tela():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


# ===========================================
# COR DO TEXTO
# ===========================================
def cor(texto, nome_cor):
    cores = {
        "vermelho": Fore.RED,
        "verde": Fore.GREEN,
        "azul": Fore.BLUE,
        "amarelo": Fore.YELLOW,
        "roxo": Fore.MAGENTA,
        "rosa": Fore.LIGHTMAGENTA_EX,
        "branco": Fore.WHITE
    
    }
    return cores.get(nome_cor, Fore.WHITE) + texto + Style.RESET_ALL


# ===========================================
# CARREGAR JOGADORES
# ===========================================
def carregar_jogadores() -> dict:
    if not os.path.exists(JOGADORES_JSON):
        return {}

    try:
        with open(JOGADORES_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
            else:
                return {}
    except Exception:
        return {}


# ===========================================
# SALVAR JOGADORES
# ===========================================
def salvar_jogadores(jogadores: dict) -> None:
    """
    Salva o dicionário de jogadores no arquivo JSON.
    """
    with open(JOGADORES_JSON, "w", encoding="utf-8") as f:
        json.dump(jogadores, f, ensure_ascii=False, indent=2)


# ===========================================
# INICIAR JOGO
# ===========================================
def iniciar_jogo():
    limpar_tela()
    print(cor("Iniciando o jogo...", "verde"))
