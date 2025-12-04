# gui_main.py (FINAL COM INTEGRAÇÃO TOTAL DA INTERFACE)

import pygame
import sys
import os
from auth import Auth 
from utils import carregar_jogadores, salvar_jogadores
from utils_audio import init_audio, load_sound

# ======================== INICIALIZAÇÃO DE AUDIO ==========================

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

init_audio()

# ----------------------------------------------------
# 1. CONSTANTES DE CONFIGURAÇÃO E CAMINHOS
# ----------------------------------------------------
LARGURA_TELA = 800
ALTURA_TELA = 600
TITULO_JOGO = "Hello Code! - Aventura Pygame"
FPS = 60
PRETO = (0, 0, 0)

# Caminho da Fonte (Definido localmente para evitar circular import)
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
PIXEL_FONT_PATH = os.path.join(ASSETS_DIR, "PressStart2P-Regular.ttf")

# ----------------------------------------------------
# 1.5 INICIALIZAÇÃO DE ÁUDIO E CARREGAMENTO DE SONS
# ----------------------------------------------------

assets_dir = os.path.join(os.path.dirname(__file__), "assets")
sounds_dir = os.path.join(assets_dir, "sounds")

load_sound("error", os.path.join(sounds_dir, "erro.mp3"))
load_sound("point", os.path.join(sounds_dir, "faseconcluida.mp3"))
load_sound("vitoria", os.path.join(sounds_dir, "vitoriafinal.mp3"))

# ----------------------------------------------------
# 2. IMPORTAÇÕES DE MÓDULOS (Todas as Telas)
# ----------------------------------------------------
from screens import StartScreen, InputBox 
from menuinicial_auth import MenuInicialAuth 
from menuprincipal_screen import MenuPrincipalScreen 
from menujogadores_screen import MenuJogadoresScreen
from atualizar_jogador_screen import AtualizarJogadorScreen
from tutorial_screen import TutorialScreen
from teste_nivel_screen import TesteNivelScreen
from fase1_screen import Fase1Screen 
from fase2_screen import Fase2Screen 
from fase3_screen import Fase3Screen 
from fase4_screen import Fase4Screen
from ranking_screen import RankingScreen 
from desafios_extras_screen import DesafiosExtrasScreen
from reward_screen import RewardScreen 

# ----------------------------------------------------
# 3. CLASSE PRINCIPAL DO JOGO (GERENCIADOR DE ESTADO)
# ----------------------------------------------------

class HelloCodeGUI:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption(TITULO_JOGO)
        self.clock = pygame.time.Clock()
        self.running = True

        # Inicialização da Lógica
        self.jogadores = carregar_jogadores()
        self.auth = Auth(None, None, self.jogadores, salvar_jogadores) 
        self.jogador_atual = None
        
        # Gestão de Telas
        self.estado_atual = "START_SCREEN"
        self.telas = {}
        
        # Telas Fixas (Instanciadas no início)
        self.telas["START_SCREEN"] = StartScreen(LARGURA_TELA, ALTURA_TELA)
        self.telas["MENU_INICIAL_AUTH"] = MenuInicialAuth(
            LARGURA_TELA, ALTURA_TELA, 
            self.auth, 
            carregar_jogadores, 
            salvar_jogadores
        )
        
        # Slots para Telas de Conteúdo (Instanciadas sob demanda)
        self.telas["MENU_PRINCIPAL"] = None 
        self.telas["MENU_JOGADORES"] = None
        self.telas["ATUALIZAR_JOGADOR"] = None
        self.telas["TUTORIAL"] = None
        self.telas["TESTE_NIVEL"] = None
        self.telas["FASE_1"] = None 
        self.telas["FASE_2"] = None 
        self.telas["FASE_3"] = None 
        self.telas["FASE_4"] = None
        self.telas["RANKING"] = None 
        self.telas["DESAFIOS_EXTRAS"] = None
        self.telas["REWARD"] = None 

    def lidar_com_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.estado_atual in self.telas and self.telas[self.estado_atual] is not None:
                resultado = self.telas[self.estado_atual].lidar_com_eventos(event)
                
                if resultado:
                    # 1. TRATAR O ESTADO DE SAÍDA (QUIT)
                    if resultado == "QUIT" or (isinstance(resultado, tuple) and resultado[0] == "QUIT"):
                        self.running = False
                        return 

                    # 2. TRATAR MUDANÇA DE ESTADO
                    if isinstance(resultado, tuple):
                        proximo_estado, jogador_obj = resultado
                        if jogador_obj:
                            self.jogador_atual = jogador_obj
                    else:
                        proximo_estado = resultado
                        jogador_obj = self.jogador_atual 

                    if proximo_estado:
                        
                        # --- TRATAR AVANÇO DE NÍVEL (SAÍDA DA REWARD SCREEN) ---
                        if proximo_estado == "NEXT_LEVEL":
                            # 1. Obter a ID da Fase correta a partir da RewardScreen
                            fase_id_ativa = self.telas["REWARD"].fase_id 
                            chave_fase = f"FASE_{fase_id_ativa}" # Ex: "FASE_1"
                            
                            # 2. Chamar _avancar_nivel na instância da Fase correta
                            fase_ativa = self.telas[chave_fase] 
                            fase_ativa._avancar_nivel() 
                            
                            # 3. Finalizar a transição
                            proximo_estado = chave_fase # O estado volta para a FaseXScreen
                            self.telas["REWARD"] = None # Destrói a tela de recompensa
                            
                        
                        # 4. LÓGICA DE TRANSIÇÃO PRINCIPAL (Instanciação - Mantida)
                        
                        elif proximo_estado == "MENU_PRINCIPAL":
                            self.telas["MENU_PRINCIPAL"] = MenuPrincipalScreen(
                                LARGURA_TELA, ALTURA_TELA, 
                                self.jogador_atual, 
                                salvar_jogadores, 
                                self.jogadores
                            )
                        
                        elif proximo_estado == "MENU_JOGADORES":
                            self.telas["MENU_JOGADORES"] = MenuJogadoresScreen(
                                LARGURA_TELA, ALTURA_TELA, 
                                self.jogador_atual, 
                                salvar_jogadores, 
                                self.jogadores
                            )
                        
                        elif proximo_estado == "ATUALIZAR_JOGADOR":
                            self.telas["ATUALIZAR_JOGADOR"] = AtualizarJogadorScreen(
                                LARGURA_TELA, ALTURA_TELA, 
                                self.jogador_atual, 
                                self.auth,
                                salvar_jogadores, 
                                self.jogadores
                            )
                            
                        elif proximo_estado == "TUTORIAL":
                             self.telas["TUTORIAL"] = TutorialScreen(
                                LARGURA_TELA, ALTURA_TELA, 
                                self.jogador_atual
                            )
                            
                        elif proximo_estado == "TESTE_NIVEL":
                             self.telas["TESTE_NIVEL"] = TesteNivelScreen(
                                LARGURA_TELA, ALTURA_TELA, 
                                self.jogador_atual,
                                salvar_jogadores, 
                                self.jogadores
                            )
                        
                        # Instanciação das Fases (FASE_1 a FASE_4)
                        elif proximo_estado == "FASE_1":
                             self.telas["FASE_1"] = Fase1Screen(
                                LARGURA_TELA, ALTURA_TELA, self.jogador_atual, salvar_jogadores, self.jogadores
                            )
                        elif proximo_estado == "FASE_2":
                             self.telas["FASE_2"] = Fase2Screen(
                                LARGURA_TELA, ALTURA_TELA, self.jogador_atual, salvar_jogadores, self.jogadores
                            )
                        elif proximo_estado == "FASE_3":
                             self.telas["FASE_3"] = Fase3Screen(
                                LARGURA_TELA, ALTURA_TELA, self.jogador_atual, salvar_jogadores, self.jogadores
                            )
                        elif proximo_estado == "FASE_4":
                             self.telas["FASE_4"] = Fase4Screen(
                                LARGURA_TELA, ALTURA_TELA, self.jogador_atual, salvar_jogadores, self.jogadores
                            )
                        
                        elif proximo_estado == "RANKING":
                             self.telas["RANKING"] = RankingScreen(LARGURA_TELA, ALTURA_TELA, self.jogador_atual)
                        
                        elif proximo_estado == "DESAFIOS_EXTRAS":
                             self.telas["DESAFIOS_EXTRAS"] = DesafiosExtrasScreen(
                                LARGURA_TELA, ALTURA_TELA, self.jogador_atual, salvar_jogadores, self.jogadores
                            )
                        
                        elif proximo_estado == "REWARD": # Instanciação do Reward Screen
                            fase_id, nivel_idx = jogador_obj
                            self.telas["REWARD"] = RewardScreen(
                                LARGURA_TELA, ALTURA_TELA, 
                                self.jogador_atual, fase_id, nivel_idx,
                                fase_id == 4 and nivel_idx == 2
                            )
                        
                        elif proximo_estado == "LOGOUT":
                            self.jogador_atual = None
                            proximo_estado = "MENU_INICIAL_AUTH" 
                            # Limpar slots de telas para liberar memória
                            self.telas["MENU_PRINCIPAL"] = None
                            self.telas["MENU_JOGADORES"] = None
                            self.telas["ATUALIZAR_JOGADOR"] = None
                            self.telas["TUTORIAL"] = None
                            self.telas["TESTE_NIVEL"] = None
                            self.telas["FASE_1"] = None
                            self.telas["FASE_2"] = None
                            self.telas["FASE_3"] = None
                            self.telas["FASE_4"] = None
                            self.telas["RANKING"] = None
                            self.telas["DESAFIOS_EXTRAS"] = None
                            self.telas["REWARD"] = None


                        self.estado_atual = proximo_estado
                        print(f"Mudando para o estado: {proximo_estado}")

    def atualizar(self):
        if self.estado_atual in self.telas and self.telas[self.estado_atual] is not None:
            self.telas[self.estado_atual].atualizar()

    def desenhar(self):
        self.tela.fill(PRETO)

        if self.estado_atual in self.telas and self.telas[self.estado_atual] is not None:
            self.telas[self.estado_atual].desenhar(self.tela)

        pygame.display.flip()

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