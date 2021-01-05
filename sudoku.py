
import pygame, random, pickle, os
from engine import *
from reader import *
from game import *
from grid import *


def main():

    pygame.init()
    pygame.display.set_caption("Sudoku")
    size = (800, 500)
    screen = pygame.display.set_mode(size)
    screen.fill((255,255,255))
    icon = pygame.image.load('imgs/icone.ico')
    pygame.display.set_icon(icon)

    # Checks if there's a saved file
    if os.stat("data/tempsave.data").st_size != 0:

        engine = Engine(screen)
        engine.game = Game(screen)
        game = engine.game
        engine.load_state()
        game.grid.make_grid_struct(False)
        game.grid.draw(screen)
        for cell in game.grid.cells:
            cell.draw(screen)
        engine.start()
    else:
        print("no save file")
        grid_pick = random.randrange(150)
        rot_pick = random.randrange(4)
        read = Reader(grid_pick, rot_pick)
        grid, full_grid = read.grid_picker()

        engine = Engine(screen)
        engine.game = Game(engine.screen)
        game = engine.game
        game.grid = Grid(grid)
        game.grid.full_grid = full_grid
        game.grid.make_grid_struct()
        game.grid.draw(game.screen)
        game.grid.set_vals(engine.screen)
        engine.start()


# Transforms list of lists into one list with 2 for loops
def forfor(a):
    return [item for sublist in a for item in sublist]

if __name__ == '__main__':
    main()
