import pygame


class Line:
    def __init__(self, screen, start, stop, width=3):
        self.screen = screen
        self.start = start
        self.stop = stop
        self.width = width

    def draw(self):
        pygame.draw.line(self.screen, pygame.Color('black'), self.start, self.stop, self.width)
