# menujogadores_screen.py (LAYOUT VERTICAL CORRIGIDO)

import pygame
import os
from typing import Dict, Any, Optional, Tuple, List
from player import Jogador 
from screens import InputBox, CINZENTO, VERDE_NEON, ROSA_NEON, AZUL_NEON, BRANCO, PRETO, LARANJA
from utils import carregar_jogadores, salvar_jogadores 

# ----------------------------------------------------
# DEFINIÇÕES LOCAIS
# ----------------------------------------------------
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
PIXEL_FONT_PATH = os.path.join(ASSETS_DIR, "PressStart2P-Regular.ttf") 

class MenuJogadoresScreen:
    def __init__(self, largura: int, altura: int, jogador: Jogador, salvar_jogadores, jogadores_dict):
        self.largura = largura
        self.altura = altura
        self.jogador = jogador
        self.salvar_jogadores = salvar_jogadores
        self.jogadores_dict = jogadores_dict
        
        try:
            self.fonte_padrao = pygame.font.Font(PIXEL_FONT_PATH, 16) 
            self.fonte_titulo = pygame.font.Font(PIXEL_FONT_PATH, 24)
        except Exception:
            self.fonte_padrao = pygame.font.Font(None, 24) 
            self.fonte_titulo = pygame.font.Font(None, 32)
        
        # Fundo (Usando um cenário genérico)
        try:
            caminho_fundo = os.path.join(ASSETS_DIR, "fundomenuprincipal.jpeg") 
            self.fundo = pygame.image.load(caminho_fundo).convert()
            self.fundo = pygame.transform.scale(self.fundo, (largura, altura))
        except pygame.error:
            self.fundo = None
            
        # Posições dos botões (Layout Vertical)
        W_BTN_WIDE, H_BTN = 250, 40 # Largura para RANKING e PRINCIPAL
        W_BTN_NARROW = 150 # Largura para SAIR
        GAP = 15
        x_center = largura // 2
        
        # Posição Y inicial para a coluna de botões
        y_start_coluna = 250 
        
        # 🌟 1. Botão RANKING (Topo da coluna)
        self.botao_ranking_rect = pygame.Rect(x_center - W_BTN_WIDE // 2, y_start_coluna, W_BTN_WIDE, H_BTN)

        # 🌟 2. Botão ATUALIZAR JOGADOR
        y_atualizar = y_start_coluna + H_BTN + GAP
        self.botao_atualizar_rect = pygame.Rect(x_center - W_BTN_WIDE // 2, y_atualizar, W_BTN_WIDE, H_BTN)

        # 🌟 3. Botão MENU PRINCIPAL
        y_principal = y_atualizar + H_BTN + GAP
        self.botao_principal_rect = pygame.Rect(x_center - W_BTN_WIDE // 2, y_principal, W_BTN_WIDE, H_BTN)

        # 🌟 4. Botão SAIR (Fundo da Tela, com largura e altura menores)
        self.botao_sair_rect = pygame.Rect(x_center - W_BTN_NARROW // 2, altura - 70, W_BTN_NARROW, H_BTN)


    def lidar_com_eventos(self, event) -> Optional[Tuple[str, Optional[Jogador]]]:
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            # Botão Ranking
            if self.botao_ranking_rect.collidepoint(mouse_pos):
                return ("RANKING", self.jogador)

            # Botão Atualizar Dados (Simulação)
            if self.botao_atualizar_rect.collidepoint(mouse_pos):
                self.jogadores_dict = carregar_jogadores()
                self.jogador.xp = self.jogadores_dict[self.jogador.nome.upper()].get("xp", 0)
                return ("ATUALIZAR_JOGADOR", self.jogador) # Corrigido para ir para a tela ATUALIZAR_JOGADOR

            # Botão Menu Principal
            if self.botao_principal_rect.collidepoint(mouse_pos):
                return ("MENU_PRINCIPAL", self.jogador)

            # Botão Sair / Deslogar
            if self.botao_sair_rect.collidepoint(mouse_pos):
                return ("MENU_INICIAL_AUTH", None) 

        return None

    def atualizar(self):
        pass

    def desenhar(self, tela):
        if self.fundo:
            tela.blit(self.fundo, (0, 0))
        else:
            tela.fill(PRETO)

        # 1. Título
        texto_titulo = self.fonte_titulo.render("MENU DO JOGADOR", True, LARANJA)
        tela.blit(texto_titulo, (self.largura // 2 - texto_titulo.get_width() // 2, 30))

        # 2. Informações do Jogador
        info_y = 100
        texto_nome = self.fonte_padrao.render(f"JOGADOR: {self.jogador.nome.upper()}", True, BRANCO)
        texto_xp = self.fonte_padrao.render(f"XP TOTAL: {self.jogador.xp}", True, VERDE_NEON)
        texto_fase = self.fonte_padrao.render(f"FASE LIBERADA: {self.jogador.fase}", True, VERDE_NEON)

        x_start = self.largura // 2 - 150
        
        tela.blit(texto_nome, (x_start, info_y))
        tela.blit(texto_xp, (x_start, info_y + 30))
        tela.blit(texto_fase, (x_start, info_y + 60))

        # 3. Desenhar Botões na Coluna
        
        botoes_base = [
            (self.botao_ranking_rect, "VER RANKING", VERDE_NEON),
            (self.botao_atualizar_rect, "ATUALIZAR DADOS", CINZENTO),
            (self.botao_principal_rect, "MENU PRINCIPAL", AZUL_NEON),
            (self.botao_sair_rect, "SAIR", ROSA_NEON) # SAIR é o botão final e menor
        ]
        
        for rect, text_label, color in botoes_base:
            pygame.draw.rect(tela, color, rect)
            
            # Ajuste de Fonte para o Botão SAIR (se necessário, mas o tamanho 16 deve funcionar)
            fonte_btn = self.fonte_padrao
            
            texto_render = fonte_btn.render(text_label, True, PRETO)
            
            # Centralizar texto no botão
            text_x = rect.x + (rect.width - texto_render.get_width()) // 2
            text_y = rect.y + (rect.height - texto_render.get_height()) // 2
            tela.blit(texto_render, (text_x, text_y))