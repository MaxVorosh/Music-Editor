import pygame
from data.Functions.make_fon import make_fon
from ..Window import Window
from ..Button import Button
import sys


class Name(Window):
    def __init__(self):
        super().__init__()
        self.string = 'Введите название'
        self.running = True
        self.is_nool = True
        self.caps = False
        self.shift = False
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
        self.accept = Button(self, 'data\\Sprites\\accept.png')
        self.accept.resize(80, 80)
        self.accept.move(280, 0)
        self.accept.set_func(self.GoToNext)
        self.set_background('data\\Sprites\\bg.jpg')

    def run(self):
        fps = 60
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exitFunc()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click(event.pos)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                        self.shift = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                        self.shift = True
                    if event.key == pygame.K_CAPSLOCK:
                        self.caps = not self.caps
                    char = ''
                    if event.key == pygame.K_q:
                        char = 'q'
                    if event.key == pygame.K_w:
                        char = 'w'
                    if event.key == pygame.K_e:
                        char = 'e'
                    if event.key == pygame.K_r:
                        char = 'r'
                    if event.key == pygame.K_t:
                        char = 't'
                    if event.key == pygame.K_y:
                        char = 'y'
                    if event.key == pygame.K_u:
                        char = 'u'
                    if event.key == pygame.K_i:
                        char = 'i'
                    if event.key == pygame.K_o:
                        char = 'o'
                    if event.key == pygame.K_p:
                        char = 'p'
                    if event.key == pygame.K_a:
                        char = 'a'
                    if event.key == pygame.K_s:
                        char = 's'
                    if event.key == pygame.K_d:
                        char = 'd'
                    if event.key == pygame.K_f:
                        char = 'f'
                    if event.key == pygame.K_g:
                        char = 'g'
                    if event.key == pygame.K_h:
                        char = 'h'
                    if event.key == pygame.K_j:
                        char = 'j'
                    if event.key == pygame.K_k:
                        char = 'k'
                    if event.key == pygame.K_l:
                        char = 'l'
                    if event.key == pygame.K_z:
                        char = 'z'
                    if event.key == pygame.K_x:
                        char = 'x'
                    if event.key == pygame.K_c:
                        char = 'c'
                    if event.key == pygame.K_v:
                        char = 'v'
                    if event.key == pygame.K_b:
                        char = 'b'
                    if event.key == pygame.K_n:
                        char = 'n'
                    if event.key == pygame.K_m:
                        char = 'm'
                    if self.shift ^ self.caps:
                        char = char.upper()
                    if event.key == pygame.K_KP_ENTER:
                        char = '\n'
                    if event.key == pygame.K_SPACE:
                        char = ' '
                    if self.is_nool:
                        if char:
                            self.string = char
                            self.is_nool = False
                    else:
                        self.string += char
                    if event.key == pygame.K_BACKSPACE:
                        if not self.is_nool:
                            self.string = self.string[0:-1]
                            if len(self.string) == 0:
                                self.is_nool = True
                                self.string = 'Введите название'
            self.screen.fill((0, 0, 0))
            if self.background:
                self.screen.blit(self.background, (0, 0))
            make_fon(self.screen, self.string.split('\n'))
            self.sprites.draw(self.screen)
            clock.tick(fps)
            pygame.display.flip()

    def exitFunc(self):
        pygame.quit()
        sys.exit()

    def GoToLast(self):
        self.string = ''
        self.running = False

    def GoToNext(self):
        self.running = False
