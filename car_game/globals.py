import pygame
from pygame.locals import *

pygame.font.init()

# Variáveis globais.

def show_display():
    global WIN
    WIN = pygame.display.set_mode((WIDTH, HEIGHT), flags=SHOWN)
    pygame.display.set_caption("AI Playground")


def hide_display():
    global WIN
    WIN = pygame.display.set_mode((WIDTH, HEIGHT), flags=HIDDEN)


ROOT_PATH = "car_game"
IMAGES_PATH = f"{ROOT_PATH}/imgs"
MODELS_PATH = f"{ROOT_PATH}/ai_models"

BACKGROUND = pygame.image.load(f"{IMAGES_PATH}/background.png")

TRACK = None
TRACK_MASK = None

WIDTH, HEIGHT = BACKGROUND.get_width(), BACKGROUND.get_height()
WIN = None

CAR_SIZE = 1

START_POS = (0, 0)

STAT_FONT = pygame.font.SysFont("comicsans", 50)

FPS = 60

GEN = 0
DRAW_ALL_CARS = True

hide_display()
