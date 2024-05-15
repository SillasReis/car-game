import math
import neat
import os
import time

import neat.nn.feed_forward
import pygame
from pygame.locals import *

from utils import scale_image, blit_rotate_center


pygame.font.init()


BACKGROUND = pygame.image.load("car_game/imgs/track-bg.png")

TRACK = pygame.image.load(f"car_game/imgs/track-2.png")
TRACK_MASK = pygame.mask.from_surface(TRACK)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

CAR = scale_image(pygame.image.load("car_game/imgs/red-car.png"), 0.5)

STAT_FONT = pygame.font.SysFont("comicsans", 50)

FPS = 60

SHOW_ALL = True

GEN = 0

pygame.display.set_caption("AI Playground")


class AbstractCar:
    def __init__(self, x, y):
        self.img = self.IMG
        self.max_vel = 10
        self.vel = 0
        self.rotation_vel = 10
        self.angle = 90
        self.x, self.y = x, y
        self.acceleration = 1
        self.alive = True
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
        self.move()
    
    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
        self.move()

    def update_rect(self):
        self.rect = self.img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

        self.update_rect()
    
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
    
    def radar(self):
        for radar_angle in (-60, -30, 0, 30, 60):
            length = 0

            x = int(self.rect.center[0])
            y = int(self.rect.center[1])

            try:
                while not TRACK.get_at((x, y)) == pygame.Color(255, 255, 255, 255) and length < 150:
                    length += 1
                    x = int(self.rect.center[0] + math.cos(math.radians(self.angle + radar_angle + 90)) * length)
                    y = int(self.rect.center[1] - math.sin(math.radians(self.angle + radar_angle + 90)) * length)
            except IndexError:
                pass

            self.radars_collisions[radar_angle] = (x, y)

            self.radars_readings[radar_angle] = int(
                math.sqrt(math.pow(self.rect.center[0] - x, 2) + math.pow(self.rect.center[1] - y, 2))
            )


def draw(win, images, cars, gen):
    for img, pos in images:
        win.blit(img, pos)
    
    for car in cars:
        car.draw(win)

    text = STAT_FONT.render(f"Gen: {gen}", 1, (0, 0, 0))
    win.blit(text, (10, 10))

    pygame.display.update()


def move_car(player_car, genome):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
        genome.fitness += 2
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
        genome.fitness += 2
    if keys[pygame.K_w]:
        genome.fitness += 4
        moved = True
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()


def move_ai_car(player_car, genome, forward=False, backward=False, left=False, right=False):
    moved = False

    if left or right:
        genome.fitness -= 1
        player_car.rotate(left=left, right=right)
    
    if forward:
        genome.fitness += 5
        moved = True
        player_car.move_forward()
    elif backward:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()


def main(genomes, config):
    global GEN, SHOW_ALL
    GEN += 1

    # start_pos = (600, 70) # Track 1
    start_pos = (700, 70) # Track 2

    run = True
    clock = pygame.time.Clock()
    images = [
        (BACKGROUND, (0, 0)),
        (TRACK, (0, 0))
    ]
    
    nets = []
    ge = []
    cars = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        cars.append(PlayerCar(*start_pos))
        g.fitness = 0
        ge.append(g)

    while run:
        clock.tick(FPS)
        
        for event in  pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()
        
        if len(cars) == 0:
            run = False
            break

        keys = pygame.key.get_pressed()

        if keys[pygame.K_x]:
            run = False
            time.sleep(1)
            break
        if keys[pygame.K_z]:
            SHOW_ALL = bool(abs(SHOW_ALL - 1))
            time.sleep(1)

        if SHOW_ALL:
            draw(WIN, images, cars, GEN)
        else:
            best_fit_idx, _ = max(list(enumerate(ge)), key=lambda x: x[1].fitness)
            draw(WIN, images, [cars[best_fit_idx]], GEN)

        for idx, car in enumerate(cars):
            car.radar()
            
            outputs = nets[idx].activate(car.radars_readings.values())
            parsed_outputs = [output > 0.5 for output in outputs]

            move_ai_car(car, ge[idx], *parsed_outputs)
            
            if car.vel <= 0:
                ge[idx].fitness -= 5
            else:
                ge[idx].fitness += 3

            if car.collide(TRACK_MASK) != None:
                cars.pop(idx)
                nets.pop(idx)
                ge.pop(idx)


def run(config_path):
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 50)

    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
