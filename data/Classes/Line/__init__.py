import pygame
from data.Constants import MULTIPLIER


class Line:
    def __init__(self, screen, start, stop, line, width=3):
        self.screen = screen
        self.start = start
        self.stop = stop
        self.width = width
        self.line = line

    def draw(self):
        if 1 <= self.line <= 3:
            pygame.draw.line(self.screen, pygame.Color('black'), self.start, self.stop, self.width)

    def do_up(self):
        self.line -= 1

    def do_down(self):
        self.line += 1
