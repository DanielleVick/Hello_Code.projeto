# menu_principal_screen.py (FINAL PARA INTEGRAÇÃO DO CADEADO E DESAFIOS EXTRAS)

import pygame
import os
from typing import Dict, Any, List, Optional, Tuple
from player import Jogador 

# ----------------------------------------------------
# DEFINIÇÕES LOCAIS (Para evitar importação circular)
# ----------------------------------------------------
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
PIXEL_FONT_PATH = os.path.join(ASSETS_DIR, "PressStart2P-Regular.ttf") 

# Cores (Mantidas as definições para uso na tela)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZENTO = (100, 100, 100)
ROSA_NEON = (255, 105, 180) 
AZUL_NEON = (0, 255, 255)
LARANJA = (255, 165, 0)
VERDE_NEON = (0, 255, 0)


class MenuPrincipalScreen:
    def __init__(self, largura: int, altura: int, jogador: Jogador, salvar_jogadores, jogadores_dict):
        self.largura = largura
        self.altura = altura
        self.jogador = jogador
        self.salvar_jogadores = salvar_jogadores
        self.jogadores_dict = jogadores_dict
        
        # 1. Fonte e Fundo
        self.fonte_padrao = pygame.font.Font(PIXEL_FONT_PATH, 14)
        self.fonte_titulo = pygame.font.Font(PIXEL_FONT_PATH, 24)
        
        try:
            # 🌟 Fundo do Menu Principal (Certifique-se que o ficheiro é este ou mude o nome)
            caminho_fundo = os.path.join(ASSETS_DIR, "fundomenuprincipal.jpeg") 
            self.fundo = pygame.image.load(caminho_fundo).convert()
            self.fundo = pygame.transform.scale(self.fundo, (largura, altura))
        except pygame.error as e:
            print(f"Aviso: Erro ao carregar fundo do Menu Principal: {e}")
            self.fundo = None
        
        # 🌟 Carregar Cadeado (Como estava no seu código)
        try:
            cadeado_path = os.path.join(ASSETS_DIR, "cadeado.png") 
            self.cadeado_img = pygame.image.load(cadeado_path).convert_alpha() 
            self.cadeado_img = pygame.transform.scale(self.cadeado_img, (30, 30)) 
        except pygame.error:
            print("Aviso: Ícone de cadeado (cadeado.png) não encontrado. Usando apenas texto.")
            self.cadeado_img = None

        # 2. Definição das Opções de Ação
        self.opcoes = [
            ("TESTE NÍVEL", "TESTE_NIVEL", 150),
            ("TUTORIAL", "TUTORIAL", 190),
            ("FASE 1", "FASE_1", 280),
            ("FASE 2", "FASE_2", 320),
            ("FASE 3", "FASE_3", 360),
            ("FASE 4", "FASE_4", 400),
            ("MINI JOGOS", "DESAFIOS_EXTRAS", 460),
            ("SAIR", "QUIT", self.altura - 50) 
        ]
        
        self.botoes = self._criar_botoes()

    def _criar_botoes(self) -> List[Dict[str, Any]]:
        botoes_list = []
        x_center = self.largura // 2
        
        for texto, estado, y in self.opcoes:
            
            w = 250 if estado.startswith("FASE") or estado == "DESAFIOS_EXTRAS" else 200
            h = 30
            rect = pygame.Rect(x_center - w // 2, y, w, h)
            
            # Lógica de Bloqueio
            fase_num = int(estado.split('_')[-1]) if estado.startswith("FASE") else 0
            
            if estado == "DESAFIOS_EXTRAS":
                bloqueado = False 
            else:
                # Bloqueio normal para as fases principais
                bloqueado = fase_num > self.jogador.fase
            
            
            botoes_list.append({
                "texto": texto,
                "estado": estado,
                "rect": rect,
                "bloqueado": bloqueado,
                # Cor: Azul Neon se Desbloqueado, Cinzento se Bloqueado
                "cor": AZUL_NEON if not bloqueado else CINZENTO
            })
        return botoes_list

    def lidar_com_eventos(self, event) -> Optional[Tuple[str, Optional[Jogador]]]:
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            for botao in self.botoes:
                if botao["rect"].collidepoint(mouse_pos):
                    if not botao["bloqueado"]:
                        if botao["estado"] == "QUIT":
                            return ("QUIT", None) 
                        
                        return (botao["estado"], self.jogador)
        return None

    def atualizar(self):
        # Reavalia o estado dos botões (para caso o jogador tenha subido de fase)
        self.botoes = self._criar_botoes()

    def desenhar(self, tela):
        # 1. Desenhar o Fundo
        if self.fundo:
            tela.blit(self.fundo, (0, 0))
        else:
            tela.fill(PRETO)
            
        # 2. Título e Stats do Jogador (topo do ecrã)
        stats = f"FASE: {self.jogador.fase} | XP: {self.jogador.xp} | CONHECIMENTO: {self.jogador.nivel_conhecimento.upper()}"
        
        texto_titulo = self.fonte_titulo.render(f"OLÁ, {self.jogador.nome.upper()}!", True, LARANJA)
        texto_stats = self.fonte_padrao.render(stats, True, BRANCO)

        tela.blit(texto_titulo, (self.largura // 2 - texto_titulo.get_width() // 2, 60))
        tela.blit(texto_stats, (self.largura // 2 - texto_stats.get_width() // 2, 100))
        
        # 3. Desenhar Botões
        for botao in self.botoes:
            
            # Cor do botão (CINZENTO se bloqueado)
            cor_fundo = botao["cor"]
            pygame.draw.rect(tela, cor_fundo, botao["rect"])

            # Desenhar texto
            texto_render = self.fonte_padrao.render(botao["texto"], True, PRETO)
            
            # Centralizar texto no botão
            text_x = botao["rect"].x + (botao["rect"].width - texto_render.get_width()) // 2
            text_y = botao["rect"].y + (botao["rect"].height - texto_render.get_height()) // 2
            tela.blit(texto_render, (text_x, text_y))
            
            # 🌟 Desenhar CADEADO (Para Fases e Desafios Extras Bloqueados)
            if botao["bloqueado"] and self.cadeado_img:
                
                # Posiciona o ícone 5px à direita do botão
                pos_x = botao["rect"].right + 5
                # Centraliza verticalmente
                pos_y = botao["rect"].y + (botao["rect"].height // 2) - (self.cadeado_img.get_height() // 2)
                
                tela.blit(self.cadeado_img, (pos_x, pos_y))