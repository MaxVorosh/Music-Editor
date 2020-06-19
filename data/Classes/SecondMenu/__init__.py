import pygame
from ..Window import Window
from ..Button import Button
from ..Melodie import Melodie
from ..Name import Name
import sys
import sqlite3


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
        self.melodies = []
        con = sqlite3.connect('data\\db\\Melodies.db')
        cur = con.cursor()
        result = cur.execute("SELECT name FROM Melodies").fetchall()
        length = len(result)
        for i in range(length):
            if i % 2 == 0:
                btn = Button(self, "data\\Sprites\\add_1.png")
                btn.resize(256, 160)
                btn.move(10, 150 + i // 2 * 170)
                btn.set_func(self.go_next)
            else:
                btn = Button(self, "data\\Sprites\\add_1.png")
                btn.resize(256, 160)
                btn.move(375, 150 + i // 2 * 170)
                btn.set_func(self.go_next)
            self.melodies.append(btn)
        add = Button(self, "data\\Sprites\\add_1.png")
        add.resize(256, 160)
        add.move(10 + length % 2 * 365, 150 + length // 2 * 170)
        add.set_func(self.go_next)
        self.melodies.append(add)
        self.set_background('data\\Sprites\\bg.jpg')

    def GoToLast(self):
        self.running = False

    def go_next(self):
        n = Name()
        if n.string:
            Melodie()

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
