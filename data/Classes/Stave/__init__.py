import pygame
from data.Functions.load import load


class Stave(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(load('data\\Sprites\\stave.jpg'), (640, 60))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
