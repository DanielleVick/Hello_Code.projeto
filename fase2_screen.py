import pygame
import os
from typing import Dict, Any, List, Optional, Tuple
from player import Jogador 
from screens import InputBox, CINZENTO, VERDE_NEON, ROSA_NEON, AZUL_NEON, BRANCO, PRETO 
import random 
from utils_audio import play_sound

# ----------------------------------------------------
# DEFINIÇÕES LOCAIS
# ----------------------------------------------------
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
PIXEL_FONT_PATH = os.path.join(ASSETS_DIR, "PressStart2P-Regular.ttf")

# --------------- FUNÇÃO DE QUEBRA AUTOMÁTICA ---------------
def wrap_text(text: str, font: pygame.font.Font, max_width: int) -> List[str]:
    """
    Quebra um texto automaticamente em várias linhas
    para caber dentro da largura definida.
    """
    words = text.split(" ")
    lines = []
    current = ""

    for w in words:
        test = current + w + " "
        if font.size(test)[0] <= max_width:
            current = test
        else:
            lines.append(current.strip())
            current = w + " "
    if current:
        lines.append(current.strip())

    return lines

# --------------- FUNÇÃO PARA DESENHAR TEXTO CENTRALIZADO ---------------
def draw_centered_text(tela, font, text: str, color, center_x, start_y, max_width):
    """
    Desenha texto grande (com quebra automática) CENTRALIZADO.
    """
    linhas = wrap_text(text, font, max_width)
    y = start_y
    for linha in linhas:
        surf = font.render(linha, True, color)
        x = center_x - surf.get_width() // 2
        tela.blit(surf, (x, y))
        y += font.get_linesize()


# ----------------------------------------------------
# CONTEÚDO DA FASE 2 (inalterado)
# ----------------------------------------------------
CHALLENGE_2_1 = {
    "id": 1,
    "titulo": "Nível 1: Laboratório Maluco!",
    "instrucao_bloco_1": "Combine dois frascos usando uma operação matemática para criar uma poção.",
    "instrucao_bloco_2": "Neste laboratório, cada frasco guarda um valor. Assim como misturar ingredientes, um programa usa variáveis para armazenar dados.",
    "frascos": {'A': 5, 'B': 10, 'C': 3},
    "pergunta": "Qual é o resultado da multiplicação de A * B?",
    "resposta_correta": "50",
    "xp": 20
}

CHALLENGE_2_2 = {
    "id": 2,
    "titulo": "Nível 2: Ilha dos Tesouros!",
    "instrucao_bloco_1": "Para achar o tesouro, você precisa calcular o caminho. Em programação, usamos operações para transformar valores e descobrir resultados.",
    "instrucao_bloco_2": "Um símbolo errado… e você fica preso na ilha! Baú 1 tem 8 moedas e Baú 2 tem 5. Qual é o RESTO da divisão de 8 por 5?",
    "baus": {1: 8, 2: 5, 3: 2},
    "pergunta": "8 % 5 = ?",
    "resposta_correta": "3",
    "xp": 20
}

CHALLENGE_2_3 = {
    "id": 3,
    "titulo": "Nível 3: Salão Mágico do Guardião!",
    "instrucao_bloco_1": "O Guardião quer saber se você entende as funções. Quando você envia valores, uma função pensa e devolve uma resposta.",
    "instrucao_bloco_2": "Por exemplo: se somarmos 4 e 6, a função retornaria 10. Agora é a sua vez! Envie os valores 7 e 9 para a função e solucione o resultado.",
    "pergunta": "Resultado da mistura de 7 e 9:",
    "resposta_correta": "16",
    "xp": 20
}

ALL_CHALLENGES_F2 = [CHALLENGE_2_1, CHALLENGE_2_2, CHALLENGE_2_3]


# ----------------------------------------------------
# CLASSE PRINCIPAL — INÍCIO
# ----------------------------------------------------
class Fase2Screen:
    def __init__(self, largura: int, altura: int, jogador: Jogador, salvar_jogadores, jogadores_dict):
        self.largura = largura
        self.altura = altura
        self.jogador = jogador
        self.salvar_jogadores = salvar_jogadores
        self.jogadores_dict = jogadores_dict

        # Fonte
        try:
            self.fonte_padrao = pygame.font.Font(PIXEL_FONT_PATH, 14)
            self.fonte_titulo = pygame.font.Font(PIXEL_FONT_PATH, 20)
        except:
            self.fonte_padrao = pygame.font.Font(None, 20)
            self.fonte_titulo = pygame.font.Font(None, 28)

        # Estado
        self.nivel_atual_idx = 0
        self.desafio_atual = ALL_CHALLENGES_F2[self.nivel_atual_idx]
        self.mensagem = ""
        self.mensagem_cor = ROSA_NEON
        self.desafio_concluido_sucesso = False
        self.fase_concluida = False

        # Fundo
        try:
            bg_path = os.path.join(ASSETS_DIR, "cenario.png")
            self.fundo = pygame.image.load(bg_path).convert()
            self.fundo = pygame.transform.scale(self.fundo, (largura, altura))
        except:
            self.fundo = None

        # Input
        w_input = 350
        x_center = largura // 2
        self.input_resposta = InputBox(
            x_center - w_input // 2,
            440,
            w_input,
            32,
            'DIGITE O RESULTADO...'
        )
        self.input_resposta.color_inactive = AZUL_NEON
        self.input_resposta.color = AZUL_NEON

        # Botões
        w_btn, h_btn = 150, 40
        self.botao_submeter_rect = pygame.Rect(x_center - w_btn - 10, altura - 70, w_btn, h_btn)
        self.botao_proximo_rect = pygame.Rect(x_center + 10, altura - 70, w_btn, h_btn)

    # -------------------------------------------------------------------
    # Atualizar (não utilizado, mas mantido para compatibilidade)
    # -------------------------------------------------------------------
    def atualizar(self):
        pass

    # -------------------------------------------------------------------
    # Adicionar XP e salvar
    # -------------------------------------------------------------------
    def _adicionar_xp_e_salvar(self, xp_ganho):
        self.jogador.xp += xp_ganho
        self.jogadores_dict[self.jogador.nome] = self.jogador.to_dict()
        self.salvar_jogadores(self.jogadores_dict)

    # -------------------------------------------------------------------
    # Salvar progresso ao completar a fase
    # -------------------------------------------------------------------
    def _salvar_progresso(self):
        self.jogadores_dict[self.jogador.nome] = self.jogador.to_dict()
        self.salvar_jogadores(self.jogadores_dict)

    # -------------------------------------------------------------------
    # Avançar nível
    # -------------------------------------------------------------------
    def _avancar_nivel(self):

        # Dar XP após a tela de recompensa
        self._adicionar_xp_e_salvar(self.desafio_atual["xp"])

        self.nivel_atual_idx += 1

        if self.nivel_atual_idx < len(ALL_CHALLENGES_F2):
            self.desafio_atual = ALL_CHALLENGES_F2[self.nivel_atual_idx]
            self.desafio_concluido_sucesso = False
            self.mensagem = f"Nível {self.desafio_atual['id']} desbloqueado!"
            self.input_resposta.text = ""
        else:
            self.fase_concluida = True
            self.jogador.fase = 3
            self._salvar_progresso()

    # -------------------------------------------------------------------
    # Processar resposta do jogador
    # -------------------------------------------------------------------
    def _processar_resposta(self, resposta_usuario: str):

        if self.desafio_concluido_sucesso:
            return

        resposta_usuario = resposta_usuario.strip().upper()
        correto = (resposta_usuario == self.desafio_atual["resposta_correta"].upper())

        if correto:
            self.mensagem = "CORRETO! Desafio concluído!"
            self.mensagem_cor = VERDE_NEON
            play_sound("point")
            self.desafio_concluido_sucesso = True

            # Retorna tela de recompensa
            return ("REWARD", (2, self.nivel_atual_idx))

        else:
            play_sound("error")
            self.mensagem = "Resultado incorreto. Tente novamente."
            self.mensagem_cor = ROSA_NEON

        return None

    # -------------------------------------------------------------------
    # Eventos
    # -------------------------------------------------------------------
    def lidar_com_eventos(self, event):

        res = self.input_resposta.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            # SUBMETER
            if self.botao_submeter_rect.collidepoint(mouse_pos) and not self.desafio_concluido_sucesso:
                result = self._processar_resposta(self.input_resposta.get_text())
                if result:
                    return result

            # PRÓXIMO ou MENU
            elif self.botao_proximo_rect.collidepoint(mouse_pos):
                if self.desafio_concluido_sucesso:
                    if self.fase_concluida:
                        return ("MENU_PRINCIPAL", self.jogador)
                    else:
                        return ("REWARD", (2, self.nivel_atual_idx))
                else:
                    return ("MENU_PRINCIPAL", self.jogador)

        if res is not None and not self.desafio_concluido_sucesso:
            result = self._processar_resposta(res)
            if result:
                return result

        return None
    # -------------------------------------------------------------------
    # Desenhar a tela
    # -------------------------------------------------------------------
    def desenhar(self, tela):

        # Fundo
        if self.fundo:
            tela.blit(self.fundo, (0, 0))
        else:
            tela.fill(PRETO)

        center_x = self.largura // 2

        # -------------------------------
        # TÍTULO (centralizado)
        # -------------------------------
        titulo = self.desafio_atual["titulo"]
        draw_centered_text(
            tela,
            self.fonte_titulo,
            titulo,
            ROSA_NEON,
            center_x,
            30,
            560
        )

        # -------------------------------
        # INSTRUÇÃO BLOCO 1
        # -------------------------------
        draw_centered_text(
            tela,
            self.fonte_padrao,
            self.desafio_atual["instrucao_bloco_1"],
            AZUL_NEON,
            center_x,
            90,
            560
        )

        # -------------------------------
        # INSTRUÇÃO BLOCO 2
        # -------------------------------
        draw_centered_text(
            tela,
            self.fonte_padrao,
            self.desafio_atual["instrucao_bloco_2"],
            BRANCO,
            center_x,
            140,
            560
        )

        # -------------------------------
        # LISTA DE ITENS (FRASCOS OU BAÚS)
        # -------------------------------
        y_dados = 220

        if "frascos" in self.desafio_atual:
            # calculamos largura máxima do bloco
            elementos = [f"FRASCO {k}: {v}" for k, v in self.desafio_atual["frascos"].items()]

            bloco_largura = max(self.fonte_padrao.size(txt)[0] for txt in elementos)
            bloco_x = center_x - bloco_largura // 2

            for txt in elementos:
                surf = self.fonte_padrao.render(txt, True, BRANCO)
                tela.blit(surf, (center_x - surf.get_width() // 2, y_dados))
                y_dados += self.fonte_padrao.get_linesize()

        elif "baus" in self.desafio_atual:
            elementos = [f"BAÚ {b}: {v} MOEDAS" for b, v in self.desafio_atual["baus"].items()]

            for txt in elementos:
                surf = self.fonte_padrao.render(txt, True, BRANCO)
                tela.blit(surf, (center_x - surf.get_width() // 2, y_dados))
                y_dados += self.fonte_padrao.get_linesize()

        # -------------------------------
        # PERGUNTA CENTRALIZADA
        # -------------------------------
        draw_centered_text(
            tela,
            self.fonte_titulo,
            self.desafio_atual["pergunta"],
            ROSA_NEON,
            center_x,
            350,
            560
        )

        # -------------------------------
        # INPUT
        # -------------------------------
        input_bg_rect = self.input_resposta.rect.inflate(10, 10)
        pygame.draw.rect(tela, (30, 30, 30), input_bg_rect, 0, 5)
        self.input_resposta.draw(tela)

        # -------------------------------
        # MENSAGEM DE FEEDBACK (centralizada)
        # -------------------------------
        if self.mensagem:
            draw_centered_text(
                tela,
                self.fonte_padrao,
                self.mensagem,
                self.mensagem_cor,
                center_x,
                500,
                560
            )
        # -------------------------------
        # BOTÕES
        # -------------------------------

        # Botão SUBMETER
        cor_submeter = VERDE_NEON if not self.desafio_concluido_sucesso else CINZENTO
        pygame.draw.rect(tela, cor_submeter, self.botao_submeter_rect, border_radius=6)

        texto_submeter = self.fonte_padrao.render("SUBMETER", True, PRETO)
        tela.blit(
            texto_submeter,
            (
                self.botao_submeter_rect.x + (self.botao_submeter_rect.width // 2 - texto_submeter.get_width() // 2),
                self.botao_submeter_rect.y + 8
            )
        )

        # Botão PRÓXIMO / MENU
        if self.desafio_concluido_sucesso:
            label_proximo = "PRÓXIMO" if not self.fase_concluida else "MENU"
            cor_proximo = AZUL_NEON
        else:
            label_proximo = "VOLTAR"
            cor_proximo = ROSA_NEON

        pygame.draw.rect(tela, cor_proximo, self.botao_proximo_rect, border_radius=6)

        texto_proximo = self.fonte_padrao.render(label_proximo, True, PRETO)
        tela.blit(
            texto_proximo,
            (
                self.botao_proximo_rect.x + (self.botao_proximo_rect.width // 2 - texto_proximo.get_width() // 2),
                self.botao_proximo_rect.y + 8
            )
        )
