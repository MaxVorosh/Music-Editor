import pygame
from ..load import load


def make_fon_by_rect(screen, intro_text, x1, x2, y1, y2, color_name, font_size=30):
    pygame.init()
    font = pygame.font.Font(None, font_size)
    text_coord = (y2 + y1) // 2 - (len(intro_text) * 21 + (len(intro_text) - 1) * 10) // 2
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(color_name))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = (x2 + x1) // 2 - string_rendered.get_width() // 2
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
