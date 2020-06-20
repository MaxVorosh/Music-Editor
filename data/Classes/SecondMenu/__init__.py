import pygame
from ..Window import Window
from ..Button import Button
from ..Melodie import Melodie
from ..Name import Name
from ..KeyWindow import KeyWindow
from data.Functions.make_fon_by_rect import make_fon_by_rect
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
        result = cur.execute("SELECT id, name FROM Melodies").fetchall()
        self.ids = [i[0] for i in result]
        self.names = [i[1] for i in result]
        con.close()
        self.length = len(result)
        for i in range(self.length):
            if i % 2 == 0:
                btn = Button(self, "data\\Sprites\\old.png")
                btn.resize(256, 160)
                btn.move(10, 100 + i // 2 * 185)
                btn.set_func(self.go_to_melody, self.ids[i])
            else:
                btn = Button(self, "data\\Sprites\\old.png")
                btn.resize(256, 160)
                btn.move(375, 100 + i // 2 * 185)
                btn.set_func(self.go_to_melody, self.ids[i])
            self.melodies.append(btn)
        add = Button(self, "data\\Sprites\\add_1.png")
        add.resize(256, 160)
        add.move(10 + self.length % 2 * 365, 100 + self.length // 2 * 185)
        add.set_func(self.go_next)
        self.melodies.append(add)
        self.set_background('data\\Sprites\\bg.jpg')

    def GoToLast(self):
        self.running = False

    def go_next(self):
        n = Name()
        if n.string:
            k = KeyWindow(n.string)
            if k.is_do:
                Melodie(k.id)
                self.running = False
                m = SecondMenu()
            else:
                self.go_next()

    def run(self):
        start = 0
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exitFunc()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click(event.pos)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and start != 0:
                        start -= 2
                        for btn in self.melodies:
                            if btn.rect.y == -185:
                                btn.rect.y = 100
                            else:
                                btn.rect.y += 185
                    if event.key == pygame.K_DOWN and start <= self.length - 6:
                        start += 2
                        for btn in self.melodies:
                            if btn.rect.y == 100:
                                btn.rect.y = -185
                            else:
                                btn.rect.y -= 185

            self.screen.fill((0, 0, 0))
            if self.background:
                self.screen.blit(self.background, (0, 0))
            self.sprites.draw(self.screen)
            for i in range(start, self.length):
                if i % 2 == 0:
                    make_fon_by_rect(self.screen, self.names[i].split('\n'), 10, 266, 100 + (i - start) // 2 * 185,
                                     100 + (i - start) // 2 * 185 + 160, 'white')
                else:
                    make_fon_by_rect(self.screen, self.names[i].split('\n'), 375, 631, 100 + (i - start) // 2 * 185,
                                     100 + (i - start) // 2 * 185 + 160, 'white')
            pygame.display.flip()

    def exitFunc(self):
        pygame.quit()
        sys.exit()

    def go_to_melody(self, id):
        Melodie(id)
