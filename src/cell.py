import pygame


class Cell(object):
    """Individual cells of the grid"""

    def __init__(self):
        self.coordinates = (0, 0)
        self.size = (40, 40)
        self.rectangle = ""
        self.font = pygame.font.SysFont('arial', 20)

        self.emptycell = pygame.Surface((38, 38))
        self.emptycell.fill((255, 255, 255))

        self.parents = {'row': '', 'collumn': '', 'square': ''}

        # Current and correct values
        self.value = 0
        self.final_val = 0

        # Different states for drawing
        self.state = {
            "original": False,
            "user_input": False,
            "selected": False,
            "hint": False,
            "solved": False
        }
        self.colors = {
            "blue": (112, 224, 234),
            "yellow": (238, 189, 48),
            "green": (161, 205, 105),
            "red": (233, 47, 47),
            "pink": (255, 93, 153)
        }

    def save_state(self):
        state = [self.coordinates, self.size, self.value, self.final_val, self.state, self.rectangle]
        return state

    def draw_border(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.rectangle, 1)

    def draw(self, screen):
        color = []
        if self.state["original"]:
            color = [40, 40, 40]
        elif self.state["solved"]:
            color = self.colors["yellow"]
        elif self.state["hint"]:
            color = self.colors["pink"]
        else:
            color = self.colors["blue"]

        if self.state["selected"]:
            self.select(screen)
        # Draws a cell value
        if self.value != 0:
            text = self.font.render(str(self.value), True, color)
            rect = text.get_rect(center=self.rectangle.center)
            screen.blit(text, rect)

        pygame.display.update()

    def select(self, screen):
        bg = pygame.Surface((38, 38))
        bg.fill((223, 240, 216))
        screen.blit(bg, self.coordinates)

    # Removes selection border
    def unselect(self, screen):
        screen.blit(self.emptycell, self.coordinates)
        # pygame.draw.rect(screen, (70, 70, 70), self.rectangle, 1)

    # Removes content before drawing new value
    def clean(self, screen):
        screen.blit(self.emptycell, self.coordinates)

    # Changes color of text if the answer is correct or not
    def confirm(self, screen, valid):
        if valid:
            color = self.colors["green"]
        else:
            color = self.colors["red"]
        self.clean(screen)
        # pygame.draw.rect(screen, (0, 0, 0), self.rectangle, 1)

        text = self.font.render(str(self.value), True, color)
        rect = text.get_rect(center=self.rectangle.center)
        screen.blit(text, rect)
        pygame.display.update()
