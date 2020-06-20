import pygame
import sys
import sqlite3
from ..Window import Window
from ..Button import Button
from ..Key import Key
from ..Stave import Stave
from ..Note import Note
from data.Functions.make_fon_by_rect import make_fon_by_rect


class Melodie(Window):
    def __init__(self, id):
        super().__init__()
        self.running = True
        self.id = id
        con = sqlite3.connect('data\\db\\Melodies.db')
        cur = con.cursor()
        melodie = cur.execute('SELECT * FROM Melodies WHERE id == ' + str(self.id)).fetchall()[0]
        self.is_violin = melodie[1]
        self.sharps = melodie[2]
        self.flats = melodie[3]
        self.body = melodie[4]
        self.name = melodie[5]
        self.stage = 0
        self.stair = pygame.sprite.Group()
        self.ui()
        self.run()

    def ui(self):
        self.staves = pygame.sprite.Group()
        self.staves.add(Stave(0, 140))
        self.staves.add(Stave(0, 260))
        self.staves.add(Stave(0, 380))
        self.resize(640, 640)
        self.last = Button(self, 'data\\Sprites\\last_black.png')
        self.last.resize(80, 80)
        self.last.move(0, 0)
        self.last.set_func(self.GoToLast)
        self.last = Button(self, 'data\\Sprites\\exit_black.png')
        self.last.resize(80, 80)
        self.last.move(560, 0)
        self.last.set_func(self.exitFunc)
        self.sharp = Button(self, 'data\\Sprites\\sharp.png')
        self.sharp.resize(20, 40)
        self.sharp.move(100, 20)
        self.sharp.set_func(self.first_sharp)
        self.flat = Button(self, 'data\\Sprites\\flat.png')
        self.flat.resize(20, 40)
        self.flat.move(500, 20)
        self.flat.set_func(self.first_flat)
        self.keys = [Key(self, self.is_violin, -10, 140), Key(self, self.is_violin, -10, 260),
                     Key(self, self.is_violin, -10, 380)]
        self.notes = {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'A#': [], 'C#': [], 'D#': [],
                      'F#': [], 'G#': []}
        self.up_note_y = {'B': 170, 'C': 163, 'D': 156, 'E': 149, 'F': 142, 'G': 135, 'A': 177}
        self.sharp_on_stair = [142, 163, 135, 156, 177, 149, 170]
        self.flat_on_stair = [170, 149, 177, 156, 184, 163, 191]
        for i in range(4):
            C = Button(self, 'data\\Sprites\\C.png')
            C.resize(21, 122)
            C.move(10 + i * 154, 508)
            C.set_func(self.add_note)
            self.notes['C'].append(C)
            D = Button(self, 'data\\Sprites\\D.png')
            D.resize(24, 124)
            D.move(31 + i * 154, 506)
            D.set_func(self.add_note)
            self.notes['D'].append(D)
            E = Button(self, 'data\\Sprites\\E.png')
            E.resize(23, 124)
            E.move(55 + i * 154, 506)
            E.set_func(self.add_note)
            self.notes['E'].append(E)
            F = Button(self, 'data\\Sprites\\F.png')
            F.resize(21, 123)
            F.move(76 + i * 154, 507)
            F.set_func(self.add_note)
            self.notes['F'].append(F)
            G = Button(self, 'data\\Sprites\\G.png')
            G.resize(24, 105)
            G.move(97 + i * 154, 525)
            G.set_func(self.add_note)
            self.notes['G'].append(G)
            A = Button(self, 'data\\Sprites\\A.png')
            A.resize(21, 122)
            A.move(121 + i * 154, 508)
            A.set_func(self.add_note)
            self.notes['A'].append(A)
            B = Button(self, 'data\\Sprites\\B.png')
            B.resize(22, 133)
            B.move(142 + i * 154, 497)
            B.set_func(self.add_note)
            self.notes['B'].append(B)
            C_ = Button(self, 'data\\Sprites\\black.png')
            C_.resize(15, 67)
            C_.move(23 + i * 154, 510)
            self.notes['C#'].append(C_)
            D_ = Button(self, 'data\\Sprites\\black.png')
            D_.resize(15, 67)
            D_.move(50 + i * 154, 510)
            self.notes['D#'].append(D_)
            F_ = Button(self, 'data\\Sprites\\black.png')
            F_.resize(15, 67)
            F_.move(89 + i * 154, 510)
            self.notes['F#'].append(F_)
            G_ = Button(self, 'data\\Sprites\\black.png')
            G_.resize(15, 67)
            G_.move(114 + i * 154, 510)
            self.notes['G#'].append(G_)
            A_ = Button(self, 'data\\Sprites\\black.png')
            A_.resize(15, 67)
            A_.move(140 + i * 154, 510)
            self.notes['A#'].append(A_)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exitFunc()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click(event.pos)
            self.screen.fill((255, 255, 255))
            if self.background:
                self.screen.blit(self.background, (0, 0))
            # self.staves.draw(self.screen)
            if self.stage == 0:
                make_fon_by_rect(self.screen, ['Выберите символ слева или справа', 'для построения лесенки'], 140, 480,
                                 0, 80, 'black')
            if self.stage == 1:
                for i in range(self.sharps):
                    self.stair.add(Note('sharp', 0, 80 + i * 15, self.sharp_on_stair[i] - 15))
            if self.stage == 2:
                for i in range(self.flats):
                    self.stair.add(Note('flat', 0, 80 + i * 15, self.flat_on_stair[i] - 22))
                    # pygame.draw.circle(self.screen, pygame.Color('green'),
                    #                    (80 + i * 10, self.note_y[self.note_on_stair[6 - i]]), 5)
            self.staves.draw(self.screen)
            # pygame.draw.circle(self.screen, pygame.Color('green'), (100, self.note_y['A']), 5)
            self.stair.draw(self.screen)
            self.sprites.draw(self.screen)
            pygame.display.flip()

    def exitFunc(self):
        pygame.quit()
        sys.exit()

    def add_note(self):
        pass

    def GoToLast(self):
        self.running = False

    def next_stage(self):
        self.accept.kill()
        self.reject.kill()

    def add_symb(self):
        if self.stage == 1:
            self.sharps += 1
            if self.sharps == 7:
                self.next_stage()
        if self.stage == 2:
            self.flats += 1
            if self.flats == 7:
                self.next_stage()

    def first_flat(self):
        self.stage = 2
        self.get_stair()

    def first_sharp(self):
        self.stage = 1
        self.get_stair()

    def get_stair(self):
        self.accept = Button(self, 'data\\Sprites\\accept_black.png')
        self.accept.resize(80, 80)
        self.accept.move(187, 0)
        self.accept.set_func(self.add_symb)
        self.reject = Button(self, 'data\\Sprites\\reject.png')
        self.reject.resize(80, 80)
        self.reject.move(374, 0)
        self.reject.set_func(self.next_stage)
        self.sharp.kill()
        self.flat.kill()
