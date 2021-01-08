import os
import random
import pygame
from src.engine import Engine
from src.game import Game
from src.reader import Reader


def main():

    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("Sudoku")
    size = (800, 500)
    screen = pygame.display.set_mode(size)
    screen.fill((255,255,255))
    icon = pygame.image.load('graphics/icone.png')
    pygame.display.set_icon(icon)
    # grids data reader
    reader = Reader()


    # Checks if there's a saved file and creates an empty one if not
    if not os.path.isfile("data/tempsave.data"):
        open("data/tempsave.data", "w+")

    # load from save or starts from scratch
    if os.stat("data/tempsave.data").st_size != 0:
        engine = Engine(screen)
        grid, full_grid = reader.grid_picker(0, 0)
        engine.game = Game(engine.screen, grid, full_grid)
        game = engine.game
        engine.load_state()
        game.grid.make_grid_struct(False)
        game.grid.draw(screen)
        for cell in game.grid.cells:
            cell.draw(screen)
        engine.start()
    else:
        print("no save file")
        grid_pick = random.randrange(reader.size()-1)
        rot_pick = random.randrange(4)
        grid, full_grid = reader.grid_picker(grid_pick, rot_pick)

        engine = Engine(screen)
        engine.game = Game(engine.screen, grid, full_grid)
        game = engine.game
        game.grid.make_grid_struct()
        game.grid.draw(game.screen)
        game.grid.set_vals(engine.screen)
        engine.start()



if __name__ == '__main__':
    main()
