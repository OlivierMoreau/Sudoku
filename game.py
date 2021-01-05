'''A sudoku game made using object oriented programing'''
import pygame, random


class Game(object):
    '''Game instance'''

    def __init__(self, screen, difficulty="normal"):
        self.difficulty = difficulty
        self.screen = screen
        self.grid = ""
        self.solved = False # Bool indicate if solver was used

    # Checks all user inputs and colors values
    def check_user_input(self):
        for cell in self.grid.cells:
            if cell.state["user_input"] == True:
                if cell.value == cell.final_val:
                    cell.confirm(self.screen, True)
                else:
                    cell.confirm(self.screen, False)

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
            if cell.value == 0 and cell.state["original"] == False:
                cell.value = cell.final_val
                cell.state["hint"] = True
                cell.draw(screen)
                looping = False
