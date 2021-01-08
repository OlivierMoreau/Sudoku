import pygame


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
        state = [self.coordinates, self.size, self.value, self.final_val, self.state, self.rectangle]
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
