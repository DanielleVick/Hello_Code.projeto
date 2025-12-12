# desafios_extras_screen.py
import pygame
import os
import random
from typing import List
from player import Jogador
from screens import InputBox, CINZENTO, VERDE_NEON, ROSA_NEON, AZUL_NEON, BRANCO, PRETO


def wrap_text(text: str, font: pygame.font.Font, max_width: int):
    words = text.split(" ")
    lines = []
    current = ""
    for w in words:
        test = current + (" " if current else "") + w
        if font.size(test)[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
PIXEL_FONT_PATH = os.path.join(ASSETS_DIR, "PressStart2P-Regular.ttf")

CHALLENGE_EXTRA_1 = {
    "id": 1,
    "titulo": "Extra: Pedra, Papel e Tesoura!",
    "instrucao_introducao": [
        "Em programação, podemos criar jogos simples usando condicionais e loops.",
        "Vamos jogar Pedra, Papel e Tesoura contra o computador!",

    ],
    "instrucao_final": [
        "Agora, vamos aprender como criar um jogo de Pedra, Papel e Tesoura!",
        "Passo 1: Importe o módulo random para escolhas aleatórias. Exemplo: import random",
        "Passo 2: Defina uma lista de opções válidas. Exemplo: opcoes = ['pedra', 'papel', 'tesoura']",
        "Passo 3: Peça a entrada do jogador e valide. Exemplo: jogador = input('Escolha: ').lower()",
        "Passo 4: Gere a escolha do computador. Exemplo: computador = random.choice(opcoes)",
        "Passo 5: Use condicionais para determinar o vencedor. Exemplo: if jogador == computador: empate",
        "Passo 6: Pratique criando seu próprio jogo com essas regras!"
    ],
    "xp": 20
}

ALL_CHALLENGES_EXTRAS = [CHALLENGE_EXTRA_1]


class DesafiosExtrasScreen:
    def __init__(self, largura: int, altura: int, jogador: Jogador, salvar_jogadores, jogadores_dict):
        self.largura = largura
        self.altura = altura
        self.jogador = jogador
        self.salvar_jogadores = salvar_jogadores
        self.jogadores_dict = jogadores_dict
        # marca que o jogador já fez uma jogada (usado para mostrar instruções finais)
        self.jogada_realizada = False

        try:
            self.fonte_padrao = pygame.font.Font(PIXEL_FONT_PATH, 14)
            self.fonte_titulo = pygame.font.Font(PIXEL_FONT_PATH, 24)
        except Exception:
            self.fonte_padrao = pygame.font.Font(None, 24)
            self.fonte_titulo = pygame.font.Font(None, 32)

        self.desafio_atual = ALL_CHALLENGES_EXTRAS[0]
        self.sub_estado = "INSTRUCOES"  # INSTRUCOES -> JOGAR -> FINALIZADO
        self.feedback_jogo: List[str] = []
        self.fase_concluida = False

        # Input
        w_input = 350
        x_center = largura // 2
        self.input_resposta = InputBox(
            x_center -
            w_input // 2, 440, w_input, 32, 'Digite (pedra/papel/tesoura):'
        )
        self.input_resposta.color_inactive = AZUL_NEON
        self.input_resposta.color = AZUL_NEON

        # Botões
        w_btn, h_btn = 150, 40
        self.botao_submeter_rect = pygame.Rect(
            x_center - w_btn - 10, altura - 70, w_btn, h_btn)
        self.botao_proximo_rect = pygame.Rect(
            x_center + 10, altura - 70, w_btn, h_btn)

        # Fundo
        try:
            caminho_fundo = os.path.join(ASSETS_DIR, "cenario.png")
            self.fundo = pygame.image.load(caminho_fundo).convert()
            self.fundo = pygame.transform.scale(self.fundo, (largura, altura))
        except pygame.error:
            self.fundo = None

        # Game State
        self.game_state = {"opcoes": [
            'pedra', 'papel', 'tesoura'], "vitoria": False, "jogado": False}

    # ---------------------------------
    # LÓGICA DO JOGO
    # ---------------------------------

    def _processar_rps(self, jogada_jogador: str):
        jogada_jogador = (jogada_jogador or "").strip().lower()
        if jogada_jogador not in self.game_state["opcoes"]:
            # adiciona apenas o erro de escolha inválida
            self.feedback_jogo = ["Escolha inválida! Pedra, Papel ou Tesoura."]
            return
        jogada_comp = random.choice(self.game_state["opcoes"])
        # monta feedback (substitui qualquer feedback anterior)
        self.feedback_jogo = [
            f"Comp: {jogada_comp.upper()} | Jogador: {jogada_jogador.upper()}"
        ]
        if jogada_jogador == jogada_comp:
            resultado = "Empate!"
        elif (jogada_jogador == 'pedra' and jogada_comp == 'tesoura') or \
            (jogada_jogador == 'tesoura' and jogada_comp == 'papel') or \
                (jogada_jogador == 'papel' and jogada_comp == 'pedra'):
            resultado = "Você venceu! Mini Desafio Completo."
            self.game_state["vitoria"] = True
            self._adicionar_xp_e_salvar(self.desafio_atual["xp"])
        else:
            resultado = "Computador venceu! Fim do Desafio."
            self.mensagem_cor = ROSA_NEON
    # adiciona resultado
        self.feedback_jogo.append(f"Resultado: {resultado}")
    # marca que houve uma jogada
        self.jogada_realizada = True

        try:
            self.input_resposta.text = ""
        except Exception:
            pass

    def _adicionar_xp_e_salvar(self, xp: int):
        self.jogador.xp += xp
        self.jogadores_dict[self.jogador.nome] = self.jogador.to_dict()
        self.salvar_jogadores(self.jogadores_dict)

    # ---------------------------------
    # EVENTOS
    # ---------------------------------
    def lidar_com_eventos(self, event):
        res = self.input_resposta.handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            # SUBMETER: só permite submeter se não tiver jogado ainda
            if self.botao_submeter_rect.collidepoint(mouse_pos) and not self.game_state["jogado"]:
                self._processar_rps(self.input_resposta.get_text())
            # VOLTAR: sempre volta ao menu principal ao clicar
            elif self.botao_proximo_rect.collidepoint(mouse_pos):
                return ("MENU_PRINCIPAL", self.jogador)

        # permitir submit via Enter (handle_event retorna texto)
        if res and not self.game_state["jogado"]:
            self._processar_rps(res)
        return None

    # ---------------------------------
    # DESENHO
    # ---------------------------------

    def atualizar(self):
        pass

    def desenhar(self, tela):
        # Fundo
        if self.fundo:
            tela.blit(self.fundo, (0, 0))
        else:
            tela.fill(PRETO)

        itens = []

        itens.append(
            (self.desafio_atual["titulo"], ROSA_NEON, self.fonte_titulo))

# Introdução
        if not getattr(self, "jogada_realizada", False):
            for line in self.desafio_atual["instrucao_introducao"]:
                itens.append((line, AZUL_NEON, self.fonte_padrao))

# Feedback
        if self.feedback_jogo:
            for line in self.feedback_jogo:
                itens.append((line, BRANCO, self.fonte_padrao))

# Instruções finais
        if getattr(self, "jogada_realizada", False):
            for line in self.desafio_atual.get("instrucao_final", []):
                itens.append((line, BRANCO, self.fonte_padrao))

        margin_x = 40
        max_text_width = max(100, self.largura - margin_x * 2)
        espacamento = 6

        surfaces = []
        for texto, cor, fonte in itens:
            wrapped_lines = wrap_text(texto, fonte, max_text_width)
            for wline in wrapped_lines:
                surf = fonte.render(wline, True, cor)
                surfaces.append(surf)
    # calcula altura total
        alturas = [s.get_height() for s in surfaces]
        altura_total = sum(alturas) + espacamento * \
            (len(surfaces) - 1) if surfaces else 0

    # coloca bloco verticalmente
        margem_inferior = 120
        start_y = max(30, (self.altura - margem_inferior - altura_total) // 2)

    # desenha tudo centralizado horizontalmente
        y = start_y
        for s in surfaces:
            rect = s.get_rect(
                center=(self.largura // 2, y + s.get_height() // 2))
            tela.blit(s, rect)
            y += s.get_height() + espacamento

        if hasattr(self.input_resposta, "rect"):
            # centraliza a input horizontalmente e posiciona logo abaixo do bloco
            try:
                w_input = self.input_resposta.rect.width
                self.input_resposta.rect.x = (self.largura - w_input) // 2
                self.input_resposta.rect.y = y + 20
            except Exception:
                pass
            try:
                self.input_resposta.draw(tela)
            except Exception:
                pass

    # Botões na parte inferior
        cor_sub = VERDE_NEON if not getattr(
            self, "jogada_realizada", False) else CINZENTO
        pygame.draw.rect(
            tela, cor_sub, self.botao_submeter_rect, border_radius=6)
        pygame.draw.rect(
            tela, AZUL_NEON, self.botao_proximo_rect, border_radius=6)

        txt_sub = self.fonte_padrao.render("SUBMETER", True, PRETO)
        rect_sub_text = txt_sub.get_rect(
            center=self.botao_submeter_rect.center)
        tela.blit(txt_sub, rect_sub_text)

        txt_prox = self.fonte_padrao.render("VOLTAR", True, PRETO)
        rect_prox_text = txt_prox.get_rect(
            center=self.botao_proximo_rect.center)
        tela.blit(txt_prox, rect_prox_text)