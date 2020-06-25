import pygame
from ..Button import Button


class ClickedNote(Button):
    def __init__(self, window, image, x, y, weight, size):
        super().__init__(window, "data\\Sprites\\" + image + ".png")
        window.clicked_note_group.add(self)
        window.sprites.remove(self)
        self.resize(*size)
        self.move(x, y)
        self.weight = weight
        self.set_func(window.draw_note, self.weight)
