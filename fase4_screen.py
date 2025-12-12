# fase4_screen.py (PRO - Centralizado e com Quebras Automáticas)

import pygame
import os
from typing import List, Tuple, Optional
from player import Jogador
from screens import InputBox, CINZENTO, VERDE_NEON, ROSA_NEON, AZUL_NEON, BRANCO, PRETO
from utils_audio import play_sound

# ----------------------------------------------------
# DEFINIÇÕES LOCAIS E CONTEÚDO DA FASE 4
# ----------------------------------------------------
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
PIXEL_FONT_PATH = os.path.join(ASSETS_DIR, "PressStart2P-Regular.ttf")

CHALLENGE_4_1 = {
    "id": 1,
    "titulo": "Nível 1: Fábrica de Robôs (WHILE)!",
    "instrucao_principal": [
        "Na fábrica de robôs, os robôs repetem tarefas até que uma condição seja atendida.",
        "Use 'while' para repetir ações enquanto uma condição for verdadeira.",
        "Cuidado! Se a condição nunca for falsa, o loop nunca para!"
    ],
    "instrucao_bloco_2": [
        "Você precisa programar um robô para contar peças até chegar a 10.",
        "O robô começa com 0 peças e adiciona 1 a cada ciclo."
    ],
    "logica": "Exemplo de loop while: while contador < 10: contador += 1",
    "pergunta": "Qual o valor final do contador quando o loop PARAR?",
    "resposta_correta": "10",
    "xp": 20
}

CHALLENGE_4_2 = {
    "id": 2,
    "titulo": "Nível 2: Jardim das Flores (FOR)!",
    "instrucao_principal": [
        "No jardim, as flores crescem em padrões repetitivos.",
        "Em programação, usamos loops 'for' para repetir ações um número fixo de vezes."
    ],
    "instrucao_bloco_2": ["Cada flor cresce em um ciclo, e você precisa plantar 5 flores!"],
    "logica": "Exemplo de loop for: for i in range(1, 6): plantar_flor(i)",
    "pergunta": "Qual o total de flores plantadas?",
    "resposta_correta": "5",
    "xp": 20
}

CHALLENGE_4_3 = {
    "id": 3,
    "titulo": "Nível 3: Torre dos Desafios (Combinado)!",
    "instrucao_principal": ["Você precisa subir 3 andares, coletando 2 itens em cada um."],
    "instrucao_bloco_2": [
        "Combine while e for para resolver o quebra-cabeça.",
        "Lembre-se: O 'while' controla os andares e o 'for' coleta os itens."
    ],
    "logica": "Exemplo: while andares < 3: for i in range(2): coletar_item()",
    "pergunta": "Qual o total de andares que você subiu?",
    "resposta_correta": "3",
    "xp": 20
}

ALL_CHALLENGES_F4 = [CHALLENGE_4_1, CHALLENGE_4_2, CHALLENGE_4_3]

# ----------------------------------------------------
# CLASSE PRINCIPAL
# ----------------------------------------------------


class Fase4Screen:
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

        self.nivel_atual_idx = 0
        self.desafio_atual = ALL_CHALLENGES_F4[self.nivel_atual_idx]
        self.mensagem = ""
        self.mensagem_cor = ROSA_NEON
        self.desafio_concluido_sucesso = False
        self.fase_concluida = False

        # Fundo
        try:
            caminho_fundo = os.path.join(ASSETS_DIR, "cenario.png")
            self.fundo = pygame.image.load(caminho_fundo).convert()
            self.fundo = pygame.transform.scale(self.fundo, (largura, altura))
        except pygame.error:
            self.fundo = None

        # Input
        w_input = 350
        x_center = largura // 2
        self.input_resposta = InputBox(
            x_center - w_input // 2, 440, w_input, 32, 'RESPOSTA AQUI...')
        self.input_resposta.color_inactive = AZUL_NEON
        self.input_resposta.color = AZUL_NEON

        # Botões
        w_btn, h_btn = 150, 40
        self.botao_submeter_rect = pygame.Rect(
            x_center - w_btn - 10, altura - 70, w_btn, h_btn)
        self.botao_proximo_rect = pygame.Rect(
            x_center + 10, altura - 70, w_btn, h_btn)

    # -------------------------
    # Funções Auxiliares
    # -------------------------
    def _wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> List[str]:
        words = text.split(' ')
        lines = []
        current_line = ''
        for word in words:
            test_line = current_line + word + ' '
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + ' '
        if current_line:
            lines.append(current_line.strip())
        return lines

    def _draw_block_text(self, tela, text_lines: List[str], start_y: int, color: Tuple[int, int, int], max_width=560):
        y = start_y
        line_height = self.fonte_padrao.get_linesize()
        for line in text_lines:
            wrapped_lines = self._wrap_text(line, self.fonte_padrao, max_width)
            for wline in wrapped_lines:
                surf = self.fonte_padrao.render(wline, True, color)
                tela.blit(surf, (self.largura // 2 - surf.get_width() // 2, y))
                y += line_height
        return y + 5

    def _draw_title(self, tela, text: str, start_y: int, color=ROSA_NEON, max_width=560):
        wrapped = self._wrap_text(text, self.fonte_titulo, max_width)
        y = start_y
        for line in wrapped:
            surf = self.fonte_titulo.render(line, True, color)
            tela.blit(surf, (self.largura // 2 - surf.get_width() // 2, y))
            y += self.fonte_titulo.get_linesize()
        return y + 10

    def _avancar_nivel(self):
        self._adicionar_xp_e_salvar(self.desafio_atual["xp"])
        self.nivel_atual_idx += 1
        if self.nivel_atual_idx < len(ALL_CHALLENGES_F4):
            self.desafio_atual = ALL_CHALLENGES_F4[self.nivel_atual_idx]
            self.desafio_concluido_sucesso = False
            self.mensagem = f"Nível {self.desafio_atual['id']} desbloqueado!"
            self.input_resposta.text = ""
        else:
            self.fase_concluida = True
            self.jogador.fase = 5
            self._salvar_progresso()

    def _processar_resposta(self, resposta_usuario: str):
        if self.desafio_concluido_sucesso:
            return None
        resposta_usuario = resposta_usuario.strip()
        correto = resposta_usuario == self.desafio_atual["resposta_correta"]
        if correto:
            self.mensagem = "CORRETO! Desafio concluído!"
            play_sound("point")
            self.mensagem_cor = VERDE_NEON
            self.desafio_concluido_sucesso = True
            return ("REWARD", (4, self.nivel_atual_idx))
        else:
            play_sound("error")
            self.mensagem = "Resultado incorreto. Tente novamente."
            self.mensagem_cor = ROSA_NEON
        return None

    def _adicionar_xp_e_salvar(self, xp_ganho):
        self.jogador.xp += xp_ganho
        self.jogadores_dict[self.jogador.nome] = self.jogador.to_dict()
        self.salvar_jogadores(self.jogadores_dict)

    def _salvar_progresso(self):
        self.jogadores_dict[self.jogador.nome] = self.jogador.to_dict()
        self.salvar_jogadores(self.jogadores_dict)

    # -------------------------
    # Eventos
    # -------------------------

    def lidar_com_eventos(self, event) -> Optional[Tuple[str, Optional[Jogador]]]:
        res = self.input_resposta.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.botao_submeter_rect.collidepoint(mouse_pos) and not self.desafio_concluido_sucesso:
                result = self._processar_resposta(
                    self.input_resposta.get_text())
                if result:
                    return result
            elif self.botao_proximo_rect.collidepoint(mouse_pos):
                if self.desafio_concluido_sucesso:
                    # Se terminou TODA a fase 4 -> volta ao menu
                    if self.fase_concluida:
                        return ("MENU_PRINCIPAL", self.jogador)
        # Caso contrário -> avança para o próximo nível (tela de recompensa)
                    else:
                        return ("REWARD", (4, self.nivel_atual_idx))
                else:
                    return ("MENU_PRINCIPAL", self.jogador)

        if res is not None and not self.desafio_concluido_sucesso:
            result = self._processar_resposta(res)
            if result:
                return result
        return None

    def atualizar(self):
        pass

    # -------------------------
    # Desenho
    # -------------------------
    def desenhar(self, tela):
        # Fundo
        if self.fundo:
            tela.blit(self.fundo, (0, 0))
        else:
            tela.fill(PRETO)

        y = 30
        y = self._draw_title(tela, self.desafio_atual["titulo"], y)

        # Bloco 1: Instrução Principal
        y = self._draw_block_text(tela, self.desafio_atual.get(
            "instrucao_principal", []), y, AZUL_NEON)

        # Bloco 2: Instrução Secundária
        y = self._draw_block_text(tela, self.desafio_atual.get(
            "instrucao_bloco_2", []), y, AZUL_NEON)

        # Bloco 3: Lógica
        y = self._draw_block_text(
            tela, [self.desafio_atual.get("logica", "")], y, BRANCO)

        # Bloco 4: Pergunta
        y = self._draw_title(tela, self.desafio_atual.get(
            "pergunta", ""), y, ROSA_NEON)

        # Input
        input_bg_rect = self.input_resposta.rect.inflate(10, 10)
        pygame.draw.rect(tela, (30, 30, 30), input_bg_rect, 0, 5)
        self.input_resposta.draw(tela)

        # Feedback
        if self.mensagem:
            msg_surf = self.fonte_padrao.render(
                self.mensagem, True, self.mensagem_cor)
            tela.blit(msg_surf, (self.largura // 2 -
                      msg_surf.get_width() // 2, 500))

        # Botões
        cor_submeter = VERDE_NEON if not self.desafio_concluido_sucesso else CINZENTO
        pygame.draw.rect(tela, cor_submeter, self.botao_submeter_rect)
        texto_submeter = self.fonte_padrao.render("SUBMETER", True, PRETO)
        tela.blit(texto_submeter, (self.botao_submeter_rect.centerx - texto_submeter.get_width() // 2,
                                   self.botao_submeter_rect.centery - texto_submeter.get_height() // 2))

        label_proximo = "PRÓXIMO" if self.desafio_concluido_sucesso else "VOLTAR"
        cor_proximo = AZUL_NEON if self.desafio_concluido_sucesso else ROSA_NEON
        pygame.draw.rect(tela, cor_proximo, self.botao_proximo_rect)
        texto_proximo = self.fonte_padrao.render(label_proximo, True, PRETO)
        tela.blit(texto_proximo, (self.botao_proximo_rect.centerx - texto_proximo.get_width() // 2,
                                  self.botao_proximo_rect.centery - texto_proximo.get_height() // 2))
