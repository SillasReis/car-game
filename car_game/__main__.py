from car_game.run_ai import play
from car_game.train_ai import train_ai


# TODO: Fazer menu com opções para: treinar e jogar. (PODE SER no CLI mesmo)
####### No caso de jogar, possibilitar escolha de modelo treinado e pista.

if __name__ == "__main__":
    # Track 1
    # track_file = "track-1.png"
    # car_size = 0.5
    # start_pos = (600, 70)

    # Track 2
    # track_file = "track-2.png"
    # car_size = 0.5
    # start_pos = (700, 70)

    # Track 3
    track_file = "track-3.png"
    car_size = 0.5
    start_pos = (500, 260)

    # train_ai(track_file, car_size, start_pos)
    play(track_file, car_size, start_pos, "neat_model_1715825448.9561605.pkl")

