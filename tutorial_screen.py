# tutorial_screen.py (CORRIGIDO PARA EVITAR IMPORT CIRCULAR)

import pygame
import os
from typing import Dict, Any, List, Optional, Tuple
from player import Jogador
from screens import CINZENTO, VERDE_NEON, ROSA_NEON, AZUL_NEON, BRANCO, PRETO, LARANJA
# 🌟 IMPORTAÇÃO DE gui_main FOI REMOVIDA AQUI!

# ----------------------------------------------------
# DEFINIÇÕES LOCAIS (Para evitar importação circular)
# ----------------------------------------------------
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
PIXEL_FONT_PATH = os.path.join(ASSETS_DIR, "PressStart2P-Regular.ttf")
# ----------------------------------------------------

# ----------------------------------------------------
# CONTEÚDO DO TUTORIAL
# ----------------------------------------------------
TUTORIAL_CONTENTS = {
    "1": "FASE 1 / NÍVEL 1: Organize os passos na ordem correta. Assim como em uma receita, cada passo precisa acontecer no momento certo.",
    "2": "FASE 1 / NÍVEL 2: Este é o mercado desorganizado, alguns itens estão fora do lugar! Seu desafio é encontrar o item que está na prateleira errada. Observe cada prateleira e identifique qual item está errado.",
    "3": "FASE 1 / NÍVEL 3: Escolha entre os caminhos A, B ou C. O caminho correto segue uma lógica passo a passo sem pular etapas.",
    "4": "FASE 2 / NÍVEL 1: Combine valores dos frascos usando soma ou multiplicação. Crie a fórmula correta usando operações matemáticas.",
    "5": "FASE 2 / NÍVEL 2: Ilha dos Tesouros. Use operadores matemáticos (soma, multiplicação, resto da divisão) para descobrir o total de moedas.",
    "6": "FASE 2 / NÍVEL 3: Salão Mágico. Funções recebem valores, processam e retornam resultados. Use funções para misturar cristais e poções.",
    "7": "FASE 3 / NÍVEL 1: If/Else. Treine condições simples. Verifique se a idade permite entrada.",
    "8": "FASE 3 / NÍVEL 2: If/Elif/Else. Aprenda como Python avalia múltiplas condições, escolhendo sempre a primeira verdadeira.",
    "9": "FASE 3 / NÍVEL 3: Condições combinadas (AND/OR). A porta só abre quando ambas as condições são verdadeiras.",
    "10": "FASE 4 / NÍVEL 1 (While): Fábrica de Robôs. Use um loop WHILE para repetir ações até chegar a um número. Um loop WHILE repete enquanto a condição for VERDADEIRA. Cuidado com loops infinitos!",
    "11": "FASE 4 / NÍVEL 2 (For): Jardim das Flores. Use o loop FOR para executar ações um número fixo de vezes (plantar 5 flores). O loop FOR é ideal quando você sabe exatamente quantas repetições precisa.",
    "12": "FASE 4 / NÍVEL 3 (Combinado): Torre dos Desafios. Combine WHILE (controlar andares) e FOR (coletar itens) para subir a torre."
}

# ----------------------------------------------------
# CLASSE PRINCIPAL
# ----------------------------------------------------


class TutorialScreen:
    def __init__(self, largura: int, altura: int, jogador: Jogador):
        self.largura = largura
        self.altura = altura
        self.jogador = jogador

        # 🌟 USANDO A DEFINIÇÃO LOCAL DA FONTE
        self.fonte_padrao = pygame.font.Font(PIXEL_FONT_PATH, 16)
        self.fonte_titulo = pygame.font.Font(PIXEL_FONT_PATH, 24)

        try:
            assets_dir = os.path.join(os.path.dirname(__file__), "assets")
            caminho_fundo = os.path.join(assets_dir, "telatutorial.jpeg")
            self.fundo = pygame.image.load(caminho_fundo).convert()
            self.fundo = pygame.transform.scale(self.fundo, (largura, altura))
        except pygame.error:
            self.fundo = None

        # 2. Gestão de Estado Interno
        self.estado_tela = "MENU"  # "MENU" ou "DETALHES"
        self.nivel_selecionado = None

        # 3. Definição dos Botões de Menu
        self.botoes_menu, self.y_ultimo_botao = self._criar_botoes_menu()

        # 4. Botão SAIR (Fixo)
        w_btn, h_btn = 150, 40
        x_center = largura // 2
        y_sair = altura - 30
        self.botao_sair_rect = pygame.Rect(
            x_center - w_btn // 2, y_sair, w_btn, h_btn)

    def _criar_botoes_menu(self) -> Tuple[List[Dict[str, Any]], int]:
        botoes_list = []
        x_center = self.largura // 2
        y_start = 80
        gap = 10
        w_btn = 350

        opcoes_texto = [
            "1. Fase 1/NÍVEL 1", "2. Fase 1/NÍVEL 2",
            "3. Fase 1/NÍVEL 3", "4. Fase 2/NÍVEL 1",
            "5. Fase 2/NÍVEL 2", "6. Fase 2/NÍVEL 3",
            "7. Fase 3/NÍVEL 1", "8. Fase 3/NÍVEL 2",
            "9. Fase 3/NÍVEL 3", "10. Fase 4/NÍVEL 1",
            "11. Fase 4/NÍVEL 2", "12. Fase 4/NÍVEL 3"
        ]

        y_atual = y_start
        for i, texto in enumerate(opcoes_texto):
            nivel_id = str(i + 1)

            rect = pygame.Rect(x_center - w_btn // 2, y_atual, w_btn, 30)

            botoes_list.append({
                "texto": texto,
                "estado": nivel_id,
                "rect": rect,
                "cor": AZUL_NEON
            })
            y_atual += 30 + gap

        return botoes_list, botoes_list[-1]["rect"].bottom if botoes_list else 0

    def lidar_com_eventos(self, event) -> Optional[Tuple[str, Optional[Jogador]]]:
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            # 1. Botão VOLTAR/SAIR (Sair para o Menu Principal)
            if self.botao_sair_rect.collidepoint(mouse_pos):
                if self.estado_tela == "DETALHES":
                    # Se estiver nos detalhes, volta para o menu do tutorial
                    self.estado_tela = "MENU"
                    self.nivel_selecionado = None
                else:
                    # Se estiver no menu principal do tutorial, volta para o Menu Principal
                    return ("MENU_PRINCIPAL", self.jogador)

            # 2. Navegação do Menu do Tutorial (Apenas se estiver no estado MENU)
            if self.estado_tela == "MENU":
                for botao in self.botoes_menu:
                    if botao["rect"].collidepoint(mouse_pos):
                        # Vai para a tela de DETALHES do nível selecionado
                        self.estado_tela = "DETALHES"
                        self.nivel_selecionado = botao["estado"]
                        return None

        return None

    def atualizar(self):
        pass

    def desenhar_menu_principal(self, tela):
        texto_titulo = self.fonte_titulo.render("TUTORIAL", True, LARANJA)
        tela.blit(texto_titulo, (self.largura // 2 -
                  texto_titulo.get_width() // 2, 50))

        for botao in self.botoes_menu:
            pygame.draw.rect(tela, botao["cor"], botao["rect"])

            texto_render = self.fonte_padrao.render(
                botao["texto"], True, PRETO)

            text_x = botao["rect"].x + 10
            text_y = botao["rect"].y + \
                (botao["rect"].height - texto_render.get_height()) // 2
            tela.blit(texto_render, (text_x, text_y))

    def desenhar_detalhes(self, tela):
        conteudo = TUTORIAL_CONTENTS.get(
            self.nivel_selecionado, "Conteúdo não encontrado.")

        titulo = f"Detalhes do Nível {self.nivel_selecionado}"
        texto_titulo = self.fonte_titulo.render(titulo, True, BRANCO)
        tela.blit(texto_titulo, (self.largura // 2 -
                  texto_titulo.get_width() // 2, 50))

        font_height = self.fonte_padrao.get_linesize()
        x_start = 50
        y_start = 120
        max_width = self.largura - 100

        palavras = conteudo.split(' ')
        linha = ''
        linhas_desenhadas = []

        for palavra in palavras:
            if self.fonte_padrao.render(linha + ' ' + palavra, True, LARANJA).get_width() < max_width:
                linha += ' ' + palavra
            else:
                linhas_desenhadas.append(linha)
                linha = palavra
        linhas_desenhadas.append(linha)

        for i, linha_texto in enumerate(linhas_desenhadas):
            texto_render = self.fonte_padrao.render(
                linha_texto.strip(), True, LARANJA)
            tela.blit(texto_render, (x_start, y_start + i * font_height))

    def desenhar(self, tela):
        if self.fundo:
            tela.blit(self.fundo, (0, 0))
        else:
            tela.fill(PRETO)

        if self.estado_tela == "MENU":
            self.desenhar_menu_principal(tela)
        else:
            self.desenhar_detalhes(tela)

        pygame.draw.rect(tela, ROSA_NEON, self.botao_sair_rect)

        texto_btn = "VOLTAR" if self.estado_tela == "DETALHES" else "VOLTAR"
        texto_render = self.fonte_padrao.render(texto_btn, True, PRETO)

        text_x = self.botao_sair_rect.x + \
            (self.botao_sair_rect.width - texto_render.get_width()) // 2
        text_y = self.botao_sair_rect.y + 5
        tela.blit(texto_render, (text_x, text_y))
