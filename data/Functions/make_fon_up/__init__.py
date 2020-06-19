import pygame
from ..load import load


def make_fon_up(screen, intro_text, height):
    pygame.init()
    fon = pygame.transform.scale(load('data\\Sprites\\bg.jpg'),
                                 (screen.get_width(), screen.get_height()))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = height // 2 - (len(intro_text) * 21 + (len(intro_text) - 1) * 10) // 2
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = screen.get_width() // 2 - string_rendered.get_width() // 2
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
