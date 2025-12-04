# reward_screen.py (CORRIGIDO E FUNCIONAL)

import pygame
import os
from typing import Dict, Any, Optional, Tuple
from player import Jogador 
from screens import CINZENTO, VERDE_NEON, ROSA_NEON, AZUL_NEON, BRANCO, PRETO 

# ----------------------------------------------------
# DEFINIÇÕES LOCAIS (Para evitar importação circular)
# ----------------------------------------------------
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
PIXEL_FONT_PATH = os.path.join(ASSETS_DIR, "PressStart2P-Regular.ttf") 

# MAPAS DE RECOMPENSA (AGORA COM XP DEFINIDO)
REWARDS_MAPPING = {
    # FASE 1
    (1, 0): {"nome": "Placa-mãe", "texto": "É a “base” de tudo.", "asset": "placamae.png", "xp": 20},
    (1, 1): {"nome": "CPU", "texto": "O cérebro da máquina. Ele processa as informações.", "asset": "cpu.png", "xp": 20},
    (1, 2): {"nome": "Memória RAM", "texto": "A memória de curto prazo. Guarda temporariamente o que o computador está usando no momento.", "asset": "memoriaram.png", "xp": 20},

    # FASE 2
    (2, 0): {"nome": "SSD", "texto": "Onde ficam salvos os arquivos e o sistema. É super rápido.", "asset": "ssd.png", "xp": 20},
    (2, 1): {"nome": "COOLER", "texto": "Responsável por manter o computador fresquinho.", "asset": "cooler.png", "xp": 20},
    (2, 2): {"nome": "GPU", "texto": "A placa de vídeo. Ela cuida das imagens, gráficos e jogos.", "asset": "gpu.png", "xp": 20},

    # FASE 3
    (3, 0): {"nome": "TECLADO", "texto": "A forma principal de digitar e enviar comandos pro PC.", "asset": "teclado.png", "xp": 20},
    (3, 1): {"nome": "MOUSE", "texto": "O ponteiro da tua vida. Serve para selecionar, clicar e navegar com precisão.", "asset": "mouse.png", "xp": 20},
    (3, 2): {"nome": "MOUSEPAD", "texto": "A superfície que ajuda o mouse a deslizar de maneira suave e precisa.", "asset": "mousepad.png", "xp": 20},

    # FASE 4
    (4, 0): {"nome": "MONITOR", "texto": "A tela onde tudo aparece.", "asset": "monitor.png", "xp": 20},
    (4, 1): {"nome": "GABINETE", "texto": "A “casa” onde ficam as peças internas do PC.", "asset": "gabinete.png", "xp": 20},
    (4, 2): {"nome": "PATINHO DEBUG", "texto": "O mascote da programação! Ajuda os programadores a pensarem melhor.", "asset": "patinhodebug.png", "xp": 20},
    
    # RECOMPENSA FINAL (Chave 5, 0)
    (5, 0): {"nome": "SETUP COMPLETO", "texto": "Parabéns! Você concluiu todas as fases, aqui está a união de todas as suas peças.", "asset": "setupcompleto.png", "xp": 0},
}


class RewardScreen:
    def __init__(self, largura: int, altura: int, jogador: Jogador, fase_id: int, nivel_idx: int, fase_concluida: bool):
        self.largura = largura
        self.altura = altura
        self.jogador = jogador
        self.fase_id = fase_id
        self.nivel_idx = nivel_idx
        self.fase_concluida = fase_concluida
        
        # 🌟 CORREÇÃO 1: Garante que a chave existe antes de buscar
        chave = (5, 0) if (fase_id == 4 and nivel_idx == 2 and fase_concluida) else (fase_id, nivel_idx)
        self.recompensa = REWARDS_MAPPING.get(chave)
        
        # O erro estava aqui: se a chave não existisse, get() retornava None. 
        # Agora sabemos que self.recompensa é um dicionário ou None.
        
        if self.recompensa is None:
            # Fallback robusto, caso a chave seja inválida (por exemplo, nivel_idx > 2)
            self.recompensa = {"nome": "Recompensa Desconhecida", "texto": "Erro: Recompensa não mapeada.", "asset": None, "xp": 0}

        # 🌟 CORREÇÃO 2: Acessa diretamente o dicionário (que agora é garantido)
        is_final_reward = (self.recompensa["nome"] == "SETUP COMPLETO")
        self.xp_ganho = self.recompensa["xp"] if not is_final_reward else 0 

        
        try:
            self.fonte_padrao = pygame.font.Font(PIXEL_FONT_PATH, 16) 
            self.fonte_titulo = pygame.font.Font(PIXEL_FONT_PATH, 30)
        except Exception:
            self.fonte_padrao = pygame.font.Font(None, 24) 
            self.fonte_titulo = pygame.font.Font(None, 32)
        
        self.cor_fundo = (10, 10, 30) 
        
        self.imagem_recompensa = self._carregar_imagem_recompensa()
            
        # Botão Continuar
        w_btn, h_btn = 250, 50
        x_center = largura // 2
        self.botao_continuar_rect = pygame.Rect(x_center - w_btn // 2, altura - 100, w_btn, h_btn)


    def _carregar_imagem_recompensa(self):
        """Carrega e redimensiona o asset da recompensa."""
        asset_name = self.recompensa.get("asset") 
        if not asset_name: return None
        
        try:
            assets_dir = os.path.join(os.path.dirname(__file__), "assets")
            # 🌟 CORREÇÃO FINAL: Usa os nomes genéricos para o carregamento
            # Assumindo que você renomeou as imagens para nomes simples (placamae.png, etc.)
            # Se você usa os nomes longos, troque "placamae.png" para "placamae 21.jpg"
            caminho_img = os.path.join(assets_dir, asset_name)
            img = pygame.image.load(caminho_img).convert_alpha()
            
            size = 300 if asset_name == "setupcompleto.png" else 200
            
            return pygame.transform.scale(img, (size, size)) 
        except pygame.error as e:
            print(f"Aviso: Imagem de recompensa '{asset_name}' não encontrada. Erro: {e}")
            return None


    def _draw_text_wrapped(self, tela, text: str, start_y: int, max_width: int, color: Tuple[int, int, int]):
        """Desenha texto com quebra de linha manual para Pygame."""
        lines = []
        words = text.split(' ')
        current_line = ''
        
        for word in words:
            if self.fonte_padrao.render(current_line + ' ' + word, True, color).get_width() < max_width:
                current_line += ' ' + word
            else:
                lines.append(current_line.strip())
                current_line = word
        lines.append(current_line.strip())

        y = start_y
        for line in lines:
            text_surface = self.fonte_padrao.render(line, True, color)
            x = self.largura // 2 - text_surface.get_width() // 2
            tela.blit(text_surface, (x, y))
            y += self.fonte_padrao.get_linesize()


    def lidar_com_eventos(self, event) -> Optional[Tuple[str, Optional[Jogador]]]:
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            # Botão Continuar
            if self.botao_continuar_rect.collidepoint(mouse_pos):
                # Retorna o estado "NEXT_LEVEL" para o gui_main avançar na fase
                return ("NEXT_LEVEL", self.jogador) 
        return None

    def atualizar(self):
        pass

    def desenhar(self, tela):
        tela.fill(self.cor_fundo)
        x_center = self.largura // 2
        
        is_final_setup = (self.recompensa["nome"] == "SETUP COMPLETO")
        
        # 1. Título
        if is_final_setup:
            texto_titulo = self.fonte_titulo.render("PARABÉNS! SETUP COMPLETO!", True, AZUL_NEON)
        else:
            texto_titulo = self.fonte_titulo.render("NÍVEL CONCLUÍDO!", True, VERDE_NEON)
            
        tela.blit(texto_titulo, (x_center - texto_titulo.get_width() // 2, 50))

        # 2. Item Ganho e Descrição
        nome_item = self.recompensa['nome'].upper()
        texto_item = self.fonte_padrao.render(f"VOCÊ GANHOU: {nome_item}", True, BRANCO)
        tela.blit(texto_item, (x_center - texto_item.get_width() // 2, 100))
        
        # 3. Desenhar a imagem da recompensa
        if self.imagem_recompensa:
            img_x = x_center - self.imagem_recompensa.get_width() // 2
            # Posição Y ajustada para a imagem maior
            img_y = 130 if not is_final_setup else 100
            tela.blit(self.imagem_recompensa, (img_x, img_y))

        # 4. Descrição Educativa
        if not is_final_setup:
            # Texto educativo aparece abaixo da imagem
            self._draw_text_wrapped(tela, self.recompensa['texto'], 380, self.largura - 100, ROSA_NEON)
            
            # 5. XP Ganho
            texto_xp = self.fonte_padrao.render(f"+ {self.xp_ganho} XP", True, AZUL_NEON)
            tela.blit(texto_xp, (x_center - texto_xp.get_width() // 2, 450))
        
        elif is_final_setup:
            # Texto da recompensa final (abaixo do setup)
            self._draw_text_wrapped(tela, self.recompensa['texto'], 430, self.largura - 100, ROSA_NEON)


        # 6. Botão Continuar/Voltar
        pygame.draw.rect(tela, ROSA_NEON, self.botao_continuar_rect)
        
        label_btn = "MENU" if is_final_setup else "CONTINUAR"
        texto_continuar = self.fonte_padrao.render(label_btn, True, PRETO)
        
        text_x = self.botao_continuar_rect.x + (self.botao_continuar_rect.width - texto_continuar.get_width()) // 2
        text_y = self.botao_continuar_rect.y + 15
        tela.blit(texto_continuar, (text_x, text_y))