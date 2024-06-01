import time

import pygame
from pygame.locals import *

from car_game import globals
from car_game.exceptions import InterruptException


# Classe para gerenciamento do jogo.
class Game:
    def __init__(self, mode):
        self.mode = mode
        self.clock = pygame.time.Clock()
        self.images = [
            (globals.BACKGROUND, (0, 0)),
            (globals.TRACK, (0, 0))
        ]
        self.run = True

    def clock_tick(self):
        self.clock.tick(globals.FPS)

    def handle_events(self):
        for event in  pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.run = False
                    pygame.quit()
                    quit()

    def handle_keys(self):
        keys = pygame.key.get_pressed()

        if self.mode == "Training":
            if keys[pygame.K_x]:
                self.run = False
                time.sleep(1)
            
            if keys[pygame.K_z]:
                globals.DRAW_ALL_CARS = bool(abs(globals.DRAW_ALL_CARS - 1))
                time.sleep(1)
            
        if keys[pygame.K_c]:
            time.sleep(1)
            raise InterruptException

    def draw(self, cars):
        for img, pos in self.images:
            globals.WIN.blit(img, pos)
    
        for car in cars:
            car.draw(globals.WIN)

        if self.mode == "Training":
            text = globals.STAT_FONT.render(f"Gen: {globals.GEN}", 1, (0, 0, 0))
            globals.WIN.blit(text, (10, 10))

        pygame.display.update()