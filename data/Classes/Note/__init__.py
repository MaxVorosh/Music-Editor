import pygame
from data.Functions.load import load


class Note(pygame.sprite.Sprite):
    def __init__(self, image, x, y, size):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("data\\Sprites\\" + image + ".png"), size)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - size[1] // 2
