import pygame
import os


class Button(pygame.sprite.Sprite):
    def __init__(self, window, path):
        super().__init__(window.sprites)
        self.set_image(path)
        self.rect = self.image.get_rect()
        self.func = None
        self.args = []

    def resize(self, width, height):
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()

    def move(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def set_image(self, path):
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()

    def set_func(self, func, *args):
        self.func = func
        self.args = args[:]

    def check_clicked(self, mouse_pos):
        if self.rect.x <= mouse_pos[0] <= self.rect.x + self.rect.width and \
                self.rect.y < mouse_pos[1] < self.rect.y + self.rect.height:
            return True
        else:
            return False

    def clicked(self):
        self.func(*self.args)
