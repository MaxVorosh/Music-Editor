import pygame
from data.Functions.load import load


class Note(pygame.sprite.Sprite):
    def __init__(self, image, x, y, size, down):
        super().__init__()
        if y > 155 or not down:
            self.image = pygame.transform.scale(pygame.image.load("data\\Sprites\\" + image + ".png"), size)
        else:
            self.image = pygame.transform.scale(pygame.image.load("data\\Sprites\\" + image + "_down.png"), size)
        self.rect = self.image.get_rect()
        self.rect.x = x
        if y > 155 or not down:
            self.rect.y = y - size[1] // 2
        else:
            self.rect.y = y + size[1] // 2 - 12
