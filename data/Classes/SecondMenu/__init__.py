import pygame
from ..Window import Window
from ..Button import Button
import sys


class SecondMenu(Window):
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
        self.last = Button(self, "data\\Sprites\\last_1.png")
        self.last.resize(80, 80)
        self.last.move(0, 0)
        self.last.set_func(self.GoToLast)
        self.up_left = Button(self, "data\\Sprites\\add_1.png")
        self.up_left.resize(256, 160)
        self.up_left.move(10, 151)
        self.up_left.set_func(self.go_next)
        self.up_right = Button(self, "data\\Sprites\\add_1.png")
        self.up_right.resize(256, 160)
        self.up_right.move(374, 151)
        self.up_right.set_func(self.go_next)
        self.down_left = Button(self, "data\\Sprites\\add_1.png")
        self.down_left.resize(256, 160)
        self.down_left.move(10, 329)
        self.down_left.set_func(self.go_next)
        self.down_right = Button(self, "data\\Sprites\\add_1.png")
        self.down_right.resize(256, 160)
        self.down_right.move(374, 329)
        self.down_right.set_func(self.go_next)
        self.set_background('data\\Sprites\\bg.jpg')

    def GoToLast(self):
        self.running = False

    def go_next(self):
        pass

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

    def exitFunc(self):
        pygame.quit()
        sys.exit()