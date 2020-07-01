import pygame
from ..Button import Button
from ..Window import Window
import sys
from data.Functions.make_fon import make_fon


class Rules(Window):
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
        text = ['Шаги для создания мелодии:', '1) Выберите символ для построения лесенки',
                '2) Нажимайте на галочку столько раз,', 'сколько символов Вам необходимо',
                '3) Если хотите прервать лесенку - нажмите на крест',
                '4) С помощью инструкций на экране, введите размер такта',
                '5) Чтобы добавить ноту, нажмите на соответствующую', 'клавишу нотной клавиатуры',
                '6) Чтобы поставить перед нотой дубль диез, или бекар,',
                'нажмите на соответствующую кнопку при выборе ноты',
                '7) После этого, выберите размер ноты,', 'нажав на соответствующий символ',
                '8) Для добавления паузы, нажмите на соответствуюший символ сверху',
                '9) Чтобы удалить символ, нажмите на delete',
                '10) Вы можете поменятть ключ мелодии нажав на него,',
                'если в мелодию не добавлено ни одной ноты',
                '11) Вы можете прокручивать мелодию вверх-вниз,',
                'при помощи соответствующих кнопок на клавиатуре',
                '12) Мелодия сохраняется автоматически при',
                'выходе из мелодии/программы']
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exitFunc()
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
