import pygame
from ..Window import Window
from ..Button import Button
import sys
import sqlite3
from data.Functions.make_fon_up import make_fon_up


class KeyWindow(Window):
    def __init__(self, name):
        super().__init__()
        self.running = True
        self.name = name
        self.is_do = False
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
        self.violin = Button(self, 'data\\Sprites\\violin.png')
        self.violin.resize(100, 100)
        self.violin.move(147, 270)
        self.violin.set_func(self.add_violin)
        self.bass = Button(self, 'data\\Sprites\\bass.png')
        self.bass.resize(100, 100)
        self.bass.move(393, 270)
        self.bass.set_func(self.add_bass)
        self.set_background('data\\Sprites\\bg.jpg')

    def GoToLast(self):
        self.running = False

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
            make_fon_up(self.screen, ['Выберите скрипичный или басовый ключ', 'с помощью нажатия на него'], 80)
            self.sprites.draw(self.screen)
            pygame.display.flip()

    def exitFunc(self):
        pygame.quit()
        sys.exit()

    def add_violin(self):
        con = sqlite3.connect('data\\db\\Melodies.db')
        cur = con.cursor()
        cur.execute('INSERT INTO Melodies (is_violin, name) VALUES (True, "' + self.name + '")')
        con.commit()
        res = cur.execute('SELECT id FROM Melodies').fetchall()
        self.id = res[-1][0]
        con.close()
        self.is_do = True
        self.running = False

    def add_bass(self):
        con = sqlite3.connect('data\\db\\Melodies.db')
        cur = con.cursor()
        cur.execute('INSERT INTO Melodies (is_violin, name) VALUES (False, "' + self.name + '")')
        con.commit()
        res = cur.execute('SELECT id FROM Melodies').fetchall()
        self.id = res[-1][0]
        con.close()
        self.is_do = True
        self.running = False
