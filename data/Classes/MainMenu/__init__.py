import pygame
from ..Window import Window
from ..Button import Button
from ..SecondMenu import SecondMenu
from ..Info import Info
from ..Rules import Rules
import sys


class MainMenu(Window):
    def __init__(self):
        super().__init__()
        self.running = True
        self.ui()
        self.run()

    def ui(self):
        self.resize(640, 640)
        self.exit = Button(self, "data\\Sprites\\exit.png")
        self.exit.resize(80, 80)
        self.exit.move(560, 0)
        self.exit.set_func(self.exitFunc)
        self.start = Button(self, "data\\Sprites\\buttonStart.png")
        self.start.resize(100, 100)
        self.start.move(270, 270)
        self.start.set_func(self.startFunc)
        self.info = Button(self, 'data\\Sprites\\info_1.png')
        self.info.resize(80, 80)
        self.info.move(0, 0)
        self.info.set_func(self.get_info)
        self.rules = Button(self, 'data\\Sprites\\rules.png')
        self.rules.resize(80, 80)
        self.rules.move(280, 0)
        self.rules.set_func(self.show_rules)
        self.set_background('data\\Sprites\\bg.jpg')

    def startFunc(self):
        SecondMenu()

    def get_info(self):
        Info()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exitFunc()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click(event.pos)
            self.screen.fill((0, 0, 0))
            if self.background:
                self.screen.blit(self.background, (0, 0))
            self.sprites.draw(self.screen)
            pygame.display.flip()

    def show_rules(self):
        Rules()

    def exitFunc(self):
        pygame.quit()
        sys.exit()
