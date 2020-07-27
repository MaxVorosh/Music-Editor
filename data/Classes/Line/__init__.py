import pygame


class Line:
    def __init__(self, screen, start, stop):
        self.screen = screen
        self.start = start
        self.stop = stop

    def draw(self):
        pygame.draw.line(self.screen, pygame.Color('black'), self.start, self.stop, 3)
