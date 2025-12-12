import pygame
import os

class CutsceneFinalScreen:
    """
    Cutscene final completa com 6 imagens (imagem8.png – imagem13.png)
    Cada imagem possui vários trechos de texto exibidos um por vez.
    """

    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura

        base = os.path.dirname(__file__)
        assets = os.path.normpath(os.path.join(base, "..", "assets"))

        # ----------- CARREGAR IMAGENS -----------
        self.imagens = []
        for i in range(8, 14):  # 8,9,10,11,12,13
            path = os.path.join(assets, f"imagem{i}.png")
            if os.path.exists(path):
                img = pygame.image.load(path).convert()
                img = pygame.transform.smoothscale(img, (self.largura, self.altura))
            else:
                img = pygame.Surface((self.largura, self.altura))
                img.fill((10, 10, 10))
            self.imagens.append(img)

        # ----------- TEXTOS POR IMAGEM -----------
        self.textos_por_imagem = [

            #  8 — Nayara + Araci no templo
            [
                "NARRAÇÃO: Depois de tudo que viveu, Nayara sentou-se ao lado de Araci no templo. "
                "O vento soprava leve, como se a própria mata estivesse ouvindo.",

                "ARACI: Vocês se saíram bem, viu? Cada desafio que enfrentaram... "
                "eu só fiz mostrar o caminho. Mas quem trilhou foram vocês dois.",

                "NAYARA: Então não foi só eu que viajei, né? Valeu mesmo... vocês me salvaram."
            ],

            #  9 — Portal se abrindo
            [
                "NARRAÇÃO: O templo tremeu suave. Linhas de energia se juntaram diante das duas, "
                "desenhando um portal.",

                "ARACI: É chegada a hora. A tua estrada continua... noutra banda.",

                "NAYARA: Tô pronta. Quer dizer... acho que tô."
            ],

            #  10 — Luz tomando conta
            [
                "NARRAÇÃO: A luz do portal cresceu, engolindo tudo ao redor. O ar vibrava como se respirasse.",

                "NARRAÇÃO: Nayara sentiu um puxão no peito. Não era medo — era só uma sensação estranha."
            ],

            #  11 — Nayara caindo no portal
            [
                "NARRAÇÃO: No meio do caminho entre mundos, o tempo deixou de existir.",

                "NARRAÇÃO: Formas, cores, memórias... tudo girava ao redor.",

                "NARRAÇÃO: E algo começou a acontecer... dentro dela."
            ],

            #  12 — Voltando ao laboratório
            [
                "NARRAÇÃO: De repente, o impacto. Nayara caiu de volta na cadeira do laboratório "
                "como se tivesse sido arremessada do céu.",

                "NARRAÇÃO: O laboratório estava exatamente igual... mas ela não.",
                
                "NAYARA: Oxi... foi sonho? Realidade? Eu tô ficando doida?"
            ],

            # 13 — No banheiro, mecha roxa
            [
                "NARRAÇÃO: Ofegante, ela correu até o banheiro. Lavou o rosto. "
                "Tentou se convencer de que nada daquilo tinha sido real.",

                "NARRAÇÃO: Mas quando levantou a cabeça...",
                
                "NAYARA: Como assim... meu cabelo...?",

                "NARRAÇÃO: No reflexo, uma mecha roxa brilhava. "
                "Um pedaço do outro mundo... que voltou com ela.",

                "NARRAÇÃO: Esse foi o fim da jornada. Ou talvez... só o começo."
            ]
        ]

        # ----------- CONTROLES DA CUTSCENE -----------
        self.img_idx = 0
        self.trecho_idx = 0
        self.char_index = 0
        self.chars_per_tick = 2

        # fonte
        font_path = os.path.join(assets, "PressStart2P-Regular.ttf")
        if os.path.exists(font_path):
            self.font = pygame.font.Font(font_path, 14)
        else:
            self.font = pygame.font.SysFont("consolas", 16)

        self.margin_x = 28
        self.margin_y = 420
        self.text_width = self.largura - self.margin_x * 2

        self.retorno = None

    # -------------------------------------------------
    def _wrap_text(self, text):
        words = text.split(" ")
        lines, cur = [], ""
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

    # -------------------------------------------------
    def lidar_com_eventos(self, event):
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN):

            texto_total = self.textos_por_imagem[self.img_idx][self.trecho_idx]

            # Se o texto ainda está revelando
            if self.char_index < len(texto_total):
                self.char_index = len(texto_total)
                return None

            # Próximo trecho
            self.trecho_idx += 1
            self.char_index = 0

            # Se acabou os trechos da imagem atual
            if self.trecho_idx >= len(self.textos_por_imagem[self.img_idx]):
                self.img_idx += 1
                self.trecho_idx = 0
                self.char_index = 0

                # Acabaram as imagens → finalizar
                if self.img_idx >= len(self.imagens):
                    self.retorno = "FINALIZAR_JOGO"
                    return self.retorno

        return None

    # -------------------------------------------------
    def atualizar(self):
        trechos = self.textos_por_imagem[self.img_idx]
        texto_total = trechos[self.trecho_idx]

        if self.char_index < len(texto_total):
            self.char_index += self.chars_per_tick

    # -------------------------------------------------
    def desenhar(self, surface):
        # fundo
        surface.blit(self.imagens[self.img_idx], (0, 0))

        trechos = self.textos_por_imagem[self.img_idx]
        texto_total = trechos[self.trecho_idx][:self.char_index]
        linhas = self._wrap_text(texto_total)

        caixa = pygame.Surface((self.text_width + 20, 150), pygame.SRCALPHA)
        caixa.fill((0, 0, 0, 170))
        pygame.draw.rect(caixa, (150, 180, 255), caixa.get_rect(), 2, border_radius=8)
        surface.blit(caixa, (self.margin_x - 10, self.margin_y - 10))

        for i, l in enumerate(linhas[:6]):
            txt = self.font.render(l, True, (255, 255, 255))
            surface.blit(txt, (self.margin_x, self.margin_y + i * 22))

        # indicador
        texto_final = trechos[self.trecho_idx]
        if self.char_index >= len(texto_final):
            tri = self.font.render("PRESS SPACE", True, (220, 220, 220))
            surface.blit(tri, (self.largura - 260, self.altura - 50))
