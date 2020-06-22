import pygame
from data.Functions.load import load


class Note(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("data\\Sprites\\" + image + ".png"), (10, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
