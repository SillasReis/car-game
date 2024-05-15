import math
import time

import pygame
from pygame.locals import *

from utils import scale_image, blit_rotate_center


BACKGROUND = pygame.image.load("car_game/imgs/track-bg.png")
CAR = pygame.image.load("car_game/imgs/red-car.png")
FPS = 60


class AbstractCar:
    def __init__(self, x, y, car_factor):
        self.img = scale_image(self.IMG, car_factor)
        self.max_vel = 6
        self.vel = 0
        self.rotation_vel = 6
        self.angle = 90
        self.x, self.y = x, y
        self.acceleration = 0.1
        self.alive = True
        self.radars_readings = {}

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)
    
    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()
    
    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal
    
    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi


class PlayerCar(AbstractCar):
    IMG = CAR
    
    def bounce(self):
        self.vel = -self.vel
        self.move()
        self.alive = False
    
    def radar(self, win, radar_angle):
        length = 0
        
        rect = self.img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)    
        x = int(rect.center[0])
        y = int(rect.center[1])

        while not win.get_at((x, y)) == pygame.Color(255, 255, 255, 255) and length < 200:
            length += 1
            x = int(rect.center[0] + math.cos(math.radians(self.angle + radar_angle + 90)) * length)
            y = int(rect.center[1] - math.sin(math.radians(self.angle + radar_angle + 90)) * length)

        self.radars_readings[radar_angle] = length

        pygame.draw.line(win, (0, 255, 0, 255), rect.center, (x, y), 1)
        pygame.draw.circle(win, (0, 0, 255, 255), (x, y), 3)


def draw(win, images, player_car):
    for img, pos in images:
        win.blit(img, pos)
    
    player_car.draw(win)

    for radar_angle in (-60, -30, 0, 30, 60):
        player_car.radar(win, radar_angle)
    
    print(player_car.radars_readings)

    pygame.display.update()


def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()


def main(track_file: str, start_pos: tuple, car_factor: float):
    track = pygame.image.load(f"car_game/imgs/{track_file}")
    track_mask = pygame.mask.from_surface(track)

    widht, height = track.get_width(), track.get_height()
    win = pygame.display.set_mode((widht, height))
    
    pygame.display.set_caption("AI Playground")

    run = True
    clock = pygame.time.Clock()
    images = [
        (BACKGROUND, (0, 0)),
        (track, (0, 0))
    ]
    player_car = PlayerCar(*start_pos, car_factor)

    while run:
        clock.tick(FPS)

        draw(win, images, player_car)

        for event in  pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    run = False
                    break
        
        move_player(player_car)

        if player_car.collide(track_mask) != None:
            player_car.bounce()

    pygame.quit()


if __name__ == "__main__":
    main("track-1.png", (600, 70), 0.5)