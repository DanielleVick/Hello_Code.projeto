# teste_audio_screen.py — teste detalhado para áudio 
import os
import time
import sys
import pygame
from utils_audio import init_audio, load_sound, play_sound  

# ---------------- init ordenado ----------------
# importante: antes de pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

print("pygame version:", pygame.version.ver)
print("Chamando pygame.mixer.get_init() agora ->", pygame.mixer.get_init())

# cria janela simples
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Teste de Áudio - Debug")

ASSETS = os.path.join(os.path.dirname(__file__), "assets", "sounds")
f_erro = os.path.join(ASSETS, "erro.mp3")
f_point = os.path.join(ASSETS, "vitoriafinal.mp3")
f_vitoria = os.path.join(ASSETS, "faseconcluida.mp3")

print("Caminhos de arquivo:")
print(" - erro:", f_erro, os.path.isfile(f_erro))
print(" - point:", f_point, os.path.isfile(f_point))
print(" - vitoria:", f_vitoria, os.path.isfile(f_vitoria))


def try_sound_load(path):
    try:
        s = pygame.mixer.Sound(path)
        print(f"Carregou Sound OK: {path} — length {s.get_length():.2f}s")
        ch = s.play()
        print("play() retornou canal:", ch)
        return True
    except Exception as e:
        print("Erro ao carregar/rodar Sound:", e)
        return False


def try_music_load(path):
    try:
        pygame.mixer.music.load(path)
        print("music.load OK:", path)
        pygame.mixer.music.play()
        print("music.play chamado")
        return True
    except Exception as e:
        print("Erro ao carregar/rodar music:", e)
        return False


# Inicializa nosso init_audio (se usar utils_audio)
try:
    ok = init_audio()
    print("init_audio() retornou:", ok)
except Exception as e:
    print("init_audio() levantou exceção:", e)

# Estado inicial do mixer
print("mixer.get_init():", pygame.mixer.get_init())
print("mixer.get_num_channels():", pygame.mixer.get_num_channels())
print("mixer.get_busy():", pygame.mixer.get_busy())

print("\n=== Tentando carregar como pygame.mixer.Sound (erro.mp3) ===")
ok1 = try_sound_load(f_erro)
time.sleep(1.5)
print("mixer.get_busy() após Sound.play():", pygame.mixer.get_busy())

print("\n=== Tentando carregar via pygame.mixer.music (point) ===")
ok2 = try_music_load(f_point)
time.sleep(1.5)
print("mixer.get_busy() após music.play():", pygame.mixer.get_busy())

print("\n=== TENTATIVA FINAL: tocar o som via utils_audio.play_sound (se disponível) ===")
try:
    play_sound("error")
    print("Chamado play_sound('error') — verifique se você ouve algo")
except Exception as e:
    print("play_sound('error') levantou exceção:", e)

print("\n--- DEBUG INSTRUÇÕES ---")
print("Se você não ouviu nada:")
print(" 1) verifique volume do Windows e dispositivo de saída (alto-falantes / fones).")
print(" 2) veja mensagens de erro acima (erros de decoder significam problema com MP3).")
print(" 3) se houver erro relacionado a MP3, converta para WAV e carregue esse .wav.")
print("\nFeche a janela para terminar o teste (ou pressione ESC).")

# loop simples para manter a janela aberta e permitir ver logs
running = True
clock = pygame.time.Clock()
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False
    # desenha algo simples
    screen.fill((0, 0, 0))
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit(0)
