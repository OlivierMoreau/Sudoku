import math
import pickle
import random

import pygame

from src.checkbox import Checkbox
from src.game import Game
from src.reader import Reader


class Engine(object):
    '''Main engine for the game'''

    def __init__(self, screen):

        self.screen = screen

        self.game = Game(screen)
        self.font = pygame.font.SysFont('arial', 16)
        self.run = False

        self.counter = 0  # frames counter, resets every sec
        self.min = 0  # frames counter, resets every min
        # Buttons
        self.buttons = {
            "new_game": ["New Game", pygame.Rect((485, 10), (100, 50))],
            "solve": ["Solve", pygame.Rect((485, 110), (100, 50))],
            "check": ["Check", pygame.Rect((485, 210), (100, 50))],
            "hint": ["Hint", pygame.Rect((485, 310), (100, 50))]
        }
        self.click_sound = pygame.mixer.Sound('./sounds/click.wav')
        # Bottom text
        self.bottom_rect = pygame.Rect((10, 375), (360, 125))
        # Checkboxes
        self.boxes = []
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
                     check_color=(0, 0, 0), font_size=22, font_color=(0, 0, 0), text_offset=(28, 1),
                     font='Ariel Black'):
        self.idnum += 1

        box = Checkbox(self.screen, x, y, self.idnum, color, caption,
                       outline_color, check_color, font_size, font_color, text_offset, font)

        self.boxes.append(box)

    # Initialisation operations
    def start(self):

        # Creates and draw checkboxes
        self.add_checkbox(self.screen, 600, 10, color=(230, 230, 230), caption="easy",
                          outline_color=self.box_outline_color, check_color=self.box_check_color,
                          font_size=self.box_font_size, font_color=self.box_font_color,
                          text_offset=self.box_text_offset, font=self.box_font)

        self.add_checkbox(self.screen, 600, 30, color=(230, 230, 230), caption="normal",
                          outline_color=self.box_outline_color, check_color=self.box_check_color,
                          font_size=self.box_font_size, font_color=self.box_font_color,
                          text_offset=self.box_text_offset, font=self.box_font)

        self.add_checkbox(self.screen, 600, 50, color=(230, 230, 230), caption="hard",
                          outline_color=self.box_outline_color, check_color=self.box_check_color,
                          font_size=self.box_font_size, font_color=self.box_font_color,
                          text_offset=self.box_text_offset, font=self.box_font)

        for box in self.boxes:
            box._draw_button_text()

        # Draw buttons
        for val in self.buttons.values():
            self.button_draw(val[0], val[1])

        # Starts main loop
        self.run = True
        self.main_loop()

    def button_draw(self, text, rect):
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 3)
        content = self.font.render(text, True, [40, 40, 40])
        rect = content.get_rect(center=rect.center)
        self.screen.blit(content, rect)

    # Update screen
    def draw(self):
        self.game.grid.draw()
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
                        pygame.mixer.Sound.play(self.click_sound)
                        self.game.grid.solve_grid()
                        self.game.solved = True

                    # New game Button clicked
                    if self.buttons["new_game"][1].collidepoint(pos):
                        diff = "normal"
                        pygame.mixer.Sound.play(self.click_sound)
                        if self.checked_box:
                            diff = self.checked_box.caption

                        self.new_game(diff)

                    # Check Button clicked
                    if self.buttons["check"][1].collidepoint(pos):
                        print('checking')
                        pygame.mixer.Sound.play(self.click_sound)
                        self.game.check_user_input()

                    # hint Button clicked
                    if self.buttons["hint"][1].collidepoint(pos) and self.game.grid.check_grid() == False:
                        print('hinting')
                        pygame.mixer.Sound.play(self.click_sound)
                        self.game.give_hint(self.screen)

                    # Cell selection
                    for cell in self.game.grid.cells:
                        rect = cell.rectangle
                        if cell.state["selected"]:
                            cell.state["selected"] = False
                            cell.unselect(self.screen)
                        if rect.collidepoint(pos):
                            print(
                                f'selected cell coordinates = {cell.coordinates} cell orignial = {cell.state["original"]}')
                            print(f'selected cell current val = {cell.value} cell final_val = {cell.final_val}')
                            cell.state["selected"] = True
                            self.game.grid.selected_cell = cell
                            cell.draw(self.screen)

                # Key press events
                # Checks if no cell as ever been selected, if previous selected cell still is and if selected cell is one of the original inputs
                if event.type == pygame.KEYDOWN and self.game.grid.selected_cell != None and \
                        self.game.grid.selected_cell.state["selected"] and self.game.grid.selected_cell.state[
                    "original"] != True and self.game.grid.selected_cell.state["hint"] != True:
                    cell = self.game.grid.selected_cell
                    cell.state["user_input"] = True
                    if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        cell.clean(self.screen)
                        cell.value = 1
                        cell.draw(self.screen)
                    if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        cell.clean(self.screen)
                        cell.value = 2
                        cell.draw(self.screen)
                    if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                        cell.clean(self.screen)
                        cell.value = 3
                        cell.draw(self.screen)
                    if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                        cell.clean(self.screen)
                        cell.value = 4
                        cell.draw(self.screen)
                    if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                        cell.clean(self.screen)
                        cell.value = 5
                        cell.draw(self.screen)
                    if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                        cell.clean(self.screen)
                        cell.value = 6
                        cell.draw(self.screen)
                    if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                        cell.clean(self.screen)
                        cell.value = 7
                        cell.draw(self.screen)
                    if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                        cell.clean(self.screen)
                        cell.value = 8
                        cell.draw(self.screen)
                    if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                        cell.clean(self.screen)
                        cell.value = 9
                        cell.draw(self.screen)
                    if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
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
                if self.game.grid.check_grid() and self.game.solved == False:
                    if self.game.final_check():
                        self.end_message("you won !", (40, 122, 40), 40)
                        open('data/tempsave.data', 'w').close()
                    else:
                        self.end_message("There's an error somewhere !", (255, 153, 153), 28)
                self.min += 1
                self.counter = 0

            # Auto saves once a min
            if self.min == 60:
                self.save_state()
                self.min = 0

    # Create new game
    def new_game(self, difficulty="normal"):
        grid_pick = ""
        print(f"new game : {difficulty}")

        reader = Reader()
        grids_sample = reader.size()
        thirds = math.floor(grids_sample / 3)

        # Grid selection sorted by the time they took to create
        if difficulty == "easy":
            grid_pick = random.randrange(thirds)
        elif difficulty == "normal":
            grid_pick = random.randrange(thirds, thirds * 2)
        elif difficulty == "hard":
            grid_pick = random.randrange(thirds * 2, thirds * 3 - 1)

        # Each grid has 4 possible 90° rotations
        rot_pick = random.randrange(4)

        grid, full_grid = reader.grid_picker(grid_pick, rot_pick)

        # New game init
        self.game = Game(self.screen, difficulty)
        game = self.game
        game.grid.draw()
        game.grid.set_vals()

        # Screen cleanup/redraw
        bottom = pygame.Rect((0, 375), (500, 125))
        pygame.draw.rect(self.screen, (255, 255, 255), bottom, 0)
        self.draw()
        game.grid.set_vals()

    # Display bottom message, t = text, c = color, s = fontsize
    def end_message(self, t, c, s):
        font = pygame.font.SysFont('arial', s)
        pygame.draw.rect(self.screen, (255, 255, 255), self.bottom_rect, 0)
        text = font.render(t, True, c)
        rect = text.get_rect(center=self.bottom_rect.center)
        self.screen.blit(text, rect)
        pygame.display.update()

    def save_state(self):
        print("saving")
        with open('data/tempsave.data', 'wb') as f:
            save = []
            for cell in self.game.grid.cells:
                save.append(cell.save_state())
            save.append(self.game.grid.grid)
            save.append(self.game.grid.full_grid)
            pickle.dump(save, f)

    def load_state(self):
        print("loading save")

        saved_state = ""
        with open("data/tempsave.data", "rb") as f:
            saved_state = pickle.load(f)

        print(saved_state[81])
        self.game.grid.grid = saved_state[81]
        self.game.grid.full_grid = saved_state[82]

        for x in range(81):
            cell = self.game.grid.cells[x]
            cell.coordinates = saved_state[x][0]
            cell.size = saved_state[x][1]
            cell.value = saved_state[x][2]
            cell.final_val = saved_state[x][3]
            cell.state = saved_state[x][4]
            cell.rectangle = saved_state[x][5]
            cell.clean(self.screen)
            cell.draw(self.screen)
