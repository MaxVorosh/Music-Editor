import pygame
from ..Button import Button
from ..Window import Window
import sys
from data.Functions.make_fon import make_fon


class Info(Window):
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
        self.last = Button(self, "data\\Sprites\\Last_1.png")
        self.last.resize(80, 80)
        self.last.move(0, 0)
        self.last.set_func(self.goToLast)
        self.set_background("data\\Sprites\\bg.jpg")

    def run(self):
        text = ['Создатель приложения:', 'MaxVorosh/MaxVor',
                'За обучение нотам спасибо Пасичник Олесе']
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click(event.pos)
            self.screen.fill((0, 0, 0))
            make_fon(self.screen, text)
            self.sprites.draw(self.screen)
            pygame.display.flip()

    def goToLast(self):
        self.running = False

    def exitFunc(self):
        pygame.quit()
        sys.exit()
