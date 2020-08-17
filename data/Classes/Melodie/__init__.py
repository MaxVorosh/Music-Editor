import pygame
import sys
import sqlite3
from ..Window import Window
from ..Button import Button
from ..Key import Key
from ..Stave import Stave
from ..Note import Note
from ..ClickedNote import ClickedNote
from ..TactLine import TactLine
from ..Line import Line
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
        self.lines = pygame.sprite.Group()
        self.none_tact_lines = []
        self.becar = None
        self.dubl = None
        self.point = None
        self.have_point = False
        self.points = 0
        self.note_x = []
        self.note_y = []
        self.first_note = []
        self.note_line = []
        self.union_lines = []
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
        if self.is_violin:
            self.up_note_1 = {'B': 135, 'C': 177, 'D': 170, 'E': 163, 'F': 156, 'G': 149, 'A': 142}
            self.up_note_2 = {'B': 170, 'C': 212, 'D': 205, 'E': 198, 'F': 191, 'G': 184, 'A': 177}
            self.up_note_3 = {'B': 121, 'C': 163, 'D': 156, 'E': 149, 'F': 142, 'G': 135, 'A': 128}
            self.up_note_4 = {'B': 72, 'C': 114, 'D': 107, 'E': 100, 'F': 93, 'G': 86, 'A': 79}
            self.up_note = {1: self.up_note_1, 2: self.up_note_2, 3: self.up_note_3, 4: self.up_note_4}
        else:
            self.up_note_1 = {'B': 184, 'E': 212, 'F': 205, 'G': 198, 'A': 191}
            self.up_note_2 = {'B': 135, 'C': 177, 'D': 170, 'E': 163, 'F': 156, 'G': 149, 'A': 142}
            self.up_note = {1: self.up_note_1, 2: self.up_note_2}
        self.sharp_on_stair = [142, 163, 135, 156, 177, 149, 170]
        self.flat_on_stair = [170, 149, 177, 156, 184, 163, 191]
        if self.stage == 5:
            self.draw_body()
            if self.is_violin:
                self.do_keyboard_violin()
            else:
                self.do_keyboard_bass()

    def run(self):
        MYEVENTTYPE = 27
        pygame.time.set_timer(MYEVENTTYPE, 300)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exitFunc()
                if event.type == MYEVENTTYPE:
                    self.save()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for note in self.clicked_note_group:
                        if note.check_clicked(event.pos):
                            note.clicked()
                    if event.button == 1:
                        self.click(event.pos)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DELETE:
                        self.delete_note()
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
                                    if self.is_violin:
                                        self.do_keyboard_violin()
                                    else:
                                        self.do_keyboard_bass()
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
            # if self.stage == 6:
            #     self.clicked_note_group.draw(self.screen)
            for i in range(self.sharps):
                self.stair.add(Note('sharp', 80 + i * 15, self.sharp_on_stair[i], (10, 30), False))
            for i in range(self.flats):
                self.stair.add(Note('flat', 80 + i * 15, self.flat_on_stair[i] - 7, (10, 30), False))
            self.stair.draw(self.screen)
            self.sprites.draw(self.screen)
            self.clicked_note_group.draw(self.screen)
            self.note_group.draw(self.screen)
            self.lines.draw(self.screen)
            for line in self.none_tact_lines:
                line.draw()
            for line in self.note_line:
                line.draw()
            for numb, line in self.union_lines:
                line.draw()
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
        for i in self.clicked_note_group:
            i.kill()
        data = ['full', 'half', 'quater', 'small', 'very_small']
        sizes = [(18, 12), (13, 42), (13, 42), (26, 46), (26, 47)]
        for i in range(5):
            if self.weight + 1 / 2 ** i <= self.up / self.down:
                ClickedNote(self, data[i], 100 + i * 75, 100 - sizes[i][1], 1 / 2 ** i, sizes[i])
        self.point = Button(self, 'data\\Sprites\\point.png')
        self.point.resize(10, 10)
        self.point.move(451, 75)
        self.point.set_func(self.do_point)
        if notes in self.becars.keys() and not self.becars[notes[0]]:
            self.becar = Button(self, 'data\\Sprites\\becar.png')
            self.becar.resize(15, 50)
            self.becar.move(520, 50)
            self.becar.set_func(self.do_becar)
            self.dubl = Button(self, 'data\\Sprites\\dubl.png')
            self.dubl.resize(28, 40)
            self.dubl.move(471, 60)
            self.dubl.set_func(self.double)
        else:
            self.dubl = None
            self.becar = None
        self.stage = 6
        self.cur_notes = notes
        # self.note_symb += [(i, self.oct) for i in self.cur_notes]
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
        if self.dubl is not None:
            self.dubl.kill()
            self.dubl = None
        if self.becar is not None:
            self.becar.kill()
            self.becar = None
        if self.point is not None:
            self.point.kill()
            self.point = None
        self.weight += weight
        if self.have_point:
            self.weight += weight / 2
        self.stage = 5
        data = []
        for note in range(len(self.cur_notes)):
            if self.cur_notes[note] == 'P':
                con = sqlite3.connect('data\\db\\Melodies.db')
                cur = con.cursor()
                id = cur.execute(
                    'SELECT id FROM Notes WHERE Note = "' + self.cur_notes[note] + '" AND Octave = 0 ' +
                    ' AND weight = ' + str(weight) + ' AND Point = ' + str(int(self.have_point))).fetchall()
                if not id:
                    cur.execute(
                        'INSERT INTO Notes(Note, Octave, weight, Point) Values ("' + self.cur_notes[note] + '", 0, '
                        + str(weight) + ', ' + str(int(self.have_point)) + ')')
                id = cur.execute(
                    'SELECT id FROM Notes WHERE Note = "' + self.cur_notes[note] + '" AND Octave = 0 ' +
                    ' AND weight = ' + str(weight) + ' AND Point = ' + str(int(self.have_point))).fetchall()[0]
                data.append(id[0])
                if weight == 1:
                    name = 'full_pause'
                    size = (20, 10)
                    y = 161
                elif weight == 0.5:
                    name = 'half_pause'
                    size = (20, 10)
                    y = 166
                elif weight == 0.25:
                    name = 'quater_pause'
                    size = (20, 56)
                    y = 168
                elif weight == 0.125:
                    name = 'small_pause'
                    size = (33, 56)
                    y = 168
                elif weight == 0.0625:
                    name = 'very_small_pause'
                    size = (28, 56)
                    y = 168
                n = Note(name, 85 + (self.sharps + self.flats) * 15 + 60 + (
                        len(self.note_group) - 1 - self.symb - self.points) * 38 + self.symb * 11, y, size, False)
                self.note_group.add(n)
                self.note_y.append(n.rect.y)
                self.note_x.append(n.rect.x)
                self.first_note.append(['P', weight, False, 1, 0])
                con.commit()
                con.close()
            elif self.cur_notes[note] == '#' or self.cur_notes[note] == 'b' or self.cur_notes[note] == '|':
                con = sqlite3.connect('data\\db\\Melodies.db')
                cur = con.cursor()
                id = cur.execute(
                    'SELECT id FROM Notes WHERE Note = "' + self.cur_notes[note] + '" AND Octave = ' + str(self.oct) +
                    ' AND weight = 0 AND Point = False').fetchall()
                if not id:
                    cur.execute(
                        'INSERT INTO Notes(Note, Octave, weight, Point) Values ("' + self.cur_notes[note] + '", ' + str(
                            self.oct) + ', 0, ' + str(int(self.have_point)) + ')')
                id = cur.execute(
                    'SELECT id FROM Notes WHERE Note = "' + self.cur_notes[note] + '" AND Octave = ' + str(self.oct) +
                    ' AND weight = 0 AND Point = False').fetchall()[0]
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
                    cur.execute('SELECT * FROM Notes WHERE Note = "' + str(self.cur_notes[-1]) + '"').fetchall()
                if not next_note:
                    cur.execute(
                        'INSERT INTO Notes(Note, Octave, weight, Point) Values ("' + self.cur_notes[-1] + '", ' + str(
                            self.oct) + ', ' + str(weight) + ', ' + str(int(self.have_point)) + ')')
                next_note = \
                    cur.execute('SELECT * FROM Notes WHERE Note = "' + str(self.cur_notes[-1]) + '"').fetchall()[
                        0]
                y = self.up_note[self.oct][next_note[1]]
                self.note_group.add(
                    Note(name, 85 + (self.sharps + self.flats) * 15 + 60 + (
                            len(self.note_group) - 1 - self.symb - self.points) * 38 + self.symb * 11,
                         y + add, size, False))
                self.symb += 1
                con.close()
            else:
                con = sqlite3.connect('data\\db\\Melodies.db')
                cur = con.cursor()
                id = cur.execute(
                    'SELECT id FROM Notes WHERE Note = "' + self.cur_notes[note] + '" AND Octave = ' + str(self.oct) +
                    ' AND weight = ' + str(weight) + ' AND Point = ' + str(int(self.have_point))).fetchall()
                if not id:
                    cur.execute(
                        'INSERT INTO Notes(Note, Octave, weight, Point) Values ("' + self.cur_notes[note] + '", ' + str(
                            self.oct) + ', ' + str(weight) + ', ' + str(int(self.have_point)) + ')')
                id = cur.execute(
                    'SELECT id FROM Notes WHERE Note = "' + self.cur_notes[note] + '" AND Octave = ' + str(self.oct) +
                    ' AND weight = ' + str(weight) + ' AND Point = ' + str(int(self.have_point))).fetchall()[0]
                data.append(id[0])
                con.commit()
                con.close()
                if self.first_note and weight - self.have_point * weight / 2 <= 1 / 8:
                    if self.weight - weight - weight * self.have_point / 2 == 0 or weight != self.first_note[-1][1]:
                        self.first_note.append([self.cur_notes, weight, False, 1, self.oct])
                    else:
                        self.first_note[-1][3] = self.first_note[-1][3] + 1
                        self.first_note[-1][2] = True
                else:
                    self.first_note.append([self.cur_notes, weight, False, 1, self.oct])
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
                    name = 'very_small'
                    size = (30, 56)
                n = Note(name, 85 + self.points * 7 + (self.sharps + self.flats) * 15 + 60 + (
                        len(self.note_group) - 1 - self.symb - self.points) * 38 + self.symb * 11,
                         self.up_note[self.oct][self.cur_notes[note]] + add, size, True)
                self.note_group.add(n)
                if self.have_point:
                    self.note_group.add(Note('point', 85 + (self.sharps + self.flats) * 20 + 60 + (
                            len(self.note_group) - 1 - self.symb - self.points) * 38 + self.symb * 11 - 23,
                                             self.up_note[self.oct][self.cur_notes[note]], (10, 10), False))
                    self.points += 1
                self.note_x.append(n.rect.x)
                self.note_y.append(n.rect.y)
                if not ((128 <= self.note_y[-1] + size[1] - 14 <= 212 and n.up) or (
                        128 <= self.note_y[-1] + 14 <= 212 and not n.up)):
                    if n.up:
                        self.note_line.append(
                            Line(self.screen, (self.note_x[-1] - 4, self.note_y[-1] + size[1] - 4),
                                 (self.note_x[-1] + size[0] + 4, self.note_y[-1] + size[1] - 4)))
                    else:
                        self.note_line.append(
                            Line(self.screen, (self.note_x[-1] - 7, self.note_y[-1] + 11),
                                 (self.note_x[-1] + size[0] - 7, self.note_y[-1] + 11)))
        if self.body[0]:
            self.body.append(data)
        else:
            self.body[0] = data
        self.cur_notes = []
        if self.weight == self.up / self.down:
            self.weight = 0
            self.lines.add(TactLine(85 + (self.sharps + self.flats) * 15 + 60 + (
                    len(self.note_group) - self.symb - 1 - self.points) * 38 + self.symb * 11 - 3, 142))
            self.becars = {'A': False, 'B': False, 'C': False, 'D': False, 'E': False, 'F': False, 'G': False}
        self.have_point = False
        self.do_pause()
        self.union_notes_if_it_can()

    def do_keyboard_violin(self):
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
            self.do_pause()

    def do_keyboard_bass(self):
        C = Button(self, 'data\\Sprites\\C.png')
        C.resize(21, 122)
        C.move(10 + 154, 508)
        C.set_func(self.add_note, 'C', 2)
        self.notes['C'].append(C)
        D = Button(self, 'data\\Sprites\\D.png')
        D.resize(24, 124)
        D.move(31 + 154, 506)
        D.set_func(self.add_note, 'D', 2)
        self.notes['D'].append(D)
        for i in range(2):
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
        C_ = Button(self, 'data\\Sprites\\black.png')
        C_.resize(15, 67)
        C_.move(23 + 154, 510)
        C_.set_func(self.sharp_or_flat, 'CD', 2)
        self.notes['C#'].append(C_)
        D_ = Button(self, 'data\\Sprites\\black.png')
        D_.resize(15, 67)
        D_.move(50 + 154, 510)
        D_.set_func(self.sharp_or_flat, 'DE', 2)
        self.notes['D#'].append(D_)
        self.do_pause()

    def draw_body(self):
        for step in self.body:
            cur_notes = ''
            for i in range(len(step)):
                fl = False
                con = sqlite3.connect('data\\db\\Melodies.db')
                cur = con.cursor()
                note = cur.execute('SELECT * FROM Notes WHERE id = ' + str(step[i])).fetchall()[0]
                add = -20
                # self.note_symb.append((note[1], note[2]))
                cur_notes += (note[1])
                if i == len(step) - 1:
                    if self.first_note and note[3] - note[3] * note[4] < 1 / 8:
                        if self.first_note[-1][1] != note[3] or self.weight == 0 or cur_notes[0] == 'P':
                            self.first_note.append([cur_notes, note[3], False, 1, note[2]])
                        else:
                            self.first_note[-1][3] = self.first_note[-1][3] + 1
                            self.first_note[-1][2] = True
                    else:
                        self.first_note.append([cur_notes, note[3], False, 1, note[2]])
                self.weight += note[3] + note[3] / 2 * note[4]
                if self.weight == self.up / self.down:
                    self.weight = 0
                    self.lines.add(TactLine(85 + (self.sharps + self.flats) * 15 + 60 + (
                            len(self.note_group) - self.symb - self.points) * 38 + self.symb * 11 - 3, 142))
                if note[1] != '#' and note[1] != 'b' and note[1] != '|' and note[1] != 'P':
                    y = self.up_note[note[2]][note[1]]
                if note[1] == 'P':
                    fl = True
                    add = 0
                    if note[3] == 1:
                        name = 'full_pause'
                        size = (20, 10)
                        y = 161
                    elif note[3] == 0.5:
                        name = 'half_pause'
                        size = (20, 10)
                        y = 166
                    elif note[3] == 0.25:
                        name = 'quater_pause'
                        size = (20, 56)
                        y = 168
                    elif note[3] == 0.125:
                        name = 'small_pause'
                        size = (33, 56)
                        y = 168
                    elif note[3] == 0.0625:
                        name = 'very_small_pause'
                        size = (28, 56)
                        y = 168
                else:
                    if note[3] == 1:
                        name = 'full'
                        size = (21, 14)
                        add = 0
                        fl = True
                    elif note[3] == 0.5:
                        name = 'half'
                        size = (15, 49)
                        fl = True
                    elif note[3] == 0.25:
                        name = 'quater'
                        size = (15, 49)
                        fl = True
                    elif note[3] == 0.125:
                        name = 'small'
                        size = (30, 54)
                        fl = True
                    elif note[3] == 0.0625:
                        name = 'very_small'
                        size = (30, 56)
                        fl = True
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
                        next_note = cur.execute('SELECT * FROM Notes WHERE id = ' + str(step[-1])).fetchall()[0]
                        y = self.up_note[note[2]][next_note[1]]
                n = Note(name, 85 + (self.sharps + self.flats) * 15 + 60 + (
                        len(self.note_group) - 1 - self.symb - self.points) * 38 + self.symb * 11,
                         y + add, size, fl)
                self.note_group.add(n)
                if fl:
                    self.note_y.append(n.rect.y)
                    self.note_x.append(n.rect.x)
                    if not ((128 <= self.note_y[-1] + size[1] - 14 <= 212 and n.up) or (
                            128 <= self.note_y[-1] + 14 <= 212 and not n.up)):
                        if n.up:
                            self.note_line.append(
                                Line(self.screen, (self.note_x[-1] - 4, self.note_y[-1] + size[1] - 4),
                                     (self.note_x[-1] + size[0] + 4, self.note_y[-1] + size[1] - 4)))
                        else:
                            self.note_line.append(
                                Line(self.screen, (self.note_x[-1] - 7, self.note_y[-1] + 11),
                                     (self.note_x[-1] + size[0] - 7, self.note_y[-1] + 11)))
                if note[4]:
                    self.note_group.add(Note('point', 85 + (self.sharps + self.flats) * 15 + 60 + (
                            len(self.note_group) - 1 - self.symb - self.points) * 38 + self.symb * 11 - 23,
                                             self.up_note[note[2]][note[1]], (10, 10), False))
                    self.points += 1
                if note[1] == '#' or note[1] == 'b' or note[1] == '|':
                    self.symb += 1
                con.close()
        self.union_notes_if_it_can(True)

    def sharp_or_flat(self, notes, oct):
        self.let = False
        self.point.kill()
        for note in self.clicked_note_group:
            note.kill()
        self.becar.kill()
        self.becar = None
        self.dubl.kill()
        self.dubl = None
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
        self.dubl.kill()
        self.dubl = None
        self.becars[self.cur_notes[-1]] = True

    def double(self):
        self.becar.kill()
        self.becar = None
        if self.point is not None:
            self.point.kill()
            self.point = None
        for i in self.clicked_note_group:
            i.kill()
        self.dubl.kill()
        self.sharp = Button(self, 'data\\Sprites\\sharp.png')
        self.sharp.resize(20, 40)
        self.sharp.move(100, 20)
        self.sharp.set_func(self.add_double, '##')
        self.flat = Button(self, 'data\\Sprites\\flat.png')
        self.flat.resize(20, 40)
        self.flat.move(500, 20)
        self.flat.set_func(self.add_double, 'bb')

    def add_double(self, symb):
        self.cur_notes = symb + self.cur_notes
        self.sharp.kill()
        self.flat.kill()
        data = ['full', 'half', 'quater', 'small', 'very_small']
        sizes = [(18, 12), (13, 42), (13, 42), (26, 46), (26, 47)]
        for i in range(5):
            if self.weight + 1 / 2 ** i <= self.up / self.down:
                ClickedNote(self, data[i], 100 + i * 75, 100 - sizes[i][1], 1 / 2 ** i, sizes[i])
        self.point = Button(self, 'data\\Sprites\\point.png')
        self.point.resize(10, 10)
        self.point.move(451, 75)
        self.point.set_func(self.do_point)

    def do_pause(self):
        self.cur_notes = 'P'
        self.oct = 0
        data = ['full_pause', 'half_pause', 'quater_pause', 'small_pause', 'very_small_pause']
        sizes = [(41, 20), (42, 21), (18, 50), (24, 41), (25, 50)]
        for i in range(5):
            if self.weight + 1 / 2 ** i <= self.up / self.down:
                ClickedNote(self, data[i], 100 + i * 85, 100 - sizes[i][1], 1 / 2 ** i, sizes[i])

    def do_point(self):
        self.point.kill()
        self.have_point = True
        for note in self.clicked_note_group:
            note.kill()
        data = ['full', 'half', 'quater', 'small', 'very_small']
        sizes = [(18, 12), (13, 42), (13, 42), (26, 46), (26, 47)]
        for i in range(5):
            if self.weight + 1 / 2 ** i + 1 / 2 ** (i + 1) <= self.up / self.down:
                ClickedNote(self, data[i], 100 + i * 75, 100 - sizes[i][1], 1 / 2 ** i, sizes[i])

    def union_notes_if_it_can(self, all=False):
        if not self.note_y:
            return
        if all:
            cur = 0
            w = 0
            for i in range(len(self.body)):
                ans = self.check_union(self.body[i][-1], self.body[cur][-1])
                if not ans[0] or ans[1] + w > 1 or ans[1] > 1 / 8:
                    self.pre_union_notes(cur, i - 1, ans[1] == 1 / 8)
                    cur = i
                w += ans[1]
                if w > 1:
                    w -= 1
            if cur != len(self.body) - 1:
                self.pre_union_notes(cur, len(self.body) - 1, ans[1] == 1 / 8)
        else:
            cur = len(self.body) - 1
            second = cur
            ans = (0, 0)
            w = 0
            start = 0
            for i in range(len(self.body)):
                ans = self.check_union(self.body[i][-1], self.body[i][-1])
                w += ans[1]
                if w > 1:
                    w -= 1
                    start = i
                if i == len(self.body) - 1:
                    fl = ans[1] == 1 / 8
            ans = (0, 0)
            for i in range(len(self.body) - 2, max(start - 1, -1), -1):
                ans = self.check_union(self.body[cur][-1], self.body[i][-1])
                if not ans[0] or ans[1] > 1 / 8:
                    second = i + 1
                    break
                elif i == max(start - 1, -1) + 1:
                    second = i
                w += ans[1]
            if cur - second > 1:
                #TODO Исправить удаление линий
                for i in range(len(self.union_lines)):
                    if second <= self.union_lines[i][0] <= cur:
                        self.union_lines.pop(i)
            if ans != (0, 0) and second != cur:
                if self.none_tact_lines:
                    self.none_tact_lines.pop()
                    if ans[1] == 1 / 16:
                        self.none_tact_lines.pop()
                self.pre_union_notes(second, cur, fl)

    def pre_union_notes(self, second, cur, fl):
        st = 1
        while st <= cur - second + 1:
            st *= 2
        st //= 2
        l = second
        while l <= cur:
            self.union_notes(l, l + st - 1, fl)
            l = l + st + 1
            while st > cur - second + 1:
                st //= 2

    def union_notes(self, l, r, is_eight):
        if l >= r:
            return
        cnt = -1
        up, down = 0, 0
        for i in self.note_group:
            if i.image_name in ['full', 'quater', 'half', 'small', 'very_small']:
                cnt += 1
                if l <= cnt <= r:
                    if i.start_up:
                        up += 1
                    else:
                        down += 1
        cnt = -1
        fl = up >= down
        for i in self.note_group:
            if i.image_name in ['quater', 'small', 'very_small']:
                cnt += 1
                if l <= cnt <= r:
                    if fl ^ i.up:
                        i.change_up()
                    i.change_image('quater', (15, 49))
                    self.note_y[cnt] = i.rect.y
        max_y, min_y = 0, 1000
        max_y_ind, min_y_ind = 0, 0
        tn = 5
        second_ind = 0
        for i in range(l, r + 1):
            if max_y < self.note_y[i]:
                max_y = self.note_y[i]
                max_y_ind = i
            if min_y > self.note_y[i]:
                min_y = self.note_y[i]
                min_y_ind = i
        for i in range(l, r + 1):
            cur_tn = 5
            if not fl:
                if i != max_y_ind:
                    if max_y == self.note_y[i]:
                        cur_tn = 0
                    else:
                        cur_tn = (max_y - self.note_y[i]) / abs(self.note_x[i] - self.note_x[max_y_ind])
            else:
                if i != min_y_ind:
                    if min_y == self.note_y[i]:
                        cur_tn = 0
                    else:
                        cur_tn = (min_y - self.note_y[i]) / abs(self.note_x[i] - self.note_x[min_y_ind])
            if abs(tn) > abs(cur_tn):
                tn = cur_tn
                second_ind = i
        if not fl:
            start_y = max_y + (self.note_x[max_y_ind] - self.note_x[l]) * tn
            stop_y = max_y - (self.note_x[r] - self.note_x[max_y_ind]) * tn
            if second_ind < max_y_ind:
                start_y = max_y - (self.note_x[max_y_ind] - self.note_x[l]) * tn
                stop_y = max_y + (self.note_x[r] - self.note_x[max_y_ind]) * tn

        else:
            start_y = min_y + (self.note_x[min_y_ind] - self.note_x[l]) * tn
            stop_y = min_y - (self.note_x[r] - self.note_x[min_y_ind]) * tn
            # if second_min_y_ind > min_y_ind:
            #     start_y, stop_y = stop_y, start_y
            if second_ind < min_y_ind:
                start_y = min_y - (self.note_x[min_y_ind] - self.note_x[l]) * tn
                stop_y = min_y + (self.note_x[r] - self.note_x[min_y_ind]) * tn
        cnt = -1
        for i in self.note_group:
            if i.image_name in ['full', 'quater', 'half', 'small', 'very_small']:
                cnt += 1
                if l <= cnt <= r:
                    if not fl:
                        need_y = max_y - (self.note_x[cnt] - self.note_x[max_y_ind]) * tn + 49
                        if start_y < stop_y:
                            need_y = max_y + (self.note_x[cnt] - self.note_x[max_y_ind]) * tn + 49
                    else:
                        need_y = min_y + (self.note_x[cnt] - self.note_x[min_y_ind]) * tn
                        if start_y < stop_y:
                            need_y = min_y - (self.note_x[cnt] - self.note_x[min_y_ind]) * tn
                    if fl:
                        self.union_lines.append((cnt, Line(self.screen, (self.note_x[cnt] + 13, min(need_y, i.rect.y - 5)),
                                                     (self.note_x[cnt] + 13, max(need_y, i.rect.y + i.size[1] - 5)), 2)))
                    else:
                        self.union_lines.append((cnt, Line(self.screen, (self.note_x[cnt], min(need_y, i.rect.y + 7)),
                                                     (self.note_x[cnt], max(need_y, i.rect.y + i.size[1])), 2)))

        if fl:
            self.none_tact_lines.append(
                Line(self.screen, (self.note_x[l] + 15, round(start_y)), (self.note_x[r] + 15, round(stop_y))))
            if not is_eight:
                self.none_tact_lines.append(
                    Line(self.screen, (self.note_x[l] + 15, round(start_y) + 7),
                         (self.note_x[r] + 15, round(stop_y) + 7)))
        else:
            self.none_tact_lines.append(
                Line(self.screen, (self.note_x[l], round(start_y) + 49), (self.note_x[r], round(stop_y) + 49)))
            if not is_eight:
                self.none_tact_lines.append(
                    Line(self.screen, (self.note_x[l], round(start_y) + 42), (self.note_x[r], round(stop_y) + 42)))

    def check_union(self, sample_id, current_id):
        con = sqlite3.connect('data\\db\\Melodies.db')
        cur = con.cursor()
        sample_note = cur.execute("SELECT Weight, Point FROM Notes WHERE id = " + str(sample_id)).fetchall()[0]
        current_note = cur.execute("SELECT Weight, Point FROM Notes WHERE id = " + str(current_id)).fetchall()[0]
        con.close()
        return ((sample_note[0] - sample_note[0] / 2 * sample_note[1] == current_note[0] - current_note[0] / 2 *
                 current_note[1]) and not (sample_note[1] and current_note[1]),
                current_note[0] - current_note[0] / 2 * current_note[1])

    def delete_note(self):
        if not self.body[0]:
            return
        con = sqlite3.connect('data\\db\\Melodies.db')
        cur = con.cursor()
        delete_note = cur.execute("SELECT Weight, Point FROM Notes WHERE id = " + str(self.body[-1][-1])).fetchall()[0]
        weight = delete_note[0] + delete_note[0] / 2 * delete_note[1]
        self.body.pop()
        y = self.note_y[-1]
        self.note_x.pop()
        self.note_y.pop()
        self.weight -= weight
        if self.weight < 0:
            self.weight += 1
            cnt = -1
            for i in self.lines:
                cnt += 1
                if cnt == len(self.lines) - 1:
                    i.kill()
        cnt = -1
        for i in self.note_group:
            if i.image_name in ['full', 'quater', 'half', 'small', 'very_small', 'full_pause', 'quater_pause',
                                'half_pause', 'small_pause', 'very_small_pause']:
                cnt += 1
                if cnt == len(self.body):
                    if not ((128 <= y + i.size[1] - 14 <= 212 and i.up) or (
                            128 <= y + 14 <= 212 and not i.up)):
                        self.note_line.pop()
                    i.kill()
            else:
                if cnt >= len(self.body) - 1:
                    i.kill()
        if not self.body:
            self.body = [[]]
            self.first_note.pop()
            return
        last_note = ''
        octave = 0
        for i in self.body[-1]:
            rez = cur.execute("SELECT Note, Octave FROM Notes WHERE id = " + str(i)).fetchall()[0]
            last_note += rez[0]
            octave = rez[1]
        if self.first_note[-1][2]:
            if self.union_lines[-1][0] == len(self.note_y):
                self.union_lines.pop()
        if ((last_note != self.first_note[-1][0] or octave != self.first_note[-1][-1])
                or self.weight == 0 or last_note == 'P'):
            self.first_note.pop()
        else:
            self.none_tact_lines.pop()
            self.first_note[-1][3] = self.first_note[-1][3] - 1
            self.union_notes_if_it_can()
            if self.first_note[-1][3] == 1:
                self.body.pop()
                if self.union_lines[-1][0] == len(self.note_y):
                    self.union_lines.pop()
                self.note_x.pop()
                self.note_y.pop()
                cnt = -1
                for i in self.note_group:
                    if i.image_name in ['full', 'quater', 'half', 'small', 'very_small']:
                        cnt += 1
                        if cnt == len(self.body):
                            if not ((128 <= y + i.size[1] - 14 <= 212 and i.up) or (
                                    128 <= y + 14 <= 212 and not i.up)):
                                self.note_line.pop()
                            i.kill()
                    else:
                        if cnt >= len(self.body) - 1:
                            i.kill()
                if not self.body:
                    self.body = [[]]
                self.cur_notes = [last_note]
                self.oct = octave
                self.draw_note(self.first_note[-1][1])
        con.close()
