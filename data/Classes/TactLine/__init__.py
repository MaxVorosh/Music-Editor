import pygame


class TactLine(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("data\\Sprites\\tact_line.png"), (2, 56))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
