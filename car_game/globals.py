import pygame
from pygame.locals import *

pygame.font.init()

BACKGROUND = pygame.image.load("car_game/imgs/track-bg.png")

TRACK = None
TRACK_MASK = None

WIDTH, HEIGHT = BACKGROUND.get_width(), BACKGROUND.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

CAR_SIZE = 1

START_POS = (0, 0)

STAT_FONT = pygame.font.SysFont("comicsans", 50)

FPS = 60

GEN = 0
DRAW_ALL_CARS = True

pygame.display.set_caption("AI Playground")