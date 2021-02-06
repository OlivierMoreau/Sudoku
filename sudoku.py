import os

import pygame

from src.engine import Engine


def main():
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("Sudoku")
    size = (650, 380)
    screen = pygame.display.set_mode(size)
    screen.fill((220, 220, 220))
    icon = pygame.image.load('graphics/icone.png')
    pygame.display.set_icon(icon)

    # Checks if there's a saved file and creates an empty one if not
    if not os.path.isfile("data/tempsave.data"):
        print()
        open("data/tempsave.data", "w+")

    # load from save or starts from scratch
    if os.stat("data/tempsave.data").st_size != 0:
        engine = Engine(screen)
        engine.load_state()
        engine.start()

    else:
        print("no save file")
        engine = Engine(screen)
        engine.start()
        engine.new_game()


if __name__ == '__main__':
    main()
