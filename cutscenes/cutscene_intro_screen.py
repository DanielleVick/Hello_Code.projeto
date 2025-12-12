import pygame
import os


class CutsceneIntroScreen:
    """
    Cutscene usada ANTES da Fase 1.
    Imagens: imagem1.jpg ... imagem7.jpg
    Retorna 'INICIAR_FASE_1' quando terminar.
    """

    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura

        base = os.path.dirname(__file__)
        assets = os.path.normpath(os.path.join(base, "..", "assets"))

        # carregar imagens 1..7 (se não existirem, cria placeholder)
        self.imagens = []
        for i in range(1, 8):
            path = os.path.join(assets, f"imagem{i}.jpg")
            if os.path.exists(path):
                img = pygame.image.load(path).convert()
                img = pygame.transform.smoothscale(
                    img, (self.largura, self.altura))
            else:
                img = pygame.Surface((self.largura, self.altura))
                img.fill((30, 30, 30))
            self.imagens.append(img)

        # === TEXTOS ORIGINAIS (restaurados exatamente como você forneceu) ===
        self.textos_por_imagem = [
            # imagem1
            ["NARRAÇÃO: Era tarde da noite quando Nayara voltou ao laboratório. Ela sabia que testar o NexusMind sozinha não era a melhor ideia... ...mas a curiosidade era maior."],

            # imagem2 (coleman + narração + fala da Nayara) -> separados em trechos
            [
                "NARRAÇÃO: O NexusMind era o novo sistema de interface neural, capaz de enviar a consciência para uma realidade simulada.",
                "Colega: Tchau Nayara! Vê se não faz nenhuma besteira sozinha!",
                "NAYARA: Eu? Fazer besteira?...Jamais, besteira e meu nome nunca se juntaram em uma frase."
            ],

            # imagem3
            [
                "NARRAÇÃO: Nayara respira fundo, coloca a tiara neural e inicia o processo de conexão...",
                "NAYARA: Tudo funcionando direitinho, bora bixo, quero ver se tu funciona mesmo..."
            ],

            # imagem4
            ["NARRAÇÃO: Algo dá errado. A energia oscila. Luzes piscam. O sistema sobrecarrega."],

            # imagem5 (tela branca)
            ["NARRAÇÃO: Um clarão toma tudo. Silêncio. Vazio."],

            # imagem6 (acorda na floresta) — separa narração e depois fala/diálogo
            [
                "NARRAÇÃO: Nayara abre os olhos em uma floresta estranha. Árvores brilhavam com circuitos. O vento soava como dados passando.",
            ],

            # imagem7 (aqui entra o diálogo engraçado com Araci; vários trechos)
            [
                "ARACI: Ave Maria, menina! Tu caiu do céu foi? Que estrondo da gota foi aquele?!",
                "NAYARA: Oxi… e tu é quem, criatura?",
                "ARACI: Eu? Araci, guardiã dessa floresta tecnológica todinha! E tu tá mais perdida que cego em tiroteio.",
                "NAYARA: Vixe… se eu te disser, tu não acredita… tava no meu laboratório e vim parar aqui do nada.",
                "ARACI: Bom, se tu quiser voltar pra tua realidade... ",
                "ARACI: vai ter que passar por alguns desafios, mas vai ter ajuda de quem tá lendo isso agora. Boa sorte pra vocês!",
                "NAYARA: Tá né...sei nem quem tu é, mas bora lá"
            ]
        ]
        # =====================================================================

        # índices e controles
        self.img_idx = 0                   # qual imagem (0..n-1)
        self.trecho_idx = 0                # qual trecho dentro da imagem
        self.char_index = 0                # animação de digitação
        self.chars_per_tick = 2
        self.clock = pygame.time.Clock()
        self.retorno = None

        # flags para evitar reenvio repetido do resultado
        self._finished = False
        self._reported_finished = False

        # fonte (PressStart2P)
        font_path = os.path.join(assets, "PressStart2P-Regular.ttf")
        if os.path.exists(font_path):
            self.font = pygame.font.Font(font_path, 14)
        else:
            self.font = pygame.font.SysFont("consolas", 16)

        # área de texto
        self.margin_x = 28
        self.margin_y = 420
        self.text_width = self.largura - self.margin_x*2

        # DEBUG opcional: comente se não quiser
        # print(f"[DEBUG] CutsceneIntro: imagens={len(self.imagens)} textos={len(self.textos_por_imagem)}")

    def _wrap_text(self, text):
        words = text.split(' ')
        lines = []
        cur = ""
        for w in words:
            test = (cur + " " + w).strip()
            if self.font.size(test)[0] <= self.text_width:
                cur = test
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    def lidar_com_eventos(self, event):
        # Se já terminou e já reportamos, não retornamos mais (evita loop)
        if self._finished and self._reported_finished:
            return None

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                # Segurança: se não houver imagens, termina
                if not self.imagens:
                    self._finished = True
                    if not self._reported_finished:
                        self._reported_finished = True
                        return "INICIAR_FASE_1"
                    return None

                # Proteções para índices de texto/imagem
                if self.img_idx >= len(self.imagens):
                    self._finished = True
                    if not self._reported_finished:
                        self._reported_finished = True
                        return "INICIAR_FASE_1"
                    return None

                trechos = self.textos_por_imagem[self.img_idx] if self.img_idx < len(
                    self.textos_por_imagem) else [""]
                if self.trecho_idx >= len(trechos):
                    self.trecho_idx = 0

                texto_total = trechos[self.trecho_idx]
                if self.char_index < len(texto_total):
                    # completa o trecho atual
                    self.char_index = len(texto_total)
                else:
                    # avança para o próximo trecho da mesma imagem (se houver)
                    self.trecho_idx += 1
                    self.char_index = 0
                    if self.trecho_idx >= len(trechos):
                        # avança imagem
                        self.img_idx += 1
                        self.trecho_idx = 0
                        self.char_index = 0
                        # se passou da última imagem, assinala retorno e marca finished
                        if self.img_idx >= len(self.imagens):
                            self._finished = True
                            if not self._reported_finished:
                                self._reported_finished = True
                                return "INICIAR_FASE_1"
        return None

    def atualizar(self):
        # Se já terminou, nada a atualizar
        if self._finished:
            return

        # Proteção: se não há imagens, nada a fazer
        if not self.imagens:
            return

        # Garante img_idx válido (defensivo)
        if self.img_idx >= len(self.imagens):
            self.img_idx = len(self.imagens) - 1
            self._finished = True
            return

        # Obter trechos da imagem atual (proteção caso listas sejam inconsistentes)
        trechos = self.textos_por_imagem[self.img_idx] if self.img_idx < len(
            self.textos_por_imagem) else [""]
        if not trechos:
            return

        # Garante trecho_idx válido
        if self.trecho_idx >= len(trechos):
            self.trecho_idx = 0

        texto_total = trechos[self.trecho_idx]
        if self.char_index < len(texto_total):
            self.char_index += self.chars_per_tick
            if self.char_index > len(texto_total):
                self.char_index = len(texto_total)

    def desenhar(self, surface):
        # Proteção: se não há imagens, desenha fundo vazio e retorna
        if not self.imagens:
            surface.fill((0, 0, 0))
            return

        # Ajusta img_idx se por alguma razão estiver fora do intervalo
        if self.img_idx >= len(self.imagens):
            self.img_idx = len(self.imagens) - 1
            if self._finished:
                return

        # desenha imagem atual
        img = self.imagens[self.img_idx]
        surface.blit(img, (0, 0))

        # texto do trecho atual (com proteções)
        trechos = self.textos_por_imagem[self.img_idx] if self.img_idx < len(
            self.textos_por_imagem) else [""]
        if not trechos:
            return

        if self.trecho_idx >= len(trechos):
            self.trecho_idx = 0

        texto_total = trechos[self.trecho_idx][:self.char_index]
        linhas = self._wrap_text(texto_total)

        # fundo semi-transparente para caixa de texto
        s = pygame.Surface((self.text_width+20, 120), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        pygame.draw.rect(s, (100, 140, 200), s.get_rect(), 2, border_radius=6)
        surface.blit(s, (self.margin_x-10, self.margin_y-10))

        # desenhar linhas (até 5)
        for i, l in enumerate(linhas[:5]):
            txt = self.font.render(l, True, (255, 255, 255))
            surface.blit(txt, (self.margin_x, self.margin_y + i*20))

        # indicador (quando trecho completo)
        if self.char_index >= len(trechos[self.trecho_idx]):
            tri = self.font.render("PRESS SPACE", True, (200, 200, 200))
            surface.blit(tri, (self.largura - 150, self.altura - 40))
