import pygame
from data.Functions.load import load


class Note(pygame.sprite.Sprite):
    def __init__(self, image, weight, line):
        super().__init__()
        self.image = pygame.transform.scale(load("data\\Sprites\\" + image + ".png", colorkey=(255, 255, 255)),
                                            (80, 80))
        self.rect = self.image.get_rect()
