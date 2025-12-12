# teste_nivel_screen.py (COMPLETO E FUNCIONAL)

import pygame
import os
from typing import Dict, Any, List, Optional, Tuple
from player import Jogador 
from screens import CINZENTO, VERDE_NEON, ROSA_NEON, AZUL_NEON, BRANCO, PRETO 

# ----------------------------------------------------
# DEFINIÇÕES LOCAIS (Para evitar importação circular)
# ----------------------------------------------------
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
PIXEL_FONT_PATH = os.path.join(ASSETS_DIR, "PressStart2P-Regular.ttf") 

# ----------------------------------------------------
# CONTEÚDO DO QUIZ
# ----------------------------------------------------
QUIZ_CONTENTS = [
    {
        "id": 1,
        "pergunta": "1) O que é uma variável em programação?",
        "opcoes": ["a) Armazena dados", "b) Um número fixo", "c) Um tipo de loop"], 
        "resposta_correta": "a" 
    },
    {
        "id": 2,
        "pergunta": "2) Qual operador é usado para multiplicação?",
        "opcoes": ["a) +", "b) -", "c) *"],
        "resposta_correta": "c"
    },
    {
        "id": 3,
        "pergunta": "3) O que significa 'if' em Python?",
        "opcoes": ["a) Estrutura de repetição", "b) Estrutura condicional", "c) Declaração de função"],
        "resposta_correta": "b"
    }
]

# ----------------------------------------------------
# CLASSE PRINCIPAL
# ----------------------------------------------------

class TesteNivelScreen:
    def __init__(self, largura: int, altura: int, jogador: Jogador, salvar_jogadores, jogadores_dict):
        self.largura = largura
        self.altura = altura
        self.jogador = jogador
        self.salvar_jogadores = salvar_jogadores
        self.jogadores_dict = jogadores_dict
        
        self.fonte_padrao = pygame.font.Font(PIXEL_FONT_PATH, 16)
        self.fonte_titulo = pygame.font.Font(PIXEL_FONT_PATH, 24)
        
        # 1. Estado do Quiz
        self.pergunta_atual_idx = 0
        self.respostas_usuario = {}
        self.quiz_finalizado = False
        self.score = 0
        self.mensagem = ""

        # 2. Fundo (Usando um cenário genérico)
        try:
            caminho_fundo = os.path.join(ASSETS_DIR, "teladefundo.png") 
            self.fundo = pygame.image.load(caminho_fundo).convert()
            self.fundo = pygame.transform.scale(self.fundo, (largura, altura))
        except pygame.error:
            self.fundo = None
            
        # 3. Definição dos Botões de Resposta (A, B, C)
        self.botoes_opcoes = self._criar_botoes_opcoes()
        
        # 4. Botão Voltar/Continuar (Fixo)
        w_btn, h_btn = 200, 40
        x_center = largura // 2
        self.botao_continuar_rect = pygame.Rect(x_center - w_btn // 2, altura - 70, w_btn, h_btn)


    def _criar_botoes_opcoes(self) -> List[Dict[str, Any]]:
        botoes_list = []
        x_center = self.largura // 2
        y_start = 250
        gap = 50
        w_btn = 300
        
        opcoes_letras = ["a", "b", "c"]
        
        for i, letra in enumerate(opcoes_letras):
            y = y_start + i * gap
            rect = pygame.Rect(x_center - w_btn // 2, y, w_btn, 30)
            
            botoes_list.append({
                "letra": letra,
                "rect": rect,
                "cor": AZUL_NEON 
            })
        return botoes_list

    def _salvar_nivel(self):
        """Calcula o score final e salva o nível de conhecimento no jogador."""
        self.score = 0
        for q in QUIZ_CONTENTS:
            if self.respostas_usuario.get(q["id"]) == q["resposta_correta"]:
                self.score += 1
        
        nivel_resultado = "Iniciante"
        if self.score == 3:
            nivel_resultado = "Avançado"
        elif self.score == 2:
            nivel_resultado = "Intermediário"

        self.jogador.nivel_conhecimento = nivel_resultado
        
        # Persistência de dados
        self.jogadores_dict[self.jogador.nome] = self.jogador.to_dict()
        self.salvar_jogadores(self.jogadores_dict)
        
        self.mensagem = f"Teste Finalizado! Nível: {nivel_resultado} ({self.score}/3)"

    def lidar_com_eventos(self, event) -> Optional[Tuple[str, Optional[Jogador]]]:
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            # 1. Botões de Resposta (Se o quiz não estiver finalizado)
            if not self.quiz_finalizado:
                for botao in self.botoes_opcoes:
                    if botao["rect"].collidepoint(mouse_pos):
                        q_data = QUIZ_CONTENTS[self.pergunta_atual_idx]
                        q_id = q_data["id"]
                        self.respostas_usuario[q_id] = botao["letra"]
                        
                        # Avança para a próxima pergunta ou finaliza
                        if self.pergunta_atual_idx + 1 < len(QUIZ_CONTENTS):
                            self.pergunta_atual_idx += 1
                        else:
                            self._salvar_nivel()
                            self.quiz_finalizado = True
                        return None
            
            # 2. Botão Continuar/Voltar
            if self.botao_continuar_rect.collidepoint(mouse_pos):
                if self.quiz_finalizado:
                    # Retorna ao Menu Principal após finalizar e salvar
                    return ("MENU_PRINCIPAL", self.jogador)
                
        return None

    def atualizar(self):
        # Lógica de atualização (Ex: piscar mensagem)
        pass

    def desenhar(self, tela):
        # 1. Desenhar o Fundo
        if self.fundo:
            tela.blit(self.fundo, (0, 0))
        else:
            tela.fill(PRETO)

        # Título
        texto_titulo = self.fonte_titulo.render("TESTE DE NÍVEL DE CONHECIMENTO", True, ROSA_NEON)
        tela.blit(texto_titulo, (self.largura // 2 - texto_titulo.get_width() // 2, 50))

        if not self.quiz_finalizado:
            
            # Desenhar Pergunta Atual
            q_data = QUIZ_CONTENTS[self.pergunta_atual_idx]
            texto_pergunta = self.fonte_padrao.render(q_data["pergunta"], True, BRANCO)
            tela.blit(texto_pergunta, (self.largura // 2 - texto_pergunta.get_width() // 2, 150))
            
            # Desenhar Opções e Botões
            for i, botao in enumerate(self.botoes_opcoes):
                # Cor do botão de opção
                cor_fundo = AZUL_NEON 
                pygame.draw.rect(tela, cor_fundo, botao["rect"])

                # Desenhar o texto da opção
                texto_opcao = self.fonte_padrao.render(q_data["opcoes"][i], True, PRETO)
                tela.blit(texto_opcao, (botao["rect"].x + 10, botao["rect"].y + 5))

            # Texto do Botão Continuar
            texto_continuar = self.fonte_padrao.render("PRÓXIMA", True, PRETO)
            pygame.draw.rect(tela, VERDE_NEON, self.botao_continuar_rect)
            
        else:
            # Estado Finalizado
            texto_final = self.fonte_titulo.render("TESTE FINALIZADO!", True, VERDE_NEON)
            texto_resultado = self.fonte_padrao.render(self.mensagem, True, BRANCO)
            
            tela.blit(texto_final, (self.largura // 2 - texto_final.get_width() // 2, 200))
            tela.blit(texto_resultado, (self.largura // 2 - texto_resultado.get_width() // 2, 250))
            
            # Texto do Botão (Voltar)
            texto_continuar = self.fonte_padrao.render("MENU PRINCIPAL", True, PRETO)
            pygame.draw.rect(tela, ROSA_NEON, self.botao_continuar_rect)

        # Centralizar o texto do botão
        text_x = self.botao_continuar_rect.x + (self.botao_continuar_rect.width - texto_continuar.get_width()) // 2
        text_y = self.botao_continuar_rect.y + 5
        tela.blit(texto_continuar, (text_x, text_y))