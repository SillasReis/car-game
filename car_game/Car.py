import math

import pygame
from pygame.locals import *

from car_game import globals
from car_game.utils import scale_image, blit_rotate_center


class AbstractCar:
    def __init__(self, x, y):
        self.img = scale_image(self.IMG, globals.CAR_SIZE)
        self.max_vel = 10
        self.vel = 0
        self.rotation_vel = 10
        self.angle = 90
        self.x, self.y = x, y
        self.acceleration = 1
        self.radars_readings = {}
        self.radars_collisions = {}
        self.score = 0
        self.rect = None
        self.update_rect()

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)
        
        for x, y in self.radars_collisions.values():
            pygame.draw.line(win, (0, 255, 0, 255), self.rect.center, (x, y), 1)
            pygame.draw.circle(win, (0, 0, 255, 255), (x, y), 3)
    
    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.update_pos()
    
    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
        self.update_pos()

    def update_rect(self):
        self.rect = self.img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)

    def update_pos(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

        self.update_rect()
    
    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.update_pos()

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi
    
    def on_collision(self, **kwargs):
        pass

    def move(self, **kwargs):
        pass