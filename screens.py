# screens.py (CORRIGIDO PARA O MÉTODO atualizar)

import pygame
import os
from typing import Dict, Any, Tuple

# ----------------------------------------------------
# DEFINIÇÕES LOCAIS (Para evitar importação circular)
# ----------------------------------------------------
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
PIXEL_FONT_PATH = os.path.join(ASSETS_DIR, "PressStart2P-Regular.ttf")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZENTO = (100, 100, 100)
ROSA_NEON = (193, 28, 132)
AZUL_NEON = (0, 255, 255)
VERDE_NEON = (0, 255, 0)
LARANJA = (255, 165, 0)
AMARELO = (255, 222, 33)
BRANCO_FRIO = (234, 246, 255)
AMARELO_NEON = (255, 255, 0)

# ====================================================
# CLASSE InputBox (Campo de Entrada de Texto)
# ====================================================


class InputBox:
    """Campo de texto interativo para Pygame."""

    def __init__(self, x, y, w, h, label=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = CINZENTO
        self.color_active = AZUL_NEON
        self.color = self.color_inactive
        self.text = ''
        self.label_text = label
        self.font = pygame.font.Font(PIXEL_FONT_PATH, 18)
        self.txt_surface = self.font.render(self.text, True, BRANCO)
        self.active = False
        self.is_password = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

                self.txt_surface = self.font.render(
                    self.get_display_text(), True, BRANCO)
        return None

    def get_display_text(self):
        if self.is_password:
            return '*' * len(self.text)
        else:
            return self.text

    # 🌟 CORREÇÃO: Método atualizar adicionado para satisfazer a chamada do gui_main
    def atualizar(self):
        pass

    def draw(self, screen):
        text_to_draw = self.get_display_text()
        color_text = BRANCO

        txt_surface = self.font.render(text_to_draw, True, color_text)

        screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))

        pygame.draw.rect(screen, self.color, self.rect, 2)

        self.rect.w = max(200, self.txt_surface.get_width() + 10)

    def get_text(self):
        return self.text

# ====================================================
# CLASSE StartScreen (Tela Inicial)
# ====================================================


class StartScreen:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura

        try:
            caminho_fundo = os.path.join(ASSETS_DIR, "telainicial.png")
            self.fundo = pygame.image.load(caminho_fundo).convert()
            self.fundo = pygame.transform.scale(self.fundo, (largura, altura))
        except pygame.error:
            self.fundo = None

        pygame.font.init()
        self.fonte_start = pygame.font.Font(PIXEL_FONT_PATH, 24)
        self.pos_start = (largura // 2, altura - 50)
        self.mostrar_start = True
        self.contador_piscar = 0

    def lidar_com_eventos(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return "MENU_INICIAL_AUTH"
        return None

    def atualizar(self):
        self.contador_piscar += 1
        if self.contador_piscar > 30:
            self.mostrar_start = not self.mostrar_start
            self.contador_piscar = 0

    def desenhar(self, tela):
        if self.fundo:
            tela.blit(self.fundo, (0, 0))
        else:
            tela.fill(PRETO)

        if self.mostrar_start:
            texto_start = self.fonte_start.render(
                "Pressione Enter para iniciar", True, BRANCO)
            tela.blit(
                texto_start, (self.pos_start[0] - texto_start.get_width() // 2, self.pos_start[1]))
