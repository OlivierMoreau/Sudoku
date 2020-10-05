'''A sudoku game made using object oriented programing'''

import pygame, random, pickle, os, checkbox
from reader import grid_picker
from blocks import *


class Engine(object):
    '''Main engine for the game'''

    def __init__(self, screen):

        self.screen = screen
        self.game = ""
        self.font = pygame.font.SysFont('arial', 16)
        self.run = False
        self.counter = 0 # frames counter, resets every sec
        self.min = 0 # frames counter, resets every min
        # Buttons
        self.buttons = {
            "new_game": ["New Game", pygame.Rect((485,10),(100, 50))],
            "solve": ["Solve", pygame.Rect((485,110),(100, 50))],
            "check": ["Check", pygame.Rect((485,210),(100, 50))],
            "hint": ["Hint", pygame.Rect((485,310),(100, 50))]
        }
        # Bottom text
        self.bottom_rect = pygame.Rect((10, 375),(360, 125))
        # Checkboxes
        self.boxes=[]
        self.box_outline_color = (78, 137, 202)
        self.box_check_color = (22, 200, 105)
        self.box_font_size = 16
        self.box_font_color = (0, 0, 0)
        self.box_text_offset = (28, 1)
        self.box_font = "arial"
        self.checked_box = ""
        self.idnum = 1

    # Adds a checkbox
    def add_checkbox(self, surface, x, y, color=(230, 230, 230), caption="", outline_color=(0, 0, 0),
                 check_color=(0, 0, 0), font_size=22, font_color=(0, 0, 0), text_offset=(28, 1), font='Ariel Black'):
        self.idnum+=1

        box = checkbox.Checkbox(self.screen, x, y, self.idnum, color, caption,
            outline_color, check_color, font_size, font_color, text_offset, font)

        self.boxes.append(box)


    # Initialisation operations
    def start(self):

        # Creates and draw checkboxes
        self.add_checkbox(self.screen, 600, 10, color=(230,230,230),caption="easy",
                            outline_color=self.box_outline_color, check_color=self.box_check_color, font_size=self.box_font_size, font_color=self.box_font_color,
                            text_offset=self.box_text_offset, font=self.box_font)

        self.add_checkbox(self.screen, 600, 30, color=(230,230,230),caption="normal",
                            outline_color=self.box_outline_color, check_color=self.box_check_color, font_size=self.box_font_size, font_color=self.box_font_color,
                            text_offset=self.box_text_offset, font=self.box_font)

        self.add_checkbox(self.screen, 600, 50, color=(230,230,230),caption="hard",
                            outline_color=self.box_outline_color, check_color=self.box_check_color, font_size=self.box_font_size, font_color=self.box_font_color,
                            text_offset=self.box_text_offset, font=self.box_font)

        for box in self.boxes:
            box._draw_button_text()

        # Draw buttons
        for val in self.buttons.values():
            self.button_draw(val[0], val[1])

        #Starts main loop
        self.run = True
        self.main_loop()


    def button_draw(self, text, rect):
        pygame.draw.rect(self.screen, (0,0,0), rect , 3)
        content = self.font.render(text, True, [40,40,40])
        rect = content.get_rect(center = rect.center)
        self.screen.blit(content, rect)


    # Update screen
    def draw(self):
        self.game.grid.draw(self.screen)
        for box in self.boxes:
            box.render_checkbox()
        pygame.display.update()


    def main_loop(self):
        while self.run:
            pygame.time.delay(16)
            self.counter += 1
            for event in pygame.event.get():
                # Quitting events
                if event.type == pygame.QUIT:
                    self.save_state()
                    self.run = False
                    pygame.quit()
                # Click events
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    print('clicking')

                    # check box
                    for box in self.boxes:
                        if box.checked:
                            box.checked = False
                        box.update_checkbox(event)
                        if box.checked:
                            self.checked_box = box

                    pos = pygame.mouse.get_pos()

                    # Solve Button clicked
                    if self.buttons["solve"][1].collidepoint(pos):
                        print('solving')
                        self.game.grid.solve_grid(self.screen)
                        self.game.solved = True

                    # New game Button clicked
                    if self.buttons["new_game"][1].collidepoint(pos):
                        diff = "normal"
                        if self.checked_box:
                            diff = self.checked_box.caption

                        self.new_game(diff)

                    # Check Button clicked
                    if self.buttons["check"][1].collidepoint(pos):
                        print('checking')

                        self.game.check_user_input()

                    # hint Button clicked
                    if self.buttons["hint"][1].collidepoint(pos) and self.game.grid.check_grid() == False:
                        print('hinting')
                        self.game.give_hint(self.screen)

                    # Cell selection
                    for cell in self.game.grid.cells:
                        rect = cell.rectangle
                        if cell.state["selected"]:
                            cell.state["selected"] = False
                            cell.unselect(self.screen)
                        if rect.collidepoint(pos):
                            print(f'selected cell coordinates = {cell.coordinates} cell orignial = {cell.state["original"]}')
                            print(f'selected cell current val = {cell.value} cell final_val = {cell.final_val}')
                            cell.state["selected"] = True
                            self.game.grid.selected_cell = cell
                            cell.draw(self.screen)

                # Key press events
                # Checks if no cell as ever been selected, if previous selected cell still is and if selected cell is one of the original inputs
                if event.type == pygame.KEYDOWN and self.game.grid.selected_cell != None and self.game.grid.selected_cell.state["selected"] and self.game.grid.selected_cell.state["original"] != True and self.game.grid.selected_cell.state["hint"] != True:
                    cell = self.game.grid.selected_cell
                    cell.state["user_input"] = True
                    if event.key == pygame.K_1 or event.key == pygame.K_KP1 :
                        cell.clean(self.screen)
                        cell.value = 1
                        cell.draw(self.screen)
                    if event.key == pygame.K_2 or event.key == pygame.K_KP2 :
                        cell.clean(self.screen)
                        cell.value = 2
                        cell.draw(self.screen)
                    if event.key == pygame.K_3 or event.key == pygame.K_KP3 :
                        cell.clean(self.screen)
                        cell.value = 3
                        cell.draw(self.screen)
                    if event.key == pygame.K_4 or event.key == pygame.K_KP4 :
                        cell.clean(self.screen)
                        cell.value = 4
                        cell.draw(self.screen)
                    if event.key == pygame.K_5 or event.key == pygame.K_KP5 :
                        cell.clean(self.screen)
                        cell.value = 5
                        cell.draw(self.screen)
                    if event.key == pygame.K_6 or event.key == pygame.K_KP6 :
                        cell.clean(self.screen)
                        cell.value = 6
                        cell.draw(self.screen)
                    if event.key == pygame.K_7 or event.key == pygame.K_KP7 :
                        cell.clean(self.screen)
                        cell.value = 7
                        cell.draw(self.screen)
                    if event.key == pygame.K_8 or event.key == pygame.K_KP8 :
                        cell.clean(self.screen)
                        cell.value = 8
                        cell.draw(self.screen)
                    if event.key == pygame.K_9 or event.key == pygame.K_KP9 :
                        cell.clean(self.screen)
                        cell.value = 9
                        cell.draw(self.screen)
                    if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE :
                        cell.clean(self.screen)
                        cell.state["user_input"] = False
                        cell.value = 0
                        cell.unselect(self.screen)
                        self.game.grid.selected_cell = None
            if self.checked_box:
                self.checked_box.checked = True
            self.draw()

            # Check for victory and local save once per sec
            if self.counter == 60:
                if self.game.grid.check_grid() and self.game.solved == False :
                    if self.game.final_check():
                        self.end_message("you won !", (40,122,40), 40)
                        open('tempsave.data', 'w').close()
                    else:
                        self.end_message("There's an error somewhere !", (255,153,153), 28)
                self.min += 1
                self.counter = 0

            # Auto saves once a min
            if self.min == 60:
                print(self.min)
                self.save_state()
                self.min = 0

    # Create new game
    def new_game(self, difficulty="normal"):
        print(f"new game : {difficulty}")
        grid_pick = ""

        # Grid selection from a file of 3k, sorted by the time they took to create
        if difficulty == "easy":
            grid_pick = random.randrange(1000)
        elif difficulty == "normal":
            grid_pick = random.randrange(1000, 2000)
        elif difficulty == "hard":
            grid_pick = random.randrange(2000, 2999)

        # Each grid has 4 possible 90° rotations
        rot_pick = random.randrange(4)

        grid, full_grid = grid_picker(grid_pick, rot_pick)

        # New game init
        self.game = Game(self.screen, difficulty)
        game = self.game
        game.grid = Grid(grid)
        game.grid.full_grid = full_grid
        game.grid.make_grid_struct()

        # Screen cleanup/redraw
        bottom = pygame.Rect((0, 375),(500, 125))
        pygame.draw.rect(self.screen, (255,255,255), bottom, 0)
        self.draw()
        game.grid.set_vals(self.screen)

    # Display bottom message, t = text, c = color, s = fontsize
    def end_message(self, t, c, s):
        font = pygame.font.SysFont('arial', s)
        pygame.draw.rect(self.screen, (255,255,255), self.bottom_rect, 0)
        text = font.render(t, True, c)
        rect = text.get_rect(center = self.bottom_rect.center)
        self.screen.blit(text, rect)
        pygame.display.update()

    def save_state(self):
        print("saving")
        with open('tempsave.data', 'wb') as f:
            save = []
            for cell in self.game.grid.cells:
                save.append(cell.save_state())
            save.append(self.game.grid.grid)
            save.append(self.game.grid.full_grid)
            pickle.dump(save, f)

    def load_state(self):
        print("loading save")

        saved_state = ""
        with open("tempsave.data", "rb") as f:
            saved_state = pickle.load(f)

        self.game.grid = Grid(saved_state[81])
        self.game.grid.full_grid = saved_state[82]
        for x in range(81):
            cell = Cell()
            cell.coordinates = saved_state[x][0]
            cell.size = saved_state[x][1]
            cell.value = saved_state[x][2]
            cell.final_val = saved_state[x][3]
            cell.state = saved_state[x][4]
            self.game.grid.cells.append(cell)

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


class Grid(object):
    '''Game grid'''

    def __init__(self, grid):
        self.grid = grid
        self.rows = []
        self.collumns = []
        self.squares = []
        self.cells = []
        self.selected_cell = None
        self.full_grid = []
        self.rect = pygame.Rect((10,10), (370, 370))

    def make_grid_struct(self, new = True):
        if new:
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
    def set_vals(self, screen):
        list_grid = forfor(self.grid)
        final_list = forfor(self.full_grid)
        for x in range(81):
            cell = self.cells[x]
            cell.clean(screen)
            cell.value = list_grid[x]
            cell.final_val = final_list[x]
            if list_grid[x] != 0:
                cell.state["original"] = True
            cell.draw(screen)
        # Add a clue if a block is empty
        for square in self.squares:
            if sum(square.get_values()) == 0:
                print("adding in square")
                cell = square.cells[random.randrange(1,9)]
                cell.value = cell.final_val
                cell.state["original"] = True
                cell.draw(screen)
        for row in self.rows:
            if sum(row.get_values()) == 0:
                print("adding in row")
                cell = row.cells[random.randrange(1,9)]
                cell.value = cell.final_val
                cell.state["original"] = True
                cell.draw(screen)
        for col in self.collumns:
            if sum(col.get_values()) == 0:
                print("adding in col")
                cell = col.cells[random.randrange(1,9)]
                cell.value = cell.final_val
                cell.state["original"] = True
                cell.draw(screen)


    # Draw grid and cells borders
    def draw(self, screen):
            grid_rect = pygame.Rect((10,10),(360, 360))
            pygame.draw.rect(screen, (0,0,0), grid_rect, 5)
            pygame.draw.line(screen, (0,0,0), (10, 130), (370, 130), 3)
            pygame.draw.line(screen, (0,0,0), (10, 250), (370, 250), 3)
            pygame.draw.line(screen, (0,0,0), (130, 10), (130, 370), 3)
            pygame.draw.line(screen, (0,0,0), (250, 10), (250, 370), 3)

            for cell in self.cells:
                cell.draw_border(screen)

    # Checks if the grid is full
    def check_grid(self):
        for cell in self.cells:
            if cell.value==0:
                return False
        return True

    # solves the grid visually
    def solve_grid(self, screen):
        for cell in self.cells:
            # removes unser_input
            if cell.state["user_input"] == True:
                cell.value = 0
                cell.state["user_input"] = False
                cell.draw(screen)

            # parents blocks values stored in a list for checking move validity next
            row, col, square = cell.parents.values()

            if cell.value == 0:
                for val in range (1, 10):
                    if row.check_valid(val) and col.check_valid(val) and square.check_valid(val):
                        cell.clean(screen)
                        self.draw(screen)
                        cell.value = val
                        cell.draw(screen)
                        # check if grid is full, exit if true
                        if(self.check_grid()):
                            print("grid full")
                            return True
                        # if not calls itself, and performs the same operations, once function calls come back to this function, try the next value
                        else:
                            if self.solve_grid(screen):
                                return True
                # Once the function calls come back to this point, if none of the value offered a solution break out of loop
                break
        # can't solve from here, resetting cell and exit function, passing to a previous function call
        cell.value = 0

class Cell(object):
    '''Individual cells of the grid'''

    def __init__(self):
        self.coordinates = (0,0)
        self.size = (40,40)
        self.rectangle = ""

        self.emptycell = pygame.Surface((38,38))
        self.emptycell.fill((255,255,255))

        self.parents = {'row': '', 'collumn': '', 'square': ''}
        self.font = pygame.font.SysFont('arial',20)

        # Current and correct values
        self.value = 0
        self.final_val = 0

        # Different states for drawing
        self.state = {
            "original": False,
            "user_input": False,
            "selected": False,
            "hint": False
        }


    def save_state(self):
        state = [self.coordinates, self.size, self.value, self.final_val, self.state]
        return state


    def draw_border(self, screen):
        pygame.draw.rect(screen, (0,0,0), self.rectangle, 1)

    def draw(self, screen):
        color = []
        if self.state["original"]:
            color = [40,40,40]
        elif self.state["hint"]:
            color = [255,153,51]
        else :
            color = [0,0,200]

        # Draws green border on selected cells
        if self.state["selected"]:
            pygame.draw.rect(screen, (0,200,0), self.rectangle, 4)
        # Draws a cell value
        if self.value != 0:
            text = self.font.render(str(self.value), True, color)
            rect = text.get_rect(center = self.rectangle.center)
            screen.blit(text, rect)

        pygame.display.update()

    # Removes selection border
    def unselect(self, screen):
        pygame.draw.rect(screen, (255,255,255), self.rectangle, 4)

    # Removes content before drawing new value
    def clean(self, screen):
        screen.blit(self.emptycell, self.coordinates)

    # Changes color of text if the answer is correct or not
    def confirm(self, screen, valid):
        if valid:
            color = [40,122,40]
        else:
            color = [255,153,153]
        self.clean(screen)
        pygame.draw.rect(screen, (0,0,0), self.rectangle, 1)
        text = self.font.render(str(self.value), True, color)
        rect = text.get_rect(center = self.rectangle.center)
        screen.blit(text, rect)
        pygame.display.update()

def main():

    pygame.init()
    pygame.display.set_caption("Sudoku")
    size = (800, 500)
    screen = pygame.display.set_mode(size)
    screen.fill((255,255,255))
    icon = pygame.image.load('icone.png')
    pygame.display.set_icon(icon)

    # Checks if there's a saved file
    if os.stat("tempsave.data").st_size != 0:

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


# Transforms list of lists into one list with 2 for loops
def forfor(a):
    return [item for sublist in a for item in sublist]

if __name__ == '__main__':
    main()
