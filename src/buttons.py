import pygame


class Button(pygame.sprite.Sprite):


    def __init__(self, img, coordinate, screen):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(img).convert_alpha()
        self.coordinate = coordinate
        self.image = pygame.transform.scale(self.image, (150, 50))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.screen = screen

    def draw(self):
        self.screen.blit(self.image, self.coordinate)

