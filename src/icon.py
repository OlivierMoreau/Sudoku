import pygame


class Icon:

    def __init__(self, img, coordinate, screen):
        self.image = pygame.image.load(img).convert_alpha()
        self.coordinate = coordinate
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect(topleft=self.coordinate)
        self.mask = pygame.mask.from_surface(self.image)
        self.screen = screen

    def draw(self):
        self.screen.blit(self.image, self.rect)

