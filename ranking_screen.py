# ranking_screen.py

import pygame
import os
from typing import Dict, Any, List, Optional, Tuple
from player import Jogador
from utils import carregar_jogadores 

# ----------------------------------------------------
# DEFINIÇÕES LOCAIS
# ----------------------------------------------------
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
PIXEL_FONT_PATH = os.path.join(ASSETS_DIR, "PressStart2P-Regular.ttf") 

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL_NEON = (0, 255, 255)
AMARELO_RANKING = (255, 255, 0) 
ROSA_NEON = (255, 20, 147)
LARANJA = (255, 165, 0)

class RankingScreen:
    def __init__(self, largura: int, altura: int, jogador: Any):
        self.largura = largura
        self.altura = altura
        self.jogador = jogador # Jogador logado (para destaque)
        
        try:
            self.fonte_padrao = pygame.font.Font(PIXEL_FONT_PATH, 16)
            self.fonte_titulo = pygame.font.Font(PIXEL_FONT_PATH, 24)
        except Exception:
            self.fonte_padrao = pygame.font.Font(None, 24) 
            self.fonte_titulo = pygame.font.Font(None, 32)
        
        self.ranking_list = self._gerar_ranking_list()
        
        # Fundo
        try:
            caminho_fundo = os.path.join(ASSETS_DIR, "fundomenuprincipal.jpeg") 
            self.fundo = pygame.image.load(caminho_fundo).convert()
            self.fundo = pygame.transform.scale(self.fundo, (largura, altura))
        except pygame.error:
            self.fundo = None
            
        # Botão Voltar (Fixo)
        w_btn, h_btn = 150, 40
        x_center = largura // 2
        self.botao_voltar_rect = pygame.Rect(x_center - w_btn // 2, altura - 70, w_btn, h_btn)


    def _gerar_ranking_list(self) -> List[Tuple[str, int]]:
        """Carrega todos os jogadores e ordena por XP (descendente)."""
        jogadores = carregar_jogadores()

        if not jogadores:
            return []

        ranking = []
        for nome, dados in jogadores.items():
            xp = dados.get("xp", 0) 
            ranking.append((nome, xp))

        # Ordenação: key=xp, reverse=True
        ranking.sort(key=lambda x: x[1], reverse=True)
        return ranking

    def lidar_com_eventos(self, event) -> Optional[Tuple[str, Optional[Jogador]]]:
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            # Botão Voltar
            if self.botao_voltar_rect.collidepoint(mouse_pos):
                # Retorna ao Menu de Jogadores
                return ("MENU_JOGADORES", self.jogador)
        return None

    def atualizar(self):
        pass

    def desenhar(self, tela):
        # 1. Desenhar o Fundo
        if self.fundo:
            tela.blit(self.fundo, (0, 0))
        else:
            tela.fill(PRETO)

        # 2. Título
        texto_titulo = self.fonte_titulo.render("RANKING DE JOGADORES", True, LARANJA)
        tela.blit(texto_titulo, (self.largura // 2 - texto_titulo.get_width() // 2, 30))
        
        # 3. Desenhar a Lista de Ranking
        if not self.ranking_list:
            texto_vazio = self.fonte_padrao.render("Nenhum jogador cadastrado.", True, BRANCO)
            tela.blit(texto_vazio, (self.largura // 2 - texto_vazio.get_width() // 2, 150))
            
        else:
            y_pos = 100
            x_left = self.largura // 2 - 150 # Coluna Nome
            x_right = self.largura // 2 + 50 # Coluna XP
            
            for pos, (nome, xp) in enumerate(self.ranking_list, 1):
                is_current_player = (nome == self.jogador.nome.upper())
                
                # Cor: Amarelo para o Top 3, Rosa para o jogador atual
                if pos <= 3:
                    cor_texto = AMARELO_RANKING
                elif is_current_player:
                    cor_texto = ROSA_NEON
                else:
                    cor_texto = BRANCO

                texto_rank = self.fonte_padrao.render(f"{pos}.", True, cor_texto)
                texto_nome = self.fonte_padrao.render(nome, True, cor_texto)
                texto_xp = self.fonte_padrao.render(f"{xp} XP", True, cor_texto)
                
                # Desenhar Posição, Nome e XP
                tela.blit(texto_rank, (x_left - 30, y_pos))
                tela.blit(texto_nome, (x_left, y_pos))
                tela.blit(texto_xp, (x_right, y_pos))
                
                y_pos += 30 # Espaçamento entre linhas

        # 4. Desenhar Botão Voltar
        pygame.draw.rect(tela, AZUL_NEON, self.botao_voltar_rect)
        texto_voltar = self.fonte_padrao.render("VOLTAR", True, PRETO)
        
        text_x = self.botao_voltar_rect.x + (self.botao_voltar_rect.width - texto_voltar.get_width()) // 2
        text_y = self.botao_voltar_rect.y + 5
        tela.blit(texto_voltar, (text_x, text_y))


