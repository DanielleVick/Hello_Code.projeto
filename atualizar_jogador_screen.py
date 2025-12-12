# atualizar_jogador_screen.py (COMPLETO COM RÓTULOS EXTERNOS)

import pygame
import os
from typing import Dict, Any, Optional, Tuple
from player import Jogador 
from screens import InputBox, CINZENTO, VERDE_NEON, ROSA_NEON, AZUL_NEON, BRANCO, PRETO
from auth import Auth 

# ----------------------------------------------------
# DEFINIÇÕES LOCAIS
# ----------------------------------------------------
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
PIXEL_FONT_PATH = os.path.join(ASSETS_DIR, "PressStart2P-Regular.ttf") 

# Constantes de Layout 
W_INPUT = 300 
W_LABEL = 150 
GAP = 15      
W_TOTAL = W_INPUT + W_LABEL + GAP

class AtualizarJogadorScreen:
    def __init__(self, largura: int, altura: int, jogador: Jogador, auth_manager: Auth, salvar_jogadores, jogadores_dict):
        self.largura = largura
        self.altura = altura
        self.jogador = jogador
        self.auth = auth_manager
        self.salvar_jogadores = salvar_jogadores
        self.jogadores_dict = jogadores_dict
        
        # 1. Fonte e Fundo
        self.fonte_padrao = pygame.font.Font(PIXEL_FONT_PATH, 18)
        self.fonte_titulo = pygame.font.Font(PIXEL_FONT_PATH, 24)
        self.fonte_label = pygame.font.Font(PIXEL_FONT_PATH, 16)
        
        try:
            caminho_fundo = os.path.join(ASSETS_DIR, "teladefundo.png") 
            self.fundo = pygame.image.load(caminho_fundo).convert()
            self.fundo = pygame.transform.scale(self.fundo, (largura, altura))
        except pygame.error:
            self.fundo = None
            
        # 2. Campos de Input (Centralizados como grupo)
        self.x_center = largura // 2
        self.y_start = altura // 2 - 120 
        
        # Posição X de Início do Rótulo
        self.X_LEFT = self.x_center - W_TOTAL // 2 
        # Posição X de Início da Caixa de Input
        X_INPUT_START = self.X_LEFT + W_LABEL + GAP 

        self.input_novo_nome = InputBox(X_INPUT_START, self.y_start, W_INPUT, 32, 'NOVO NOME')
        self.input_nova_senha = InputBox(X_INPUT_START, self.y_start + 50, W_INPUT, 32, 'NOVA SENHA')
        self.input_nova_senha.is_password = True
        self.input_nova_data = InputBox(X_INPUT_START, self.y_start + 100, W_INPUT, 32, 'NOVA DATA')
        
        self.input_boxes = [self.input_novo_nome, self.input_nova_senha, self.input_nova_data]

        # 3. Botões
        w_btn, h_btn = 150, 40
        btn_y = self.y_start + 170 
        
        self.botao_salvar_rect = pygame.Rect(self.x_center - w_btn - 10, btn_y, w_btn, h_btn)
        self.botao_voltar_rect = pygame.Rect(self.x_center + 10, btn_y, w_btn, h_btn)
        
        # 4. Mensagem de feedback
        self.mensagem = ""
        self.mensagem_timer = 0
        self.mensagem_cor = ROSA_NEON

    # ... (Métodos de lógica _display_message, _tentar_atualizar, lidar_com_eventos, atualizar mantidos) ...

    def _display_message(self, texto, cor_rgb):
        self.mensagem = texto
        self.mensagem_cor = cor_rgb
        self.mensagem_timer = 180 

    def _tentar_atualizar(self):
        novo_nome = self.input_novo_nome.get_text().strip().upper()
        nova_senha = self.input_nova_senha.get_text().strip()
        nova_data = self.input_nova_data.get_text().strip()
        
        novos_dados = {}
        dados_alterados = False
        
        # 1. Validar e processar NOVO NOME
        if novo_nome and novo_nome != self.jogador.nome.upper():
            if novo_nome in self.jogadores_dict:
                self._display_message(f"Nome '{novo_nome}' já está em uso.", ROSA_NEON)
                return False
            novos_dados["nome"] = novo_nome 
            dados_alterados = True

        # 2. Validar e adicionar Nova Senha
        if nova_senha:
            if not self.auth.validar_senha(nova_senha):
                self._display_message("Senha inválida! (6-10 chars, Maiúscula, Especial)", ROSA_NEON)
                return False
            novos_dados["senha"] = nova_senha
            dados_alterados = True

        # 3. Validar e adicionar Nova Data
        if nova_data:
            if not self.auth.validar_data_nascimento(nova_data):
                self._display_message("Data inválida! Use DD/MM/AAAA.", ROSA_NEON)
                return False
            novos_dados["data_nascimento"] = nova_data
            dados_alterados = True
        
        # 4. Processamento Final e Persistência
        if dados_alterados:
            
            if "nome" in novos_dados:
                dados_antigos = self.jogador.to_dict()
                dados_antigos.update(novos_dados) 
                
                del self.jogadores_dict[self.jogador.nome.upper()] 
                self.jogadores_dict[novo_nome] = dados_antigos
                
                self.jogador.nome = novo_nome 
                
            else:
                self.auth.atualizar(self.jogador.nome, novos_dados)
                
            self.salvar_jogadores(self.jogadores_dict)
            
            self._display_message("Dados atualizados com sucesso!", VERDE_NEON)
            return True
            
        else:
            self._display_message("Nenhum dado novo fornecido.", CINZENTO)
            return True 

    def lidar_com_eventos(self, event):
        for box in self.input_boxes:
            box.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            if self.botao_salvar_rect.collidepoint(mouse_pos):
                if self._tentar_atualizar():
                    self.input_novo_nome.text = ""
                    self.input_nova_senha.text = ""
                    self.input_nova_data.text = ""
                    
            elif self.botao_voltar_rect.collidepoint(mouse_pos):
                return ("MENU_JOGADORES", self.jogador) 

        return None

    def atualizar(self):
        if self.mensagem_timer > 0:
            self.mensagem_timer -= 1

    def desenhar(self, tela):
        # 1. Desenhar o Fundo
        if self.fundo:
            tela.blit(self.fundo, (0, 0))
        else:
            tela.fill(PRETO)

        # Título
        texto_titulo = self.fonte_titulo.render("ATUALIZAR DADOS", True, AZUL_NEON)
        tela.blit(texto_titulo, (self.largura // 2 - texto_titulo.get_width() // 2, 50))
        
        # Nome do Jogador Atual (referência)
        texto_nome_atual = self.fonte_padrao.render(f"Logado como: {self.jogador.nome.upper()}", True, ROSA_NEON)
        tela.blit(texto_nome_atual, (self.largura // 2 - texto_nome_atual.get_width() // 2, 120))

        # 2. Desenhar os RÓTULOS e InputBoxes
        
        for box in self.input_boxes:
            # 🌟 Desenha o RÓTULO (Label)
            label_render = self.fonte_label.render(box.label_text, True, BRANCO)
            
            # Posição Y centralizada na caixa de input
            label_y = box.rect.y + (box.rect.height - label_render.get_height()) // 2
            
            # Desenha o rótulo (alinhado em self.X_LEFT)
            tela.blit(label_render, (self.X_LEFT, label_y)) 
            
            # Desenha a caixa de Input
            box.draw(tela)

        # 3. Desenhar Botões
        pygame.draw.rect(tela, VERDE_NEON, self.botao_salvar_rect)
        texto_salvar = self.fonte_padrao.render("SALVAR", True, PRETO)
        tela.blit(texto_salvar, (self.botao_salvar_rect.x + 20, self.botao_salvar_rect.y + 10))

        pygame.draw.rect(tela, CINZENTO, self.botao_voltar_rect)
        texto_voltar = self.fonte_padrao.render("VOLTAR", True, BRANCO)
        tela.blit(texto_voltar, (self.botao_voltar_rect.x + 20, self.botao_voltar_rect.y + 10))

        # 4. Mensagem de Feedback
        if self.mensagem_timer > 0:
            texto_msg = self.fonte_padrao.render(self.mensagem, True, self.mensagem_cor)
            tela.blit(texto_msg, (self.largura // 2 - texto_msg.get_width() // 2, self.altura // 2 + 150))