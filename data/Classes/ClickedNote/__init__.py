import pygame
from ..Button import Button


class ClickedNote(Button):
    def __init__(self, window, image, x, y, weight):
        super().__init__(window, "data\\Sprites\\" + image + ".png")
        window.note_group.add(self)
        window.sprites.remove(self)
        self.resize(30, 90)
        self.move(x, y)
        self.weight = weight
        self.set_func(window.draw_note, self.weight)
