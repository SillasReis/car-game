import neat
import pickle

import neat.nn.feed_forward
import pygame
from pygame.locals import *

from car_game import globals
from car_game.exceptions import InterruptException
from car_game.Game import Game
from car_game.AICar import AICar
from car_game.PlayerCar import PlayerCar


def create_neural_network(genome, config):
    return neat.nn.FeedForwardNetwork.create(genome, config)


def run(network):
    globals.GEN += 1

    game = Game("Running")

    cars = [AICar(*globals.START_POS), PlayerCar(*globals.START_POS)]

    while game.run:
        game.clock_tick()
        game.handle_events()
        game.handle_keys()
        game.draw(cars)

        for car in cars:
            car.move(network=network)
            
            if car.collide(globals.TRACK_MASK) != None:
                car.on_collision(mode="Running")
        
        if len(cars) == 0:
            game.run = False
            break


# Executa o jogo no modo de uso de execução da IA
def play(track_file, car_size, start_pos, model_file):
    globals.TRACK = pygame.image.load(f"car_game/imgs/{track_file}")
    globals.TRACK_MASK = pygame.mask.from_surface(globals.TRACK)
    globals.CAR_SIZE = car_size
    globals.START_POS = start_pos
    globals.FPS = 60

    with open(f"car_game/ai_models/{model_file}", "rb") as f:
        config, genome = pickle.load(f)
    
    network = create_neural_network(genome, config)
    
    try:
        run(network)
    except InterruptException:
        pass
