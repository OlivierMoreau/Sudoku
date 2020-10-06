from src.dependency import *
from src.reader import *
from src.game import *
from src.blocks import *
from src.tempreader import *

def main():

    pygame.init()
    pygame.display.set_caption("Sudoku")
    size = (800, 500)
    screen = pygame.display.set_mode(size)
    screen.fill((255,255,255))
    icon = pygame.image.load('graphics/icone.png')
    pygame.display.set_icon(icon)

    # Checks if there's a saved file
    if not os.path.isfile("data/tempsave.data"):
        open("data/tempsave.data", "w+")



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

        grid, full_grid = grid_picker(grid_pick, rot_pick)

        engine = Engine(screen)
        engine.game = Game(engine.screen)
        game = engine.game
        game.grid = Grid(grid)
        game.grid.full_grid = full_grid
        game.grid.make_grid_struct()
        game.grid.draw(game.screen)
        game.grid.set_vals(engine.screen)
        engine.start()



if __name__ == '__main__':
    main()
