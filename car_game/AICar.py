import math

import pygame
from pygame.locals import *

from car_game import globals
from car_game.Car import AbstractCar


RED_CAR = pygame.image.load("car_game/imgs/red-car.png")


# Definição de Carro próprio para rede neural.
class AICar(AbstractCar):
    IMG = RED_CAR
    
    # Quando um carro da rede neural colide, ele é excluído da lista de
    # carros da geração e seu genoma e arquitetura são excluídos de suas respectivas listas.
    def on_collision(self, **kwargs):
        mode = kwargs["mode"]

        car_idx = kwargs.get("car_idx")
        cars = kwargs.get("cars")
        nets = kwargs.get("nets")
        genomes = kwargs.get("genomes")

        if mode == "Training":
            cars.pop(car_idx)
            nets.pop(car_idx)
            genomes.pop(car_idx)

    # No caso do carro automático, sua movimentação é controlada pelos outputs da rede neural.
    # A rede neural, por sua vez, tem como inputs os valores de distância medidos pelos radares.
    def move(self, **kwargs):
        genome = kwargs.get("genome", None)
        net = kwargs["network"]

        self.radar()
            
        outputs = net.activate(self.radars_readings.values())
        forward, backward, left, right = [output > 0.5 for output in outputs]
        
        moved = False

        fitness_increment = 0

        # Os carros são levemente punidos por virar. A idéia é que os carros virem apenas quando for
        # necessário para continuarem vivos, evitando movimentos desnecessários.
        if left or right:
            fitness_increment -= 1
            self.rotate(left=left, right=right)
        
        # Os carros são generosamente recompensados quando vão para frente.
        if forward:
            fitness_increment += 5
            moved = True
            self.move_forward()
        elif backward:
            moved = True
            self.move_backward()

        if not moved:
            self.reduce_speed()
        
        # Caso um genoma tenha sido informado na chamada da função (modo de treino)
        # o fitness é ajustado.
        if genome:
            genome.fitness += fitness_increment

    
    # Calcula a distância entre o carro e os pontos de colisão em 5 ângulos diferentes.
    def radar(self):
        for radar_angle in (-60, -30, 0, 30, 60):
            length = 0

            x = int(self.rect.center[0])
            y = int(self.rect.center[1])

            try:
                while not globals.TRACK.get_at((x, y)) == pygame.Color(255, 255, 255, 255) and length < 150:
                    length += 1
                    x = int(self.rect.center[0] + math.cos(math.radians(self.angle + radar_angle + 90)) * length)
                    y = int(self.rect.center[1] - math.sin(math.radians(self.angle + radar_angle + 90)) * length)
            except IndexError:
                pass

            self.radars_collisions[radar_angle] = (x, y)

            self.radars_readings[radar_angle] = int(
                math.sqrt(math.pow(self.rect.center[0] - x, 2) + math.pow(self.rect.center[1] - y, 2))
            )
