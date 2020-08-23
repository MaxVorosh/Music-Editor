import pygame
from data.Functions.load import load
from data.Constants import MULTIPLIER


class Note(pygame.sprite.Sprite):
    def __init__(self, image, x, y, size, down, line):
        super().__init__()
        if y > 155 or not down:
            self.image = pygame.transform.scale(pygame.image.load("data\\Sprites\\" + image + ".png"), size)
            self.up = True
        else:
            self.image = pygame.transform.scale(pygame.image.load("data\\Sprites\\" + image + "_down.png"), size)
            self.up = False
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.image_name = image
        self.start_name = image
        self.down = down
        self.line = line
        self.y = y
        self.size = size
        self.start_up = self.up
        if y > 155 or not down:
            self.rect.y = y - size[1] // 2
        else:
            self.rect.y = y + size[1] // 2 - 12

    def change_image(self, image, size):
        x, y = self.rect.x, self.rect.y
        self.image_name = image
        if self.up:
            self.image = pygame.transform.scale(pygame.image.load("data\\Sprites\\" + image + ".png"), size)
        else:
            self.image = pygame.transform.scale(pygame.image.load("data\\Sprites\\" + image + "_down.png"), size)
        self.rect = self.image.get_rect()
        self.rect.x = x
        if self.up:
            self.rect.y = y - size[1] + self.size[1]
        else:
            self.rect.y = y
        self.size = size

    def change_up(self):
        if self.down:
            self.up = not self.up
            x, y = self.rect.x, self.rect.y
            if self.up:
                self.image = pygame.transform.scale(pygame.image.load("data\\Sprites\\" + self.image_name + ".png"),
                                                    self.size)
            else:
                self.image = pygame.transform.scale(
                    pygame.image.load("data\\Sprites\\" + self.image_name + "_down.png"), self.size)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y - self.size[1]
            if self.up:
                self.rect.y = y - self.size[1] + 14
            else:
                self.rect.y = y + self.size[1] - 14

    def do_up(self):
        self.line -= 1
        if self.line == 0:
            self.rect.y = -100
        elif self.line == 3:
            self.rect.y = self.y + 3 * MULTIPLIER

    def do_down(self):
        self.line += 1
        if self.line == 4:
            self.rect.y = 650
        elif self.line == 1:
            self.rect.y = self.y
