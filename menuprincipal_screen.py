# menu_principal_screen.py

import pygame
import os
from typing import Dict, Any, List, Optional, Tuple
from player import Jogador 

# ----------------------------------------------------
# DEFINIÇÕES LOCAIS
# ----------------------------------------------------
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
PIXEL_FONT_PATH = os.path.join(ASSETS_DIR, "PressStart2P-Regular.ttf")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZENTO = (100, 100, 100)
AZUL_NEON = (0, 255, 255)
LARANJA = (255, 165, 0)


class MenuPrincipalScreen:
    def __init__(self, largura: int, altura: int, jogador: Jogador, salvar_jogadores, jogadores_dict):
        self.largura = largura
        self.altura = altura
        self.jogador = jogador
        self.salvar_jogadores = salvar_jogadores
        self.jogadores_dict = jogadores_dict

        # Fontes
        self.fonte_padrao = pygame.font.Font(PIXEL_FONT_PATH, 14)
        self.fonte_titulo = pygame.font.Font(PIXEL_FONT_PATH, 24)

        # Fundo
        try:
            caminho_fundo = os.path.join(ASSETS_DIR, "fundomenuprincipal.jpeg")
            self.fundo = pygame.image.load(caminho_fundo).convert()
            self.fundo = pygame.transform.scale(self.fundo, (largura, altura))
        except:
            print("Aviso: fundo não encontrado.")
            self.fundo = None

        # Cadeado
        try:
            cadeado_path = os.path.join(ASSETS_DIR, "cadeado.png")
            self.cadeado_img = pygame.image.load(cadeado_path).convert_alpha()
            self.cadeado_img = pygame.transform.scale(self.cadeado_img, (30, 30))
        except:
            print("Aviso: cadeado não encontrado.")
            self.cadeado_img = None

        # Opções do menu
        self.opcoes = [
            ("TESTE NÍVEL", "TESTE_NIVEL", 150),
            ("TUTORIAL", "TUTORIAL", 190),
            ("FASE 1", "FASE_1", 280),
            ("FASE 2", "FASE_2", 320),
            ("FASE 3", "FASE_3", 360),
            ("FASE 4", "FASE_4", 400),
            ("MINI JOGOS", "DESAFIOS_EXTRAS", 460),
            ("CENA FINAL", "CUTSCENE_FINAL", 500),
            ("SAIR", "QUIT", self.altura - 50)
        ]

        self.botoes = self._criar_botoes()

    # ----------------------------------------------------
    # CRIAR BOTÕES
    # ----------------------------------------------------
    def _criar_botoes(self) -> List[Dict[str, Any]]:
        botoes_list = []
        x_center = self.largura // 2

        for texto, estado, y in self.opcoes:
            w = 250 if estado.startswith("FASE") or estado in ["DESAFIOS_EXTRAS", "CUTSCENE_FINAL"] else 200
            h = 30
            rect = pygame.Rect(x_center - w // 2, y, w, h)

            # -------------------------------
            # LÓGICA DE BLOQUEIO
            # -------------------------------
            if estado == "CUTSCENE_FINAL":
                bloqueado = self.jogador.fase < 4

            elif estado == "DESAFIOS_EXTRAS":
                bloqueado = self.jogador.fase < 4

            elif estado.startswith("FASE"):
                fase_num = int(estado.split("_")[1])
                bloqueado = fase_num > self.jogador.fase

            else:
                bloqueado = False

            botoes_list.append({
                "texto": texto,
                "estado": estado,
                "rect": rect,
                "bloqueado": bloqueado,
                "cor": AZUL_NEON if not bloqueado else CINZENTO
            })

        return botoes_list

    # ----------------------------------------------------
    # EVENTOS
    # ----------------------------------------------------
    def lidar_com_eventos(self, event) -> Optional[Tuple[str, Optional[Jogador]]]:
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            for botao in self.botoes:
                if botao["rect"].collidepoint(mouse_pos):

                    if botao["bloqueado"]:
                        return None

                    if botao["estado"] == "QUIT":
                        return ("QUIT", None)

                    if botao["estado"] == "CUTSCENE_FINAL":
                        return ("CUTSCENE_FINAL", self.jogador)

                    return (botao["estado"], self.jogador)

        return None

    # ----------------------------------------------------
    # ATUALIZAR BOTÕES
    # ----------------------------------------------------
    def atualizar(self):
        self.botoes = self._criar_botoes()

    # ----------------------------------------------------
    # DESENHAR TELA
    # ----------------------------------------------------
    def desenhar(self, tela):
        # Fundo
        if self.fundo:
            tela.blit(self.fundo, (0, 0))
        else:
            tela.fill(PRETO)

        # Título e status
        stats = f"FASE: {self.jogador.fase} | XP: {self.jogador.xp} | CONHECIMENTO: {self.jogador.nivel_conhecimento.upper()}"
        texto_titulo = self.fonte_titulo.render(f"OLÁ, {self.jogador.nome.upper()}!", True, LARANJA)
        texto_stats = self.fonte_padrao.render(stats, True, BRANCO)

        tela.blit(texto_titulo, (self.largura // 2 - texto_titulo.get_width() // 2, 60))
        tela.blit(texto_stats, (self.largura // 2 - texto_stats.get_width() // 2, 100))

        # Botões
        for botao in self.botoes:
            pygame.draw.rect(tela, botao["cor"], botao["rect"])

            texto_render = self.fonte_padrao.render(botao["texto"], True, PRETO)
            text_x = botao["rect"].x + (botao["rect"].width - texto_render.get_width()) // 2
            text_y = botao["rect"].y + (botao["rect"].height - texto_render.get_height()) // 2
            tela.blit(texto_render, (text_x, text_y))

            # Cadeado
            if botao["bloqueado"] and self.cadeado_img:
                pos_x = botao["rect"].right + 5
                pos_y = botao["rect"].y + (botao["rect"].height // 2) - (self.cadeado_img.get_height() // 2)
                tela.blit(self.cadeado_img, (pos_x, pos_y))
