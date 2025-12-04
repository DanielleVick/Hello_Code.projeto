# desafios_extras_screen.py (PEDRA, PAPEL E TESOURA COM INTRO + FEEDBACK)

import pygame
import os
import random
from typing import List
from player import Jogador
from screens import InputBox, CINZENTO, VERDE_NEON, ROSA_NEON, AZUL_NEON, BRANCO, PRETO

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
PIXEL_FONT_PATH = os.path.join(ASSETS_DIR, "PressStart2P-Regular.ttf")

CHALLENGE_EXTRA_1 = {
    "id": 1,
    "titulo": "Extra: Pedra, Papel e Tesoura!",
    "instrucao_introducao": [
        "Em programação, podemos criar jogos simples usando condicionais e loops.",
        "Vamos jogar Pedra, Papel e Tesoura contra o computador!",
        "Regras: Pedra ganha de Tesoura, Tesoura de Papel, Papel de Pedra."
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
        jogada_jogador = jogada_jogador.lower()
        if jogada_jogador not in self.game_state["opcoes"]:
            self.feedback_jogo.append(
                "Escolha inválida! Pedra, Papel ou Tesoura.")
            return

        jogada_comp = random.choice(self.game_state["opcoes"])
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

        self.feedback_jogo.append(f"Resultado: {resultado}")
        self.game_state["jogado"] = True
        self.sub_estado = "FINALIZADO_SUCESSO" if self.game_state["vitoria"] else "FINALIZADO_FALHA"
        self.input_resposta.text = ""  # limpa input

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
            if self.botao_submeter_rect.collidepoint(mouse_pos) and not self.game_state["jogado"]:
                self._processar_rps(self.input_resposta.get_text())
            elif self.botao_proximo_rect.collidepoint(mouse_pos) and self.game_state["jogado"]:
                return ("MENU_PRINCIPAL", self.jogador)

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

        # Título
        texto_titulo = self.fonte_titulo.render(
            self.desafio_atual["titulo"], True, ROSA_NEON)
        tela.blit(texto_titulo, (self.largura // 2 -
                  texto_titulo.get_width() // 2, 30))

        y = 80
        # Mostrar instruções
        for line in self.desafio_atual["instrucao_introducao"]:
            txt_surf = self.fonte_padrao.render(line, True, AZUL_NEON)
            tela.blit(txt_surf, (self.largura // 2 -
                      txt_surf.get_width() // 2, y))
            y += 20

        # Mostrar feedback do jogo
        if self.feedback_jogo:
            y += 20
            for idx, line in enumerate(self.feedback_jogo):
                txt_surf = self.fonte_padrao.render(line, True, BRANCO)
                tela.blit(txt_surf, (self.largura // 2 -
                          txt_surf.get_width() // 2, y + idx * 20))

        # Input (se não jogou ainda)
        if not self.game_state["jogado"]:
            input_bg_rect = self.input_resposta.rect.inflate(10, 10)
            pygame.draw.rect(tela, (30, 30, 30), input_bg_rect, 0, 5)
            self.input_resposta.draw(tela)

        # Botões
        pygame.draw.rect(
            tela, VERDE_NEON, self.botao_submeter_rect if not self.game_state["jogado"] else CINZENTO)
        pygame.draw.rect(tela, AZUL_NEON, self.botao_proximo_rect)
        txt_sub = self.fonte_padrao.render("SUBMETER", True, PRETO)
        txt_prox = self.fonte_padrao.render("VOLTAR", True, PRETO)
        tela.blit(txt_sub, (self.botao_submeter_rect.x +
                  10, self.botao_submeter_rect.y + 10))
        tela.blit(txt_prox, (self.botao_proximo_rect.x +
                  10, self.botao_proximo_rect.y + 10))
