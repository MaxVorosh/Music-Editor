import pygame
from ..Button import Button
from data.Functions.load import load


class Key(Button):
    def __init__(self, window, is_violin, x, y):
        self.is_violin = is_violin
        self.window = window
        if is_violin:
            super().__init__(window, "data\\Sprites\\violin_black.png")
        else:
            super().__init__(window, "data\\Sprites\\bass_black.png")
        self.y = y
        self.x = x
        if not is_violin:
            self.x += 10
            self.resize(60, 60)
        else:
            self.y -= 15
            self.resize(90, 90)
        self.move(self.x, self.y)

    def update(self, stage):
        if stage < 5:
            for key in self.window.keys:
                key.is_violin = not key.is_violin
                if key.is_violin:
                    key.set_image("data\\Sprites\\violin_black.png")
                else:
                    key.set_image("data\\Sprites\\bass_black.png")
                if not key.is_violin:
                    key.x += 10
                    key.y += 15
                    key.resize(60, 60)
                else:
                    key.x -= 10
                    key.y -= 15
                    key.resize(90, 90)
                key.move(key.x, key.y)
