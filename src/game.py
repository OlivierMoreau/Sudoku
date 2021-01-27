import random

import pygame

from src.grid import Grid


class Game(object):

    def __init__(self, screen, difficulty="normal"):
        self.difficulty = difficulty
        self.screen = screen
        self.grid = Grid(self.screen, self.difficulty)
        self.solved = False  # Bool indicate if solver was used

        # sounds
        self.valid_sound = pygame.mixer.Sound('./sounds/confirmation.ogg')
        self.error_sound = pygame.mixer.Sound('./sounds/error.ogg')

    # Checks all user inputs and colors values
    def check_user_input(self):

        # flag for all user inputs
        all_valid = True

        for cell in self.grid.cells:
            if cell.state["user_input"]:
                if cell.value == cell.final_val:
                    cell.confirm(self.screen, True)
                else:
                    all_valid = False
                    cell.confirm(self.screen, False)
        if all_valid:
            pygame.mixer.Sound.play(self.valid_sound)
        else:
            pygame.mixer.Sound.play(self.error_sound)

    # Checks the validity of the full grids
    def final_check(self):
        ret = False
        for cell in self.grid.cells:
            if cell.value == cell.final_val:
                ret = True
            else:
                return False
        return ret

    # Finds a random cell and gives the answer
    def give_hint(self, screen):
        looping = True
        while looping:
            print("looking for a cell")
            cell = random.choice(self.grid.cells)
            if cell.value == 0 and cell.state["original"] is False:
                cell.value = cell.final_val
                cell.state["hint"] = True
                cell.draw(screen)
                looping = False
