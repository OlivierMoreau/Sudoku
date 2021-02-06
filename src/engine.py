import pickle

import pygame

from src.button import Button
from src.checkbox import Checkbox
from src.game import Game
from src.icon import Icon


class Engine(object):
    '''Main engine for the game'''

    def __init__(self, screen):

        self.screen = screen
        self.background_color = (220, 220, 220)

        self.game = Game(screen)
        self.font = pygame.font.SysFont('arial', 16)

        # flags
        self.run = False
        self.won = False
        self.victory_loading = False  # checks if victory state comes from loaded save

        self.counter = 0  # frames counter, resets every sec
        self.min = 0  # frames counter, resets every min

        # Ui
        self.buttons = {
            "new_game": Button('./imgs/newgame_button.png', (390, 10), self.screen),
            "solve": Button('./imgs/solve_button.png', (390, 70), self.screen),
            "check": Button('./imgs/check_button.png', (390, 140), self.screen),
            "hint": Button('./imgs/hint_button.png', (390, 210), self.screen)
        }
        self.icons = {
            "easy": Icon('./imgs/easy_icon.png', (568, 5), self.screen),
            "normal": Icon('./imgs/normal_icon.png', (568, 27), self.screen),
            "hard": Icon('./imgs/hard_icon.png', (568, 49), self.screen),

        }

        # sounds
        self.click_sound = pygame.mixer.Sound('./sounds/metalClick.ogg')
        self.valid_sound = pygame.mixer.Sound('./sounds/confirmation.ogg')
        self.victory_sound = pygame.mixer.Sound('./sounds/victory.ogg')

        # victory text
        self.victory_img = pygame.image.load('./imgs/you_won.png').convert_alpha()
        self.victory_rect = self.victory_img.get_rect(topleft=(390, 260))

        # Checkboxes
        self.boxes = []
        self.box_outline_color = (78, 137, 202)
        self.box_check_color = (161, 205, 105)
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
        self.add_checkbox(self.screen, 550, 10, color=(230, 230, 230), caption="easy",
                          outline_color=self.box_outline_color, check_color=self.box_check_color,
                          font_size=self.box_font_size, font_color=self.box_font_color,
                          text_offset=self.box_text_offset, font=self.box_font)

        self.add_checkbox(self.screen, 550, 30, color=(230, 230, 230), caption="normal",
                          outline_color=self.box_outline_color, check_color=self.box_check_color,
                          font_size=self.box_font_size, font_color=self.box_font_color,
                          text_offset=self.box_text_offset, font=self.box_font)

        self.add_checkbox(self.screen, 550, 50, color=(230, 230, 230), caption="hard",
                          outline_color=self.box_outline_color, check_color=self.box_check_color,
                          font_size=self.box_font_size, font_color=self.box_font_color,
                          text_offset=self.box_text_offset, font=self.box_font)

        # Draw buttons and icons
        self.game.grid.draw()
        self.button_draw()
        self.icon_draw()

        # Starts main loop
        self.run = True
        self.main_loop()

    def button_draw(self):
        for name, button in self.buttons.items():
            button.draw()

    def icon_draw(self):
        for name, icon in self.icons.items():
            icon.draw()

    # Update screen
    def draw(self):

        self.game.grid.draw_lines()
        for box in self.boxes:
            box.render_checkbox()
        pygame.display.update()

    def main_loop(self):
        while self.run:
            pygame.time.delay(16)
            self.counter += 1
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                # Quitting events
                if event.type == pygame.QUIT:
                    self.save_state()
                    self.run = False
                    pygame.quit()

                # Click events
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                    # check box
                    for box in self.boxes:
                        if box.checked:
                            box.checked = False
                        box.update_checkbox(event)
                        if box.checked:
                            self.checked_box = box

                    # Solve Button clicked
                    if self.buttons["solve"].is_touching(pos):
                        pygame.mixer.Sound.play(self.click_sound)
                        self.game.grid.solve_grid()
                        pygame.mixer.Sound.play(self.valid_sound)
                        self.game.solved = True

                    # New game Button clicked
                    if self.buttons["new_game"].is_touching(pos):
                        diff = "normal"
                        pygame.mixer.Sound.play(self.click_sound)
                        if self.checked_box:
                            diff = self.checked_box.caption

                        self.new_game(diff)

                    # Check Button clicked
                    if self.buttons["check"].is_touching(pos):
                        self.game.grid.unselect_cell()
                        self.game.check_user_input()

                    # hint Button clicked
                    if self.buttons["hint"].is_touching(pos) and self.game.grid.check_grid() == False:
                        pygame.mixer.Sound.play(self.click_sound)
                        self.game.give_hint(self.screen)

                    # Cell selection
                    for cell in self.game.grid.cells:
                        rect = cell.rectangle
                        if cell.state["selected"]:
                            cell.state["selected"] = False
                            cell.unselect(self.screen)
                            cell.draw(self.screen)
                        if rect.collidepoint(pos):
                            cell.state["selected"] = True
                            self.game.grid.selected_cell = cell
                            cell.select(self.screen)
                            cell.draw(self.screen)

                # Key press events
                # Checks if no cell as ever been selected, if previous selected cell still is and if
                # selected cell is one of the original inputs
                if event.type == pygame.KEYDOWN and self.game.grid.selected_cell is not None \
                        and self.game.grid.selected_cell.state["selected"] \
                        and self.game.grid.selected_cell.state["original"] != True \
                        and self.game.grid.selected_cell.state["hint"] != True:
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

            # Check for victory and local save once per sec
            if self.counter == 60:
                if self.game.grid.check_grid() and self.game.solved is False:  # Checks if the grid is full, and was not filled by the autosolver
                    if not self.victory_loading and self.game.final_check():  # Checks if we've just loaded the complete game & if the answers are all correct
                        if not self.won:  # only draws victory message once.
                            self.end_message(self.victory_img, self.victory_rect)
                            pygame.mixer.Sound.play(self.victory_sound)
                        self.won = True
                        open('data/tempsave.data', 'w').close()
                    # else:
                    # error message

                self.min += 1
                self.counter = 0

            # Auto saves once a min
            if self.min == 60:
                self.save_state()
                self.min = 0

            self.draw()

    # Create new game
    def new_game(self, difficulty="normal"):
        self.won = False
        self.victory_loading = False

        # New game init
        self.game = Game(self.screen, difficulty)
        game = self.game
        game.grid.draw()
        game.grid.set_vals()

        # Screen cleanup/redraw
        self.screen.fill(self.background_color)
        self.game.grid.draw()
        self.button_draw()
        self.icon_draw()
        self.draw()
        game.grid.set_vals()

    # Display end message
    def end_message(self, img, rect):
        self.screen.blit(img, rect)
        pygame.display.update()

    def save_state(self):
        with open('data/tempsave.data', 'wb') as f:
            save = []
            for cell in self.game.grid.cells:
                save.append(cell.save_state())
            save.append(self.game.grid.grid)
            save.append(self.game.grid.full_grid)
            save.append(self.game.solved)
            pickle.dump(save, f)

    def load_state(self):
        saved_state = ""
        with open("data/tempsave.data", "rb") as f:
            saved_state = pickle.load(f)

        self.game.grid.grid = saved_state[81]
        self.game.grid.full_grid = saved_state[82]
        self.game.solved = saved_state[83]

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

        # Stops victory sound and text from loaded save
        if self.game.grid.check_grid() and self.game.solved is False:
            if self.game.final_check():
                self.victory_loading = True
