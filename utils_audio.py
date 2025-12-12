# utils_audio.py
import os
import pygame

AUDIO_INITIALIZED = False
SOUNDS = {}   # dict: nome -> pygame.mixer.Sound


def init_audio(frequency=44100, size=-16, channels=2, buffer=512):
    global AUDIO_INITIALIZED

    if AUDIO_INITIALIZED:
        return True

    try:
        pygame.mixer.pre_init(frequency, size, channels, buffer)
        pygame.init()
        pygame.mixer.init()
        AUDIO_INITIALIZED = True
        print(">>> Áudio inicializado com sucesso")
        return True
    except Exception as e:
        print(f"Aviso: não foi possível inicializar áudio: {e}")
        AUDIO_INITIALIZED = False
        return False


def load_sound(name, filepath):
    if not init_audio():
        return False

    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"Arquivo de som não encontrado: {filepath}")

    try:
        snd = pygame.mixer.Sound(filepath)
        SOUNDS[name] = snd
        print(f"Som carregado OK: {name}")
        return True
    except Exception as e:
        raise RuntimeError(f"Erro ao carregar som '{filepath}': {e}")


def play_sound(name, volume=1.0):
    snd = SOUNDS.get(name)
    if not snd:
        print(f"(Atenção) Som '{name}' não encontrado em SOUNDS.")
        return

    try:
        snd.set_volume(max(0.0, min(1.0, volume)))
        snd.play()
        print(f"Tocando som: {name}")
    except Exception as e:
        print(f"Falha ao tocar som '{name}': {e}")


def stop_all_sounds():
    try:
        pygame.mixer.stop()
    except Exception:
        pass


def set_global_sfx_volume(vol):
    vol = max(0.0, min(1.0, vol))
    for s in SOUNDS.values():
        s.set_volume(vol)
