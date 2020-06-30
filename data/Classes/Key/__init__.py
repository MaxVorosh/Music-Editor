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
                    self.window.up_note_1 = {'B': 135, 'C': 177, 'D': 170, 'E': 163, 'F': 156, 'G': 149, 'A': 142}
                    self.window.up_note_2 = {'B': 170, 'C': 212, 'D': 205, 'E': 198, 'F': 191, 'G': 184, 'A': 177}
                    self.window.up_note_3 = {'B': 121, 'C': 163, 'D': 156, 'E': 149, 'F': 142, 'G': 135, 'A': 128}
                    self.window.up_note_4 = {'B': 72, 'C': 114, 'D': 107, 'E': 100, 'F': 93, 'G': 86, 'A': 79}
                    self.window.up_note = {1: self.window.up_note_1, 2: self.window.up_note_2, 3: self.window.up_note_3,
                                           4: self.window.up_note_4}
                else:
                    self.window.up_note_1 = {'B': 184, 'E': 212, 'F': 205, 'G': 198, 'A': 191}
                    self.window.up_note_2 = {'B': 135, 'C': 177, 'D': 170, 'E': 163, 'F': 156, 'G': 149, 'A': 142}
                    self.window.up_note = {1: self.window.up_note_1, 2: self.window.up_note_2}
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
