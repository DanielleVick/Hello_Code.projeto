# menuinicial_auth.py (COMPLETO COM RÓTULOS EXTERNOS)

import pygame
import os
from auth import Auth
from typing import Dict, Any, Optional, Tuple 
from screens import InputBox, CINZENTO, VERDE_NEON, ROSA_NEON, AZUL_NEON, BRANCO, PRETO 

# ----------------------------------------------------
# DEFINIÇÕES LOCAIS (Para evitar importação circular)
# ----------------------------------------------------
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
PIXEL_FONT_PATH = os.path.join(ASSETS_DIR, "PressStart2P-Regular.ttf") 

# Cores e Constantes locais
BRANCO = (255, 255, 255) 
PRETO = (0, 0, 0) 

# 🌟 CONSTANTES DE LAYOUT: Novo alinhamento
W_INPUT = 250 
W_LABEL = 150 
GAP = 15      
W_TOTAL = W_INPUT + W_LABEL + GAP

class MenuInicialAuth:
    """Tela para Login e Cadastro."""
    def __init__(self, largura, altura, auth_manager: Auth, carregar_jogadores, salvar_jogadores):
        self.largura = largura
        self.altura = altura
        self.auth = auth_manager
        self.carregar_jogadores = carregar_jogadores
        self.salvar_jogadores = salvar_jogadores
        
        self.fonte_padrao = pygame.font.Font(PIXEL_FONT_PATH, 20)
        self.fonte_label = pygame.font.Font(PIXEL_FONT_PATH, 16) # Fonte menor para rótulo
        
        self.estado_auth = "LOGIN" 

        # 1. Campos de Input (Centralizados como grupo)
        x_center = largura // 2
        y_start = altura // 2 - 120 
        
        # Posição X de Início do Rótulo
        self.X_LEFT = x_center - W_TOTAL // 2 
        # Posição X de Início da Caixa de Input
        X_INPUT_START = self.X_LEFT + W_LABEL + GAP 

        self.input_usuario = InputBox(X_INPUT_START, y_start, W_INPUT, 32, 'USUÁRIO:')
        self.input_senha = InputBox(X_INPUT_START, y_start + 50, W_INPUT, 32, 'SENHA:')
        self.input_senha.is_password = True
        
        self.input_data_nasc = InputBox(X_INPUT_START, y_start + 100, W_INPUT, 32, 'DATA NASC.:')
        
        self.input_boxes = [self.input_usuario, self.input_senha]

        # 3. Botões 
        btn_y = y_start + 150 
        self.botao_acao_rect = pygame.Rect(self.X_LEFT, btn_y, W_TOTAL, 40) 
        self.botao_switch_rect = pygame.Rect(self.X_LEFT, btn_y + 50, W_TOTAL, 30)
        self.botao_sair_rect = pygame.Rect(x_center - 50, altura - 50, 100, 30)

        # 4. Mensagem de feedback
        self.mensagem = ""
        self.mensagem_timer = 0
        self.mensagem_cor = ROSA_NEON
        
        # 5. Fundo
        try:
            assets_dir = os.path.join(os.path.dirname(__file__), "assets")
            caminho_fundo = os.path.join(assets_dir, "teladefundo.png") 
            self.fundo = pygame.image.load(caminho_fundo).convert()
            self.fundo = pygame.transform.scale(self.fundo, (largura, altura))
        except pygame.error as e:
            print(f"Aviso: Erro ao carregar fundo da tela Auth: {e}")
            self.fundo = None

    def _display_message(self, texto, cor_rgb):
        self.mensagem = texto
        self.mensagem_cor = cor_rgb
        self.mensagem_timer = 180 

    def _tentar_login(self) -> Tuple[Optional[str], Optional[Any]]:
        usuario = self.input_usuario.get_text().strip().upper()
        senha = self.input_senha.get_text().strip()
        jogador = self.auth.login_gui(usuario, senha)
        
        if jogador:
            self._display_message("Login bem-sucedido!", VERDE_NEON)
            return ("MENU_JOGADORES", jogador) 
        else:
            self._display_message("Usuário ou senha incorretos.", ROSA_NEON)
            return (None, None)

    def _tentar_cadastro(self) -> Tuple[Optional[str], Optional[Any]]:
        usuario = self.input_usuario.get_text().strip().upper()
        senha = self.input_senha.get_text().strip()
        data_nasc = self.input_data_nasc.get_text().strip()
        
        if not self.auth.validar_senha(senha):
            self._display_message("Senha inválida!", ROSA_NEON)
            return (None, None)
        
        if not self.auth.validar_data_nascimento(data_nasc):
            self._display_message("Data inválida! DD/MM/AAAA", ROSA_NEON)
            return (None, None)
            
        if self.auth.cadastro_gui(usuario, senha, data_nasc):
            self._display_message("Cadastro efetuado! Faça login.", AZUL_NEON)
            self.estado_auth = "LOGIN"
            self.auth.jogadores = self.carregar_jogadores()
            return (None, None)
        else:
             self._display_message("Nome de usuário já existe.", ROSA_NEON)
             return (None, None)

    def lidar_com_eventos(self, event) -> Tuple[Optional[str], Optional[Any]]:
        
        if self.estado_auth == "CADASTRO":
            boxes_ativos = [self.input_usuario, self.input_senha, self.input_data_nasc]
        else:
            boxes_ativos = [self.input_usuario, self.input_senha]

        for box in boxes_ativos:
            box_result = box.handle_event(event)
            if box_result is not None:
                if self.estado_auth == "LOGIN":
                    return self._tentar_login()
                elif self.estado_auth == "CADASTRO":
                    return self._tentar_cadastro()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            if self.botao_acao_rect.collidepoint(mouse_pos):
                if self.estado_auth == "LOGIN":
                    return self._tentar_login()
                elif self.estado_auth == "CADASTRO":
                    return self._tentar_cadastro()

            elif self.botao_switch_rect.collidepoint(mouse_pos):
                self.estado_auth = "CADASTRO" if self.estado_auth == "LOGIN" else "LOGIN"
                self.mensagem = "" 

            elif self.botao_sair_rect.collidepoint(mouse_pos):
                return ("QUIT", None)
        
        return (None, None)
        
    def atualizar(self):
        if self.mensagem_timer > 0:
            self.mensagem_timer -= 1
        
    def desenhar(self, tela):
        
        if self.fundo:
            tela.blit(self.fundo, (0, 0))
        else:
            tela.fill(PRETO)
            
        titulo = "LOGIN" if self.estado_auth == "LOGIN" else "CADASTRO"
        texto_titulo = self.fonte_padrao.render(titulo, True, AZUL_NEON)
        tela.blit(texto_titulo, (self.largura // 2 - texto_titulo.get_width() // 2, self.altura // 2 - 150))

        # 2. Desenhar os RÓTULOS e InputBoxes
        boxes_a_desenhar = [self.input_usuario, self.input_senha]
        if self.estado_auth == "CADASTRO":
            boxes_a_desenhar.append(self.input_data_nasc)

        for box in boxes_a_desenhar:
            # 🌟 Desenha o RÓTULO (Label)
            label_render = self.fonte_label.render(box.label_text, True, BRANCO)
            
            # Posição Y centralizada na caixa de input
            label_y = box.rect.y + (box.rect.height - label_render.get_height()) // 2
            
            # Desenha o rótulo (alinhado em self.X_LEFT)
            tela.blit(label_render, (self.X_LEFT, label_y)) 
            
            # Desenha a caixa de Input
            box.draw(tela)

        # 3. Desenhar Botões de Ação
        if self.estado_auth == "LOGIN":
            cor_botao = AZUL_NEON
            pygame.draw.rect(tela, cor_botao, self.botao_acao_rect)
            texto_render = self.fonte_padrao.render("LOGIN", True, PRETO)
        
        elif self.estado_auth == "CADASTRO":
            cor_botao = ROSA_NEON
            pygame.draw.rect(tela, cor_botao, self.botao_acao_rect)
            texto_render = self.fonte_padrao.render("REGISTRAR", True, PRETO)
        
        # Centralizar o texto sobre o retângulo de ação
        text_x = self.botao_acao_rect.x + (self.botao_acao_rect.width - texto_render.get_width()) // 2
        text_y = self.botao_acao_rect.y + (self.botao_acao_rect.height - texto_render.get_height()) // 2
        tela.blit(texto_render, (text_x, text_y))

        # Botão Mudar Modo 
        pygame.draw.rect(tela, CINZENTO, self.botao_switch_rect)
        texto_switch = "Cadastre-se" if self.estado_auth == "LOGIN" else "LOGIN"
        texto_switch_render = self.fonte_padrao.render(texto_switch, True, BRANCO)
        
        text_switch_x = self.botao_switch_rect.x + (self.botao_switch_rect.width - texto_switch_render.get_width()) // 2
        text_switch_y = self.botao_switch_rect.y + (self.botao_switch_rect.height - texto_switch_render.get_height()) // 2
        tela.blit(texto_switch_render, (text_switch_x, text_switch_y))

        # Botão SAIR
        pygame.draw.rect(tela, ROSA_NEON, self.botao_sair_rect)
        texto_sair = self.fonte_padrao.render("Sair", True, PRETO)
        tela.blit(texto_sair, (self.botao_sair_rect.x + 10, self.botao_sair_rect.y + 5))

        # 4. Mensagem de Erro/Sucesso
        if self.mensagem_timer > 0:
            texto_msg = self.fonte_padrao.render(self.mensagem, True, self.mensagem_cor)
            tela.blit(texto_msg, (self.largura // 2 - texto_msg.get_width() // 2, self.altura // 2 + 200))