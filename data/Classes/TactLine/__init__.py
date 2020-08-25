import pygame
from data.Constants import MULTIPLIER


class TactLine(pygame.sprite.Sprite):
    def __init__(self, x, y, line, plane):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("data\\Sprites\\tact_line.png"), (2, 56))
        self.rect = self.image.get_rect()
        self.rect.x = x - (line - 1) * 545
        self.y = y
        self.line = line - plane + 1
        self.rect.y = y + (self.line - 1) * MULTIPLIER

    def do_up(self):
        self.line -= 1
        if self.line == 0:
            self.rect.y = -100
        elif 1 <= self.line <= 3:
            self.rect.y = self.y + (self.line - 1) * MULTIPLIER

    def do_down(self):
        self.line += 1
        if self.line == 4:
            self.rect.y = 650
        elif 1 <= self.line <= 3:
            self.rect.y = self.y + (self.line - 1) * MULTIPLIER
