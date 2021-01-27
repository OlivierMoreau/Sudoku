import pygame


class Button:

    def __init__(self, img, coordinate, screen):
        self.image = pygame.image.load(img).convert_alpha()
        self.coordinate = coordinate
        self.rect = self.image.get_rect(topleft=self.coordinate)
        self.mask = pygame.mask.from_surface(self.image)
        self.screen = screen

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def is_touching(self, pos):
        pos_in_mask = pos[0] - self.rect.x, pos[1] - self.rect.y
        touching = self.rect.collidepoint(pos) and self.mask.get_at(pos_in_mask)
        return touching
