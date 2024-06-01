import neat
import os
import pickle
from time import time

import neat.nn.feed_forward
import pygame
from pygame.locals import *

from car_game import globals
from car_game.exceptions import InterruptException
from car_game.Game import Game
from car_game.AICar import AICar


def eval_genomes(genomes, config):
    globals.GEN += 1

    game = Game("Training")
    
    nets = []
    ge = []
    cars = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        cars.append(AICar(*globals.START_POS))
        g.fitness = 0
        ge.append(g)

    while game.run:
        game.clock_tick()
        game.handle_events()
        game.handle_keys()

        if globals.DRAW_ALL_CARS:
            cars_to_draw = cars
        else:
            best_fit_idx, _ = max(list(enumerate(ge)), key=lambda x: x[1].fitness)
            cars_to_draw = [cars[best_fit_idx]]

        game.draw(cars_to_draw)

        for idx, car in enumerate(cars):
            car.move(network=nets[idx], genome=ge[idx])
            
            if car.vel <= 0:
                ge[idx].fitness -= 5
            else:
                ge[idx].fitness += 3

            if car.collide(globals.TRACK_MASK) != None:
                car.on_collision(car_idx=idx, cars=cars, nets=nets, genomes=ge, mode="Training")
        
        if len(cars) == 0:
            game.run = False
            break


# Executa o jogo no modo de treinamento
def train_ai(track_file, car_size, start_pos):
    globals.GEN = 0
    globals.TRACK = pygame.image.load(f"car_game/imgs/{track_file}")
    globals.TRACK_MASK = pygame.mask.from_surface(globals.TRACK)
    globals.CAR_SIZE = car_size
    globals.START_POS = start_pos
    globals.FPS = 1000

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")

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

    try:
        winner = p.run(eval_genomes, 50)
    except InterruptException:
        winner = p.best_genome
    
    with open(f"car_game/ai_models/neat_model_{time()}.pkl", "wb") as output:
        pickle.dump((config, winner), output, pickle.HIGHEST_PROTOCOL)

    print('\nBest genome:\n{!s}'.format(winner))
