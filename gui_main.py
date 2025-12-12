from reward_screen import RewardScreen
from ranking_screen import RankingScreen
from fase3_screen import Fase3Screen
from fase2_screen import Fase2Screen
from fase1_screen import Fase1Screen
from menuprincipal_screen import MenuPrincipalScreen
from menuinicial_auth import MenuInicialAuth
from screens import StartScreen, InputBox
from desafios_extras_screen import DesafiosExtrasScreen
from fase4_screen import Fase4Screen
from teste_nivel_screen import TesteNivelScreen
from tutorial_screen import TutorialScreen
from atualizar_jogador_screen import AtualizarJogadorScreen
from menujogadores_screen import MenuJogadoresScreen

# CUTSCENES
from cutscenes.cutscene_intro_screen import CutsceneIntroScreen
from cutscenes.cutscene_final_screen import CutsceneFinalScreen

import pygame
import sys
import os
from auth import Auth, Jogador
from utils import carregar_jogadores, salvar_jogadores
from utils_audio import init_audio, load_sound

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
init_audio()

# ------------------------------------------------
# CONSTANTES
# ------------------------------------------------
LARGURA_TELA = 800
ALTURA_TELA = 600
TITULO_JOGO = "Hello Code! - Aventura Pygame"
FPS = 60
PRETO = (0, 0, 0)

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
PIXEL_FONT_PATH = os.path.join(ASSETS_DIR, "PressStart2P-Regular.ttf")

sounds_dir = os.path.join(ASSETS_DIR, "sounds")
load_sound("error", os.path.join(sounds_dir, "erro.mp3"))
load_sound("point", os.path.join(sounds_dir, "faseconcluida.mp3"))
load_sound("vitoria", os.path.join(sounds_dir, "vitoriafinal.mp3"))

# ------------------------------------------------
# CLASSE PRINCIPAL
# ------------------------------------------------


class HelloCodeGUI:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption(TITULO_JOGO)
        self.clock = pygame.time.Clock()
        self.running = True

        # Lógica
        self.jogadores = carregar_jogadores()
        self.auth = Auth(None, None, self.jogadores, salvar_jogadores)

        self.jogador_atual = None  # objeto Jogador

        # Telas
        self.estado_atual = "START_SCREEN"
        self.telas = {}

        self.telas["START_SCREEN"] = StartScreen(LARGURA_TELA, ALTURA_TELA)
        self.telas["MENU_INICIAL_AUTH"] = MenuInicialAuth(
            LARGURA_TELA, ALTURA_TELA,
            self.auth, carregar_jogadores, salvar_jogadores
        )

        # Telas dinâmicas
        for key in [
            "MENU_PRINCIPAL", "MENU_JOGADORES", "ATUALIZAR_JOGADOR",
            "TUTORIAL", "TESTE_NIVEL", "FASE_1", "FASE_2", "FASE_3",
            "FASE_4", "RANKING", "DESAFIOS_EXTRAS", "REWARD",
            "CUTSCENE_INTRO", "CUTSCENE_FINAL"
        ]:
            self.telas[key] = None

    # ------------------------------------------------
    # DEBUG: LIBERAR TODAS AS FASES (CLIQUE SECRETO)
    # ------------------------------------------------

    def ativar_debug(self):
        print("DEBUG: Ativado por clique secreto!")

        # Se jogador não está logado, pega o primeiro
        if self.jogador_atual is None:
            if len(self.jogadores) > 0:
                nome = list(self.jogadores.keys())[0]
                self.jogador_atual = Jogador.from_dict(nome, self.jogadores[nome])
            else:
                print("DEBUG: Nenhum jogador encontrado.")
                return

        # Jogador é OBJETO → acessar via atributo
        self.jogador_atual.fase = 5

        # Precisa atualizar o dicionário salvo
        nome = self.jogador_atual.nome.upper()
        if nome in self.jogadores:
            self.jogadores[nome]["fase"] = 5

        salvar_jogadores(self.jogadores)

        print("DEBUG: TODAS AS FASES FORAM LIBERADAS!")

        # Atualiza menu se estiver nele
        if self.estado_atual == "MENU_PRINCIPAL":
            self.telas["MENU_PRINCIPAL"] = MenuPrincipalScreen(
                LARGURA_TELA, ALTURA_TELA,
                self.jogador_atual,
                salvar_jogadores,
                self.jogadores
            )

    # ------------------------------------------------
    # EVENTOS
    # ------------------------------------------------

    def lidar_com_eventos(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            # ===========================
            # DEBUG: clique secreto
            # ===========================
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x < 50 and y < 50:  # área secreta
                    self.ativar_debug()
                    continue

            # ===========================
            # EVENTOS DAS TELAS
            # ===========================
            tela = self.telas.get(self.estado_atual)

            if tela is not None:
                resultado = tela.lidar_com_eventos(event)

                if resultado:

                    if resultado == "QUIT":
                        self.running = False
                        return

                    proximo_estado = None
                    dado_extra = None

                    # Telas que retornam tupla (estado, jogador)
                    if isinstance(resultado, tuple):
                        proximo_estado, dado_extra = resultado

                        if dado_extra is not None and not isinstance(dado_extra, tuple):
                            self.jogador_atual = dado_extra  # jogador é OBJETO

                    else:
                        proximo_estado = resultado

                    # REWARD SCREEN → avançar nível
                    if proximo_estado == "NEXT_LEVEL":
                        reward_tela = self.telas.get("REWARD")
                        if reward_tela:
                            fase_id = reward_tela.fase_id
                            chave = f"FASE_{fase_id}"

                            fase_obj = self.telas.get(chave)
                            if fase_obj:
                                fase_obj._avancar_nivel()

                            self.telas["REWARD"] = None
                            proximo_estado = chave

                        else:
                            proximo_estado = "MENU_PRINCIPAL"

                    # --------------------------
                    # TROCA DE TELAS
                    # --------------------------
                    if proximo_estado:

                        if proximo_estado == "FASE_1":
                            if self.telas["CUTSCENE_INTRO"] is None:
                                self.telas["CUTSCENE_INTRO"] = CutsceneIntroScreen(LARGURA_TELA, ALTURA_TELA)
                                self.estado_atual = "CUTSCENE_INTRO"
                                return

                        if proximo_estado == "INICIAR_FASE_1":
                            self.telas["FASE_1"] = Fase1Screen(
                                LARGURA_TELA, ALTURA_TELA,
                                self.jogador_atual, salvar_jogadores, self.jogadores
                            )
                            self.estado_atual = "FASE_1"
                            return

                        if proximo_estado == "CUTSCENE_FINAL":
                            self.telas["CUTSCENE_FINAL"] = CutsceneFinalScreen(LARGURA_TELA, ALTURA_TELA)
                            self.estado_atual = "CUTSCENE_FINAL"
                            return

                        if proximo_estado == "FINALIZAR_JOGO":
                            self.estado_atual = "MENU_PRINCIPAL"
                            return

                        # Menus
                        if proximo_estado == "MENU_PRINCIPAL":
                            self.telas["MENU_PRINCIPAL"] = MenuPrincipalScreen(
                                LARGURA_TELA, ALTURA_TELA,
                                self.jogador_atual,
                                salvar_jogadores,
                                self.jogadores
                            )

                        elif proximo_estado == "MENU_JOGADORES":
                            self.telas["MENU_JOGADORES"] = MenuJogadoresScreen(
                                LARGURA_TELA, ALTURA_TELA,
                                self.jogador_atual, salvar_jogadores, self.jogadores
                            )

                        elif proximo_estado == "ATUALIZAR_JOGADOR":
                            self.telas["ATUALIZAR_JOGADOR"] = AtualizarJogadorScreen(
                                LARGURA_TELA, ALTURA_TELA,
                                self.jogador_atual, self.auth,
                                salvar_jogadores, self.jogadores
                            )

                        elif proximo_estado == "TUTORIAL":
                            self.telas["TUTORIAL"] = TutorialScreen(
                                LARGURA_TELA, ALTURA_TELA, self.jogador_atual
                            )

                        elif proximo_estado == "TESTE_NIVEL":
                            self.telas["TESTE_NIVEL"] = TesteNivelScreen(
                                LARGURA_TELA, ALTURA_TELA,
                                self.jogador_atual, salvar_jogadores, self.jogadores
                            )

                        # Fases
                        elif proximo_estado == "FASE_2":
                            self.telas["FASE_2"] = Fase2Screen(
                                LARGURA_TELA, ALTURA_TELA,
                                self.jogador_atual, salvar_jogadores, self.jogadores
                            )

                        elif proximo_estado == "FASE_3":
                            self.telas["FASE_3"] = Fase3Screen(
                                LARGURA_TELA, ALTURA_TELA,
                                self.jogador_atual, salvar_jogadores, self.jogadores
                            )

                        elif proximo_estado == "FASE_4":
                            self.telas["FASE_4"] = Fase4Screen(
                                LARGURA_TELA, ALTURA_TELA,
                                self.jogador_atual, salvar_jogadores, self.jogadores
                            )

                        # Ranking
                        elif proximo_estado == "RANKING":
                            self.telas["RANKING"] = RankingScreen(
                                LARGURA_TELA, ALTURA_TELA,
                                self.jogador_atual
                            )

                        # Desafios extras
                        elif proximo_estado == "DESAFIOS_EXTRAS":
                            self.telas["DESAFIOS_EXTRAS"] = DesafiosExtrasScreen(
                                LARGURA_TELA, ALTURA_TELA,
                                self.jogador_atual, salvar_jogadores, self.jogadores
                            )

                        # Reward screen
                        elif proximo_estado == "REWARD":
                            fase_id, nivel_idx = 1, 1

                            if isinstance(dado_extra, tuple) and len(dado_extra) == 2:
                                fase_id, nivel_idx = dado_extra

                            self.telas["REWARD"] = RewardScreen(
                                LARGURA_TELA, ALTURA_TELA,
                                self.jogador_atual,
                                fase_id,
                                nivel_idx,
                                fase_id == 4 and nivel_idx == 2
                            )

                        # Logout
                        elif proximo_estado == "LOGOUT":
                            self.jogador_atual = None
                            for key in self.telas.keys():
                                if key not in ["START_SCREEN", "MENU_INICIAL_AUTH"]:
                                    self.telas[key] = None

                            proximo_estado = "MENU_INICIAL_AUTH"

                        # Aplicar mudança de tela
                        self.estado_atual = proximo_estado

    # ------------------------------------------------
    # UPDATE
    # ------------------------------------------------

    def atualizar(self):
        tela = self.telas.get(self.estado_atual)
        if tela is not None:
            tela.atualizar()

    # ------------------------------------------------
    # DESENHAR
    # ------------------------------------------------

    def desenhar(self):
        self.tela.fill(PRETO)

        tela = self.telas.get(self.estado_atual)
        if tela is not None:
            tela.desenhar(self.tela)

        pygame.display.flip()

    # ------------------------------------------------
    # LOOP PRINCIPAL
    # ------------------------------------------------

    def rodar(self):
        while self.running:
            self.clock.tick(FPS)
            self.lidar_com_eventos()
            self.atualizar()
            self.desenhar()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    jogo = HelloCodeGUI()
    jogo.rodar()
