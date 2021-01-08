import random

import pygame


from src.blocks import Row, Collumn, Square
from src.cell import Cell
from src.reader import Reader


def forfor(a):
    return [item for sublist in a for item in sublist]

class Grid(object):
    '''Game grid'''

    def __init__(self, screen):
        # Fetch a random grid on new game
        self.reader = Reader()
        self.grid_pick = random.randrange(self.reader.size() - 1)
        self.rot_pick = random.randrange(4)
        self.grid, self.full_grid = self.reader.grid_picker(self.grid_pick, self.rot_pick)


        self.screen = screen
        self.rows = []
        self.collumns = []
        self.squares = []
        self.cells = []
        self.selected_cell = None

        self.rect = pygame.Rect((10,10), (370, 370))

        self.make_grid_struct()

        self.set_vals()
        self.draw()

    def make_grid_struct(self):

        # create grid cells
        for x in range(81):
            self.cells.append(Cell())

        # fills rows and collumns with cells
        for x in range(9):
            row = Row()
            collumn = Collumn()

            for y in range(9):
                row.cells.append(self.cells[x + ((y) * 9)])
                self.cells[x + ((y) * 9)].parents['collumn'] = row
                collumn.cells.append(self.cells[y + ((x) * 9)])
                self.cells[y + ((x) * 9)].parents['row'] = collumn

            self.rows.append(collumn)
            self.collumns.append(row)

        # fills squares with cells
        for z in range(3):
            col = z * 3 # horizontal offset for the collumn
            for x in range(0, 9, 3): # vertical offset for the rows
                square = Square()
                for y in range(3):
                   square.cells.append(self.rows[x + y].cells[0 + col])
                   self.rows[x + y].cells[0 + col].parents['square'] = square
                   square.cells.append(self.rows[x + y].cells[1 + col])
                   self.rows[x + y].cells[1 + col].parents['square'] = square
                   square.cells.append(self.rows[x + y].cells[2 + col])
                   self.rows[x + y].cells[2 + col].parents['square'] = square
                self.squares.append(square)

        # set cells coordinates and make the rect
        x_axis = 10
        for coll in self.collumns:
            y_axis = 10
            for cell in coll.cells:
                cell.coordinates = (x_axis, y_axis)
                cell.rectangle = pygame.Rect(cell.coordinates, cell.size)
                y_axis += 40
            x_axis += 40

    # Set cells values from the pre-generated grid and draw them
    def set_vals(self):
        list_grid = forfor(self.grid)
        final_list = forfor(self.full_grid)
        for x in range(81):
            cell = self.cells[x]
            cell.clean(self.screen)
            cell.value = list_grid[x]
            cell.final_val = final_list[x]
            if list_grid[x] != 0:
                cell.state["original"] = True
            cell.draw(self.screen)
        # Add a clue if a block is empty
        for square in self.squares:
            if sum(square.get_values()) == 0:
                print("adding in square")
                cell = square.cells[random.randrange(1,9)]
                cell.value = cell.final_val
                cell.state["original"] = True
                cell.draw(self.screen)
        for row in self.rows:
            if sum(row.get_values()) == 0:
                print("adding in row")
                cell = row.cells[random.randrange(1,9)]
                cell.value = cell.final_val
                cell.state["original"] = True
                cell.draw(self.screen)
        for col in self.collumns:
            if sum(col.get_values()) == 0:
                print("adding in col")
                cell = col.cells[random.randrange(1,9)]
                cell.value = cell.final_val
                cell.state["original"] = True
                cell.draw(self.screen)


    # Draw grid and cells borders
    def draw(self):
            grid_rect = pygame.Rect((10,10),(360, 360))
            pygame.draw.rect(self.screen, (0,0,0), grid_rect, 5)
            pygame.draw.line(self.screen, (0,0,0), (10, 130), (370, 130), 3)
            pygame.draw.line(self.screen, (0,0,0), (10, 250), (370, 250), 3)
            pygame.draw.line(self.screen, (0,0,0), (130, 10), (130, 370), 3)
            pygame.draw.line(self.screen, (0,0,0), (250, 10), (250, 370), 3)

            for cell in self.cells:
                cell.draw_border(self.screen)

    # Checks if the grid is full
    def check_grid(self):
        for cell in self.cells:
            if cell.value==0:
                return False
        return True

    # solves the grid visually
    def solve_grid(self):
        for cell in self.cells:
            # removes user_input
            if cell.state["user_input"]:
                cell.value = 0
                cell.state["user_input"] = False
                cell.draw(self.screen)

            # parents blocks values stored in a list for checking move validity next
            row, col, square = cell.parents.values()

            if cell.value == 0:
                for val in range (1, 10):
                    if row.check_valid(val) and col.check_valid(val) and square.check_valid(val):
                        cell.clean(self.screen)
                        self.draw()
                        cell.value = val
                        cell.draw(self.screen)
                        # check if grid is full, exit if true
                        if(self.check_grid()):
                            print("grid full")
                            return True
                        # if not calls itself, and performs the same operations, once function calls come back to this function, try the next value
                        else:
                            if self.solve_grid():
                                return True
                # Once the function calls come back to this point, if none of the value offered a solution break out of loop
                break
        # can't solve from here, resetting cell and exit function, passing to a previous function call
        cell.value = 0
