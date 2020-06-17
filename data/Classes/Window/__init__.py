from ..Button import *


class Window:
    def __init__(self):
        self.sprites = pygame.sprite.Group()
        self.width = 0
        self.height = 0
        self.background = None

    def resize(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))

    def set_background(self, path):
        self.background = pygame.image.load(path)
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

    def click(self, mouse_pos):
        for sprite in self.sprites:
            if sprite.check_clicked(mouse_pos):
                sprite.clicked()
