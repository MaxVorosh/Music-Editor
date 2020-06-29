import pygame
import sys
import sqlite3
from ..Window import Window
from ..Button import Button
from ..Key import Key
from ..Stave import Stave
from ..Note import Note
from ..ClickedNote import ClickedNote
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
        self.body = [i.split() for i in str(melodie[4]).split(';')]
        self.name = melodie[5]
        self.up = melodie[6]
        self.down = melodie[7]
        self.stage = melodie[8]
        self.line = melodie[9]
        self.symb = 0
        self.let = True
        self.weight = 0
        self.stair = pygame.sprite.Group()
        self.clicked_note_group = pygame.sprite.Group()
        self.note_group = pygame.sprite.Group()
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
        if self.stage == 0:
            self.sharp = Button(self, 'data\\Sprites\\sharp.png')
            self.sharp.resize(20, 40)
            self.sharp.move(100, 20)
            self.sharp.set_func(self.first_sharp)
            self.flat = Button(self, 'data\\Sprites\\flat.png')
            self.flat.resize(20, 40)
            self.flat.move(500, 20)
            self.flat.set_func(self.first_flat)
        else:
            self.get_stair()
        self.keys = [Key(self, self.is_violin, -10, 140), Key(self, self.is_violin, -10, 260),
                     Key(self, self.is_violin, -10, 380)]
        for key in self.keys:
            key.set_func(key.update, self.stage)
        self.notes = {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'A#': [], 'C#': [], 'D#': [],
                      'F#': [], 'G#': []}
        self.becars = {'A': False, 'B': False, 'C': False, 'D': False, 'E': False, 'F': False, 'G': False}
        self.up_note_1 = {'B': 135, 'C': 177, 'D': 170, 'E': 163, 'F': 156, 'G': 149, 'A': 142}
        self.up_note_2 = {'B': 170, 'C': 212, 'D': 205, 'E': 198, 'F': 191, 'G': 184, 'A': 177}
        self.up_note_3 = {'B': 121, 'C': 163, 'D': 156, 'E': 149, 'F': 142, 'G': 135, 'A': 128}
        self.up_note_4 = {'B': 72, 'C': 114, 'D': 107, 'E': 100, 'F': 93, 'G': 86, 'A': 79}
        self.up_note = {1: self.up_note_1, 2: self.up_note_2, 3: self.up_note_3, 4: self.up_note_4}
        self.sharp_on_stair = [142, 163, 135, 156, 177, 149, 170]
        self.flat_on_stair = [170, 149, 177, 156, 184, 163, 191]
        if self.stage == 5:
            self.do_keyboard()
            self.draw_body()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exitFunc()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for note in self.clicked_note_group:
                        if note.check_clicked(event.pos):
                            note.clicked()
                    if event.button == 1:
                        self.click(event.pos)
                if event.type == pygame.KEYDOWN:
                    if 3 <= self.stage <= 4:
                        chis = -1
                        if event.key == pygame.K_2:
                            chis = 2
                        if event.key == pygame.K_3:
                            chis = 3
                        if event.key == pygame.K_4:
                            chis = 4
                        if event.key == pygame.K_6:
                            chis = 6
                        if event.key == pygame.K_8:
                            chis = 8
                        if chis != -1:
                            if self.down == 0 and (chis == 4 or chis == 8):
                                self.down = chis
                                self.stage = 4
                            elif self.down != 0:
                                if chis <= self.down:
                                    self.up = chis
                                    self.stage = 5
                                    self.do_keyboard()
                                    for key in self.keys:
                                        key.set_func(key.update, self.stage)
            self.screen.fill((255, 255, 255))
            self.staves.draw(self.screen)
            if self.stage == 0:
                make_fon_by_rect(self.screen, ['Выберите символ слева или справа', 'для построения лесенки'], 140, 480,
                                 0, 80, 'black')
            if 3 <= self.stage <= 4:
                make_fon_by_rect(self.screen, ['С помощью цифр на клавиатуре', 'выберите размер такта.',
                                               'Первое число пойдёт вниз, второе - вверх'], 140, 480, 0, 80, 'black')
            if self.up != 0:
                make_fon_by_rect(self.screen, [str(self.up)], 80 + (self.sharps + self.flats) * 15 + 5,
                                 80 + (self.sharps + self.flats) * 15 + 19, 130, 144, 'black', 56)
            if self.down != 0:
                make_fon_by_rect(self.screen, [str(self.down)], 80 + (self.sharps + self.flats) * 15 + 5,
                                 80 + (self.sharps + self.flats) * 15 + 19, 162, 176, 'black', 56)
            if self.stage == 6:
                self.clicked_note_group.draw(self.screen)
            for i in range(self.sharps):
                self.stair.add(Note('sharp', 80 + i * 15, self.sharp_on_stair[i], (10, 30)))
            for i in range(self.flats):
                self.stair.add(Note('flat', 80 + i * 15, self.flat_on_stair[i] - 7, (10, 30)))
            self.stair.draw(self.screen)
            self.sprites.draw(self.screen)
            self.note_group.draw(self.screen)
            pygame.display.flip()

    def exitFunc(self):
        self.save()
        pygame.quit()
        sys.exit()

    def add_note(self, notes, oct):
        try:
            self.sharp.kill()
            self.flat.kill()
        except:
            pass
        data = ['full', 'half', 'quater', 'small', 'very small']
        sizes = [(24, 16), (17, 56), (17, 56), (34, 61), (34, 63)]
        for i in range(5):
            if self.weight + 1 / 2 ** i <= self.up / self.down:
                ClickedNote(self, data[i], 100 + i * 75, 100 - sizes[i][1], 1 / 2 ** i, sizes[i])
        if len(notes) == 1 and not self.becars[notes[0]]:
            self.becar = Button(self, 'data\\Sprites\\becar.png')
            self.becar.move(520, 33)
            self.becar.set_func(self.do_becar)
        self.stage = 6
        self.cur_notes = notes
        self.oct = oct

    def GoToLast(self):
        self.save()
        self.running = False

    def next_stage(self):
        self.accept.kill()
        self.reject.kill()
        self.stage = 3

    def add_symb(self):
        if self.stage == 1:
            self.sharps += 1
            if self.sharps == 7:
                self.next_stage()
                self.stage = 4
        if self.stage == 2:
            self.flats += 1
            if self.flats == 7:
                self.next_stage()
                self.stage = 4

    def first_flat(self):
        self.sharp.kill()
        self.flat.kill()
        self.stage = 2
        self.get_stair()

    def first_sharp(self):
        self.sharp.kill()
        self.flat.kill()
        self.stage = 1
        self.get_stair()

    def get_stair(self):
        if self.stage >= 3:
            pass
        else:
            self.accept = Button(self, 'data\\Sprites\\accept_black.png')
            self.accept.resize(80, 80)
            self.accept.move(187, 0)
            self.accept.set_func(self.add_symb)
            self.reject = Button(self, 'data\\Sprites\\reject.png')
            self.reject.resize(80, 80)
            self.reject.move(374, 0)
            self.reject.set_func(self.next_stage)

    def save(self):
        if self.stage == 6:
            self.stage = 5
        con = sqlite3.connect('data\\db\\Melodies.db')
        cur = con.cursor()
        copy_body = self.body[:]
        for i in range(len(copy_body)):
            copy_body[i] = [str(j) for j in copy_body[i]]
            copy_body[i] = ' '.join(copy_body[i])
        body = ';'.join(copy_body)
        text = ('UPDATE Melodies\nSET is_violin = ' + str(self.is_violin) + ', sharp = ' + str(self.sharps) +
                ', flat = ' + str(self.flats) + ', body = "' + body + '", up = ' + str(self.up) +
                ', down = ' + str(self.down) +
                ', stage = ' + str(self.stage) + '\nWHERE id = ' + str(self.id))
        cur.execute(text)
        con.commit()
        con.close()

    def draw_note(self, weight):
        for i in self.clicked_note_group:
            i.kill()
        if self.becar is not None:
            self.becar.kill()
            self.becar = None
        self.weight += weight
        if self.weight == self.up / self.down:
            self.weight = 0
            self.becars = {'A': False, 'B': False, 'C': False, 'D': False, 'E': False, 'F': False, 'G': False}
        self.stage = 5
        data = []
        for note in range(len(self.cur_notes)):
            # print(self.symb, len(self.note_group))
            next = 60
            if self.cur_notes[note] == '#' or self.cur_notes[note] == 'b' or self.cur_notes[note] == '|':
                con = sqlite3.connect('data\\db\\Melodies.db')
                cur = con.cursor()
                id = cur.execute(
                    'SELECT id FROM Notes WHERE Note = "' + self.cur_notes[note] + '" AND Octave = ' + str(self.oct) +
                    ' AND weight = 0').fetchall()
                if not id:
                    cur.execute(
                        'INSERT INTO Notes(Note, Octave, weight) Values ("' + self.cur_notes[note] + '", ' + str(
                            self.oct) + ', 0)')
                id = cur.execute(
                    'SELECT id FROM Notes WHERE Note = "' + self.cur_notes[note] + '" AND Octave = ' + str(self.oct) +
                    ' AND weight = 0').fetchall()[0]
                data.append(id[0])
                con.commit()
                size = (10, 30)
                if self.cur_notes[note] == '#':
                    name = 'sharp'
                elif self.cur_notes[note] == '|':
                    name = 'becar'
                else:
                    name = 'flat'
                add = 0
                next_note = \
                    cur.execute('SELECT * FROM Notes WHERE Note = "' + str(self.cur_notes[note + 1]) + '"').fetchall()
                if not next_note:
                    cur.execute(
                        'INSERT INTO Notes(Note, Octave, weight) Values ("' + self.cur_notes[note + 1] + '", ' + str(
                            self.oct) + ', ' + str(weight) + ')')
                next_note = \
                    cur.execute('SELECT * FROM Notes WHERE Note = "' + str(self.cur_notes[note + 1]) + '"').fetchall()[
                        0]
                y = self.up_note[self.oct][next_note[1]]
                self.note_group.add(
                    Note(name, 80 + (self.sharps + self.flats) * 15 + next + (
                            len(self.note_group) - 1 - self.symb) * 35 + self.symb * 11,
                         y + add, size))
                self.symb += 1
                con.close()
            else:
                con = sqlite3.connect('data\\db\\Melodies.db')
                cur = con.cursor()
                id = cur.execute(
                    'SELECT id FROM Notes WHERE Note = "' + self.cur_notes[note] + '" AND Octave = ' + str(self.oct) +
                    ' AND weight = ' + str(weight)).fetchall()
                if not id:
                    cur.execute(
                        'INSERT INTO Notes(Note, Octave, weight) Values ("' + self.cur_notes[note] + '", ' + str(
                            self.oct) + ', ' + str(weight) + ')')
                id = cur.execute(
                    'SELECT id FROM Notes WHERE Note = "' + self.cur_notes[note] + '" AND Octave = ' + str(self.oct) +
                    ' AND weight = ' + str(weight)).fetchall()[0]
                data.append(id[0])
                con.commit()
                con.close()
                add = -20
                if weight == 1:
                    name = 'full'
                    size = (21, 14)
                    add = 0
                elif weight == 0.5:
                    name = 'half'
                    size = (15, 49)
                elif weight == 0.25:
                    name = 'quater'
                    size = (15, 49)
                elif weight == 0.125:
                    name = 'small'
                    size = (30, 54)
                elif weight == 0.0625:
                    name = 'very small'
                    size = (30, 56)
                self.note_group.add(
                    Note(name, 80 + (self.sharps + self.flats) * 15 + next + (
                            len(self.note_group) - 1 - self.symb) * 35 + self.symb * 11,
                         self.up_note[self.oct][self.cur_notes[note]] + add, size))

        if self.body[0]:
            self.body.append(data)
        else:
            self.body[0] = data
        self.cur_notes = []

    def do_keyboard(self):
        for i in range(4):
            C = Button(self, 'data\\Sprites\\C.png')
            C.resize(21, 122)
            C.move(10 + i * 154, 508)
            C.set_func(self.add_note, 'C', i + 1)
            self.notes['C'].append(C)
            D = Button(self, 'data\\Sprites\\D.png')
            D.resize(24, 124)
            D.move(31 + i * 154, 506)
            D.set_func(self.add_note, 'D', i + 1)
            self.notes['D'].append(D)
            E = Button(self, 'data\\Sprites\\E.png')
            E.resize(23, 124)
            E.move(55 + i * 154, 506)
            E.set_func(self.add_note, 'E', i + 1)
            self.notes['E'].append(E)
            F = Button(self, 'data\\Sprites\\F.png')
            F.resize(21, 123)
            F.move(76 + i * 154, 507)
            F.set_func(self.add_note, 'F', i + 1)
            self.notes['F'].append(F)
            G = Button(self, 'data\\Sprites\\G.png')
            G.resize(24, 105)
            G.move(97 + i * 154, 525)
            G.set_func(self.add_note, 'G', i + 1)
            self.notes['G'].append(G)
            A = Button(self, 'data\\Sprites\\A.png')
            A.resize(21, 122)
            A.move(121 + i * 154, 508)
            A.set_func(self.add_note, 'A', i + 1)
            self.notes['A'].append(A)
            B = Button(self, 'data\\Sprites\\B.png')
            B.resize(22, 133)
            B.move(142 + i * 154, 497)
            B.set_func(self.add_note, 'B', i + 1)
            self.notes['B'].append(B)
            C_ = Button(self, 'data\\Sprites\\black.png')
            C_.resize(15, 67)
            C_.move(23 + i * 154, 510)
            C_.set_func(self.sharp_or_flat, 'CD', i + 1)
            self.notes['C#'].append(C_)
            D_ = Button(self, 'data\\Sprites\\black.png')
            D_.resize(15, 67)
            D_.move(50 + i * 154, 510)
            D_.set_func(self.sharp_or_flat, 'DE', i + 1)
            self.notes['D#'].append(D_)
            F_ = Button(self, 'data\\Sprites\\black.png')
            F_.resize(15, 67)
            F_.move(89 + i * 154, 510)
            F_.set_func(self.sharp_or_flat, 'FG', i + 1)
            self.notes['F#'].append(F_)
            G_ = Button(self, 'data\\Sprites\\black.png')
            G_.resize(15, 67)
            G_.move(114 + i * 154, 510)
            G_.set_func(self.sharp_or_flat, 'GA', i + 1)
            self.notes['G#'].append(G_)
            A_ = Button(self, 'data\\Sprites\\black.png')
            A_.resize(15, 67)
            A_.move(140 + i * 154, 510)
            A_.set_func(self.sharp_or_flat, 'AB', i + 1)
            self.notes['A#'].append(A_)

    def draw_body(self):
        for step in self.body:
            for i in range(len(step)):
                con = sqlite3.connect('data\\db\\Melodies.db')
                cur = con.cursor()
                note = cur.execute('SELECT * FROM Notes WHERE id = ' + str(step[i])).fetchall()[0]
                add = -20
                next = 60
                self.weight += note[3]
                if self.weight == self.up / self.down:
                    self.weight = 0
                if note[1] != '#' and note[1] != 'b' and note[1] != '|':
                    y = self.up_note[note[2]][note[1]]
                if note[3] == 1:
                    name = 'full'
                    size = (21, 14)
                    add = 0
                elif note[3] == 0.5:
                    name = 'half'
                    size = (15, 49)
                elif note[3] == 0.25:
                    name = 'quater'
                    size = (15, 49)
                elif note[3] == 0.125:
                    name = 'small'
                    size = (30, 54)
                elif note[3] == 0.0625:
                    name = 'very small'
                    size = (30, 56)
                else:
                    if note[1] == '#':
                        name = 'sharp'
                        add = 0
                    elif note[1] == 'b':
                        name = 'flat'
                        add = -7
                    elif note[1] == '|':
                        name = 'becar'
                        add = 0
                    size = (10, 30)
                    next_note = cur.execute('SELECT * FROM Notes WHERE id = ' + str(step[i + 1])).fetchall()[0]
                    y = self.up_note[note[2]][next_note[1]]
                self.note_group.add(
                    Note(name, 80 + (self.sharps + self.flats) * 15 + next + (
                            len(self.note_group) - 1 - self.symb) * 35 + self.symb * 11,
                         y + add, size))
                if note[1] == '#' or note[1] == 'b' or note[1] == '|':
                    self.symb += 1
                con.close()

    def sharp_or_flat(self, notes, oct):
        self.let = False
        for note in self.clicked_note_group:
            note.kill()
        self.sharp = Button(self, 'data\\Sprites\\sharp.png')
        self.sharp.resize(20, 40)
        self.sharp.move(100, 20)
        self.sharp.set_func(self.go_to_add_note, '#' + notes[0], oct)
        self.flat = Button(self, 'data\\Sprites\\flat.png')
        self.flat.resize(20, 40)
        self.flat.move(500, 20)
        self.flat.set_func(self.go_to_add_note, 'b' + notes[1], oct)

    def go_to_add_note(self, notes, oct):
        self.let = True
        self.add_note(notes, oct)

    def do_becar(self):
        self.cur_notes = '|' + self.cur_notes
        self.becar.kill()
        self.becar = None
        self.becars[self.cur_notes[-1]] = True
