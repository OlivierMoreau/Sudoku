'''A sudoku game made using object oriented programin'''

import sys, pygame
pygame.init()

size =  (500, 500)

screen = pygame.display.set_mode(size)

pygame.display.set_caption("Sudoku")

run = True

while run:
    screen.fill((255,255,255))
    pygame.display.update()
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

class Game(object):
    'Main engine for the game'

    def __init__(self):
        pass

    def start(self):
        pass

    def board_fill(self):
        cells = []
        for x in range(81):
            cells.append(Cell(x))

        rows = []
        collumns = []
        squares = []
        for x in range(9):
            row = Row()
            collumn = Collumn()
            square = Square()
            for y in range(9):
                row.cells.append(cells[y + ((x) * 9)])
                collumn.cells.append(cells[x + ((y) * 9)])

            rows.append(row)
            collumns.append(collumn)

        #    for x in range(3):
        #        square.cells.append(cells)


        self.board = Board(rows, collumns, [])

class Board(object):
    'Game board'

    def __init__(self, rows, collumns, squares):
        self.rows = rows
        self.collumns = collumns
        self.squares = squares

    def display(self):

        for row in self.rows:
            print("|", end="")
            for cell in row.cells:
                print(f"{cell.value}|", end="")
            print("")



class Block(object):
    'Abstract class for block objects Rows, Collumns & Squares.'

    def __init__(self):
        self.cells = []

class Row(Block):
    pass

class Collumn(Block):
    pass

class Square(Block):
    pass


class Cell(object):
    'Individual cells of the board'

    def __init__(self, id):
        self.id = id
        self.value = " "
