from enum import Enum

from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import button_dialog, radiolist_dialog

from car_game import globals
from car_game.run_ai import play
from car_game.Track import tracks
from car_game.train_ai import train_ai
from car_game.utils import get_files_with_prefix


class GameMode(Enum):
    TRAINING = "Treinamento"
    PLAYING = "Execução"


def mode_selection():
    result = radiolist_dialog(
        title="AI Car",
        text="Escolha o modo:",
        values=[(game_mode, game_mode.value) for game_mode in GameMode],
        cancel_text="Close"
    ).run()

    return result


def track_selection():
    result = radiolist_dialog(
        title="AI Car",
        text="Escolha a pista:",
        values=[(track, track.name) for track in tracks]
    ).run()

    return result


def model_selection():
    models = [
        model.split("/")[-1]
        for model in get_files_with_prefix(globals.MODELS_PATH, "neat_model_")
    ]

    result = radiolist_dialog(
        title="AI Car",
        text="Escolha o modelo para execução:",
        values=[(model, model.replace(".pkl", "")) for model in models]
    ).run()

    return result


if __name__ == "__main__":
    while True:
        mode = mode_selection()
        if not mode:
            break
        
        track = track_selection()
        if not track:
            continue

        match (mode):
            case GameMode.TRAINING:
                globals.show_display()
                train_ai(track.track_file, track.car_size, track.start_pos)
                globals.hide_display()
            case GameMode.PLAYING:
                model = model_selection()
                if not model:
                    continue

                globals.show_display()
                play(track.track_file, track.car_size, track.start_pos, model)
                globals.hide_display()
