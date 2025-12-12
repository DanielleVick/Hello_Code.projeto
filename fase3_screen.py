# fase3_screen.py (COMPLETO — centralização em bloco, quebra automática 560px)
import pygame
import os
from typing import Dict, Any, List, Optional, Tuple
from player import Jogador
from screens import InputBox, CINZENTO, VERDE_NEON, ROSA_NEON, AZUL_NEON, BRANCO, PRETO
try:
    from utils_audio import play_sound
except Exception:
    def play_sound(name):
        pass

# ----------------------------------------------------
# DEFINIÇÕES LOCAIS E CONTEÚDO DA FASE 3
# ----------------------------------------------------
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
PIXEL_FONT_PATH = os.path.join(ASSETS_DIR, "PressStart2P-Regular.ttf")

# Nível 1: Sociedade dos Loops (If/Else)
CHALLENGE_3_1 = {
    "id": 1,
    "titulo": "Nível 1: Sociedade Condicional!",
    "instrucao_bloco_1": "Você é o guardião de um portão que só deixa passar pessoas com idade adequada. Usando estruturas condicionais (if/else),",
    "instrucao_bloco_2": "Você precisa decidir se cada pessoa pode ou não realizar determinada ação. Vamos começar!",
    "logica": "Qual opção verifica 'idade = 20' corretamente?",
    "opcoes": [
        "a) if idade > 18:", "b) if idade >= 18:",
        "c) if idade < 18:", "d) if idade == 18:"
    ],
    "pergunta": "Qual opção verifica 'idade = 20' corretamente?",
    "resposta_correta": "B",
    "xp": 20
}

# Nível 2: Ponte dos Três Resultados (If/Elif/Else)
CHALLENGE_3_2 = {
    "id": 2,
    "titulo": "Nível 2: Ponte dos Três Resultados!",
    "instrucao_bloco_1": "Uma ponte encantada avalia seu nível de foco e escolhe um caminho mágico.",
    "instrucao_bloco_2": "Sabendo que seu foco é 73, qual caminho a ponte escolherá para você?",
    "logica": "Lógica inscrita: if foco >= 90 / elif foco >= 60 / else Passagem Nebulosa",
    "opcoes": [
        "Rajada Dourada", "Trilha Prateada", "Passagem Nebulosa"
    ],
    "pergunta": "Digite o nome do caminho mágico correto:",
    "resposta_correta": "TRILHA PRATEADA",
    "xp": 20
}

# Nível 3: Porta das Condições Combinadas (AND/OR)
CHALLENGE_3_3 = {
    "id": 3,
    "titulo": "Nível 3: Porta Lógica AND/OR!",
    "instrucao_bloco_1": "Você precisa ativar uma porta mágica que só abre quando duas condições são verdadeiras:",
    "instrucao_bloco_2": "Qual será o valor de 'resposta' se energia = 55 e tem_cristal = False?",
    "logica": "if E>=40 AND T=True / elif E>=40 OR T=True / else 'Sem chance'.",
    "opcoes": [
        "A: Sequência lógica que organiza ideias e verifica erros.",
        "B: A porta não abre, mas aparece a mensagem 'Quase lá'.",
        "C: A porta abre, mas aparece a mensagem 'Sem chance'."
    ],
    "pergunta": "Digite a letra correta (A, B ou C):",
    "resposta_correta": "B",
    "xp": 20
}

ALL_CHALLENGES_F3 = [CHALLENGE_3_1, CHALLENGE_3_2, CHALLENGE_3_3]

# ----------------------------------------------------
# FUNÇÕES GERAIS: QUEBRA AUTOMÁTICA E CENTRALIZAÇÃO EM BLOCO
# ----------------------------------------------------


def wrap_text(text: str, font: pygame.font.Font, max_width: int) -> List[str]:
    """
    Quebra um texto automaticamente em várias linhas para caber dentro de max_width.
    Mantém palavras inteiras.
    """
    if not text:
        return []
    words = text.split(" ")
    lines: List[str] = []
    current = ""
    for w in words:
        test = (current + " " + w).strip() if current else w
        if font.size(test)[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


def draw_centered_block(surface: pygame.Surface, text: str, font: pygame.font.Font, color: Tuple[int, int, int],
                        start_y: int, max_width: int, screen_width: int) -> int:
    """
    Quebra automaticamente o texto e centraliza o BLOCO inteiro.
    Retorna o y após o bloco.
    """
    lines = wrap_text(text, font, max_width)
    if not lines:
        return start_y
    line_height = font.get_linesize()
    block_width = max(font.size(line)[0] for line in lines)
    x_start = (screen_width - block_width) // 2
    y = start_y
    for line in lines:
        surf = font.render(line, True, color)
        x_line = x_start + (block_width - surf.get_width()) // 2
        surface.blit(surf, (x_line, y))
        y += line_height
    return y

# ----------------------------------------------------
# CLASSE PRINCIPAL
# ----------------------------------------------------


class Fase3Screen:
    def __init__(self, largura: int, altura: int, jogador: Jogador, salvar_jogadores, jogadores_dict):
        self.largura = largura
        self.altura = altura
        self.jogador = jogador
        self.salvar_jogadores = salvar_jogadores
        self.jogadores_dict = jogadores_dict

        # Fontes
        try:
            self.fonte_padrao = pygame.font.Font(PIXEL_FONT_PATH, 14)
            self.fonte_titulo = pygame.font.Font(PIXEL_FONT_PATH, 24)
        except Exception:
            self.fonte_padrao = pygame.font.Font(None, 24)
            self.fonte_titulo = pygame.font.Font(None, 32)

        # Estado
        self.nivel_atual_idx = 0
        self.desafio_atual = ALL_CHALLENGES_F3[self.nivel_atual_idx]
        self.mensagem = ""
        self.mensagem_cor = ROSA_NEON
        self.desafio_concluido_sucesso = False
        self.fase_concluida = False

        # Fundo
        try:
            caminho_fundo = os.path.join(ASSETS_DIR, "cenario.png")
            self.fundo = pygame.image.load(caminho_fundo).convert()
            self.fundo = pygame.transform.scale(self.fundo, (largura, altura))
        except Exception:
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

    # -------------------------------------------------------------------
    # Utilitários de desenho (usando funções gerais)
    # -------------------------------------------------------------------
    def _draw_text_block(self, tela, texto: str, start_y: int, cor, max_width=560) -> int:
        """
        Usa draw_centered_block (centralização em bloco).
        """
        return draw_centered_block(
            surface=tela,
            text=texto,
            font=self.fonte_padrao,
            color=cor,
            start_y=start_y,
            max_width=max_width,
            screen_width=self.largura
        )

    def _draw_title_block(self, tela, texto: str, start_y: int, cor) -> int:
        """
        Título com fonte maior; usa a mesma lógica de bloco.
        """
        return draw_centered_block(
            surface=tela,
            text=texto,
            font=self.fonte_titulo,
            color=cor,
            start_y=start_y,
            max_width=700,
            screen_width=self.largura
        )

    def _draw_text_block_left(self, tela, texto: str, start_y: int, cor, max_width=560) -> int:
        """
        Desenha texto alinhado à esquerda (listas/opções), com quebra automática.
        """
        linhas = wrap_text(texto, self.fonte_padrao, max_width)
        y = start_y
        margem_x = self.largura // 2 - 250
        for linha in linhas:
            surf = self.fonte_padrao.render(linha, True, cor)
            tela.blit(surf, (margem_x, y))
            y += self.fonte_padrao.get_linesize()
        return y

    # -------------------------------------------------------------------
    # Progressão e salvamento
    # -------------------------------------------------------------------
    def _adicionar_xp_e_salvar(self, xp_ganho):
        self.jogador.xp += xp_ganho
        self.jogadores_dict[self.jogador.nome] = self.jogador.to_dict()
        self.salvar_jogadores(self.jogadores_dict)

    def _salvar_progresso(self):
        self.jogadores_dict[self.jogador.nome] = self.jogador.to_dict()
        self.salvar_jogadores(self.jogadores_dict)

    def _avancar_nivel(self):
        # Dar XP (após REWARD)
        self._adicionar_xp_e_salvar(self.desafio_atual["xp"])
        self.nivel_atual_idx += 1
        if self.nivel_atual_idx < len(ALL_CHALLENGES_F3):
            self.desafio_atual = ALL_CHALLENGES_F3[self.nivel_atual_idx]
            self.desafio_concluido_sucesso = False
            self.mensagem = f"Nível {self.desafio_atual['id']} desbloqueado!"
            self.input_resposta.text = ""
        else:
            self.fase_concluida = True
            self.jogador.fase = 4
            self._salvar_progresso()

    # -------------------------------------------------------------------
    # Processar resposta
    # -------------------------------------------------------------------
    def _processar_resposta(self, resposta_usuario: str):
        if self.desafio_concluido_sucesso:
            return None
        resposta_usuario = resposta_usuario.strip().upper()
        correto = (resposta_usuario ==
                   self.desafio_atual["resposta_correta"].upper())
        if correto:
            self.mensagem = "CORRETO! Desafio concluído!"
            play_sound("point")
            self.mensagem_cor = VERDE_NEON
            self._adicionar_xp_e_salvar(self.desafio_atual["xp"])
            self.desafio_concluido_sucesso = True
            return ("REWARD", (3, self.nivel_atual_idx))
        else:
            play_sound("error")
            self.mensagem = "Resultado incorreto. Tente novamente."
            self.mensagem_cor = ROSA_NEON
            return None

    # -------------------------------------------------------------------
    # Eventos
    # -------------------------------------------------------------------
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
                    if self.fase_concluida:
                        return ("MENU_PRINCIPAL", self.jogador)
                    else:
                        return ("REWARD", (3, self.nivel_atual_idx))
                else:
                    return ("MENU_PRINCIPAL", self.jogador)

        if res is not None and not self.desafio_concluido_sucesso:
            result = self._processar_resposta(res)
            if result:
                return result

        return None

    def atualizar(self):
        pass

    # -------------------------------------------------------------------
    # Desenhar tela (com novo sistema)
    # -------------------------------------------------------------------
    def desenhar(self, tela):
        # 1. Fundo
        if self.fundo:
            tela.blit(self.fundo, (0, 0))
        else:
            tela.fill(PRETO)

        # 2. Título
        y = self._draw_title_block(
            tela, self.desafio_atual["titulo"], 30, ROSA_NEON)

        # 3. Instrução bloco 1
        y += 20
        y = self._draw_text_block(tela, self.desafio_atual.get(
            "instrucao_bloco_1", ""), y, AZUL_NEON)

        # 4. Instrução bloco 2
        y += 20
        y = self._draw_text_block(tela, self.desafio_atual.get(
            "instrucao_bloco_2", ""), y, BRANCO)

        # 5. Lógica (se existir)
        if self.desafio_atual.get("logica"):
            y += 25
            y = self._draw_text_block(
                tela, self.desafio_atual["logica"], y, BRANCO)

        # 6. Pergunta
        y += 30
        y = self._draw_text_block(
            tela, self.desafio_atual.get("pergunta", ""), y, ROSA_NEON)

        # guarda posição para opções
        y_opcoes_inicial = y + 25

        # 7. Opções (listas, alinhado à esquerda)
        if "opcoes" in self.desafio_atual:
            y = y_opcoes_inicial
            for opcao in self.desafio_atual["opcoes"]:
                y = self._draw_text_block_left(tela, opcao, y, BRANCO)
                y += 5

        # 9. Input
        input_bg_rect = self.input_resposta.rect.inflate(10, 10)
        pygame.draw.rect(tela, (30, 30, 30), input_bg_rect, 0, 5)
        self.input_resposta.draw(tela)

        # 10. Mensagem de feedback
        if self.mensagem:
            self._draw_text_block(tela, self.mensagem, 500, self.mensagem_cor)

        # 11. Botões
        cor_submeter = VERDE_NEON if not self.desafio_concluido_sucesso else CINZENTO
        pygame.draw.rect(tela, cor_submeter,
                         self.botao_submeter_rect, border_radius=6)
        texto_submeter = self.fonte_padrao.render("SUBMETER", True, PRETO)
        tela.blit(
            texto_submeter,
            (
                self.botao_submeter_rect.x +
                (self.botao_submeter_rect.width //
                 2 - texto_submeter.get_width() // 2),
                self.botao_submeter_rect.y + 8
            )
        )

        if self.desafio_concluido_sucesso:
            label = "PRÓXIMO" if not self.fase_concluida else "MENU"
            cor_proximo = AZUL_NEON
        else:
            label = "VOLTAR"
            cor_proximo = ROSA_NEON

        pygame.draw.rect(tela, cor_proximo,
                         self.botao_proximo_rect, border_radius=6)
        texto_proximo = self.fonte_padrao.render(label, True, PRETO)
        tela.blit(
            texto_proximo,
            (
                self.botao_proximo_rect.x +
                (self.botao_proximo_rect.width //
                 2 - texto_proximo.get_width() // 2),
                self.botao_proximo_rect.y + 8
            )
        )
