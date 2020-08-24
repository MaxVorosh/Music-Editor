import pygame
from data.Constants import MULTIPLIER


class Line:
    def __init__(self, screen, start, stop, line, width=3):
        self.screen = screen
        self.start = start
        self.stop = stop
        self.draw_start = start
        self.draw_stop = stop
        self.width = width
        self.line = line

    def draw(self):
        pygame.draw.line(self.screen, pygame.Color('black'), self.draw_start, self.draw_stop, self.width)

    def do_up(self):
        self.line -= 1
        if self.line == 0:
            self.draw_start = (-10, -10)
            self.draw_stop = (-10, -10)
        if self.line == 3:
            self.draw_start = (self.start[0] + 3 * MULTIPLIER, self.start[1] + 3 * MULTIPLIER)
            self.draw_stop = (self.stop[0] + 3 * MULTIPLIER, self.stop[1] + 3 * MULTIPLIER)

    def do_down(self):
        self.line += 1
        if self.line == 1:
            self.draw_start = self.start
            self.draw_stop = self.stop
        if self.line == 4:
            self.draw_start = (650, 650)
            self.draw_stop = (650, 650)
