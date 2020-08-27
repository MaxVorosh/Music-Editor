import pygame
from data.Constants import MULTIPLIER


class Line:
    def __init__(self, screen, start, stop, line, width=3):
        self.screen = screen
        self.start = (start[0], start[1] - (line - 1) * MULTIPLIER)
        self.stop = (stop[0], stop[1] - (line - 1) * MULTIPLIER)
        self.width = width
        self.line = line
        self.draw_start = (self.start[0], self.start[1] + (self.line - 1) * MULTIPLIER)
        self.draw_stop = (self.stop[0], self.stop[1] + (self.line - 1) * MULTIPLIER)
        if self.line > 2:
            self.draw_start = (650, 650)
            self.draw_stop = (650, 650)

    def draw(self):
        pygame.draw.line(self.screen, pygame.Color('black'), self.draw_start, self.draw_stop, self.width)

    def do_up(self):
        self.line -= 1
        if self.line == 0:
            self.draw_start = (-10, -10)
            self.draw_stop = (-10, -10)
        if 1 <= self.line <= 2:
            self.draw_start = (self.start[0], self.start[1] + (self.line - 1) * MULTIPLIER)
            self.draw_stop = (self.stop[0], self.stop[1] + (self.line - 1) * MULTIPLIER)

    def do_down(self):
        self.line += 1
        if self.line == 3:
            self.draw_start = (650, 650)
            self.draw_stop = (650, 650)
        elif 1 <= self.line <= 2:
            self.draw_start = (self.start[0], self.start[1] + (self.line - 1) * MULTIPLIER)
            self.draw_stop = (self.stop[0], self.stop[1] + (self.line - 1) * MULTIPLIER)
