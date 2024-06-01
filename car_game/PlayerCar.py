import pygame
from pygame.locals import *

from car_game import *
from car_game.Car import AbstractCar


PURPLE_CAR = pygame.image.load("car_game/imgs/purple-car.png")


class PlayerCar(AbstractCar):
    IMG = PURPLE_CAR

    # Na colisão do carro controlado pelo jogador, o carro é jogado na direção oposta.
    def on_collision(self, **kwargs):
        self.vel = -self.vel
        self.update_pos()
    
    # Movimento controlado pelas teclas w, a, s, d.
    def move(self, **kwargs):
        keys = pygame.key.get_pressed()
        moved = False

        if keys[pygame.K_a]:
            self.rotate(left=True)
        
        if keys[pygame.K_d]:
            self.rotate(right=True)
        
        if keys[pygame.K_w]:
            moved = True
            self.move_forward()
        elif keys[pygame.K_s]:
            moved = True
            self.move_backward()

        if not moved:
            self.reduce_speed()
