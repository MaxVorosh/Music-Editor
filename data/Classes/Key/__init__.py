import pygame
from ..Button import Button
from data.Functions.load import load


class Key(Button):
    def __init__(self, window, is_violin, x, y):
        self.is_violin = is_violin
        if is_violin:
            super().__init__(window, "data\\Sprites\\violin_black.png")
        else:
            super().__init__(window, "data\\Sprites\\bass_black.png")
        self.y = y
        self.x = x
        if not is_violin:
            self.x += 10
        self.resize(60, 60)
        self.move(self.x, self.y)
        self.func = self.update

    def update(self):
        self.is_violin = not self.is_violin
        if self.is_violin:
            self.set_image("data\\Sprites\\violin_black.png")
        else:
            self.set_image("data\\Sprites\\bass_black.png")
        self.resize(60, 60)
        if not self.is_violin:
            self.x += 10
        else:
            self.x -= 10
        self.move(self.x, self.y)
