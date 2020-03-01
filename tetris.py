import pygame
import os
from random import randint as rand

pygame.init()
pygame.mixer.init()
all_sprites = pygame.sprite.Group()
figure = pygame.sprite.Group()
next_figure = pygame.sprite.Group()
down_border = pygame.sprite.Group()
left_border = pygame.sprite.Group()
right_border = pygame.sprite.Group()
size = w, h = 800, 600
screen = pygame.display.set_mode(size)
pygame.mixer.music.load('music\\tetris.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)
fps = 100
speed = 25
score = 0
constant_speed = True
mode = 'Низкая'


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Figure(pygame.sprite.Sprite):
    image = load_image("fig.png", -1)
    image = pygame.transform.scale(image, (50, 50))

    def __init__(self, pos, col, speed):
        global fps
        super().__init__(figure)
        self.image = pygame.transform.chop(Figure.image,
                                           pygame.Rect(25 * col[0], 25 * col[1], 25, 25))
        self.rect = pygame.Rect(0, 0, 25, 25)
        self.rect.x = pos[0] // 25 * 25
        self.rect.y = pos[1] // 25 * 25
        self.fps = fps
        self.speed = speed
        self.y = self.rect.y
        self.x = self.rect.x

    def next_to_now(self):
        global fig
        for i in range(len(next_fig)):
            fig[i].image = pygame.transform.scale(fig[i].image, (25, 25))
            fig[i].rect.x = fig[i].x
            fig[i].rect.y = fig[i].y

    def next_draw(self):
        global next_fig
        for i in range(len(next_fig)):
            next_fig[i].image = pygame.transform.scale(next_fig[i].image, (15, 15))
            next_fig[i].rect.x = (next_fig[i].rect.x // 25 + 17) * 15
            next_fig[i].rect.y = (next_fig[i].rect.y // 25 + 6) * 15

    def sdvig(self):
        global fig
        for i in fig:
            i.y += i.speed / i.fps
            i.rect.y = i.y // 25 * 25
        for i in fig:
            if pygame.sprite.spritecollideany(i, down_border) or \
                    pygame.sprite.spritecollideany(i, all_sprites):
                self.fix_figure()

    def move(self, dx, dy):
        global fig
        flag = False
        for i in fig:
            i.rect.x += dx
            i.rect.y += dy
            i.y += dy
            i.x += dx
            if (pygame.sprite.spritecollideany(i, down_border) or
                    pygame.sprite.spritecollideany(i, right_border) or
                    pygame.sprite.spritecollideany(i, left_border) or
                    pygame.sprite.spritecollideany(i, all_sprites)):
                flag = True
        if flag:
            for i in fig:
                i.rect.x -= dx
                i.rect.y -= dy
                i.y -= dy
                i.x -= dx

    def fall(self):
        global fig
        flag = False
        while True:
            for i in fig:
                i.rect.y += 25
                i.y += 25
            for i in fig:
                if pygame.sprite.spritecollideany(i, down_border) or \
                        pygame.sprite.spritecollideany(i, all_sprites):
                    self.fix_figure()
                    flag = True
            if flag:
                break

    def fix_figure(self):
        global fig, board, end
        for i in fig:
            i.add(all_sprites)
            i.speed = 0
            i.remove(figure)
            i.y += 0.01
            i.rect.y = i.y // 25 * 25 - 25
            board.board[(i.rect.y - board.top) // 25][(i.rect.x - board.left) // 25] = i
            if i.rect.y < board.top:
                end = True
        fig = []

    def rotate(self):
        global fig
        xrot = 50
        yrot = 50
        for i in fig:
            xrot += i.x
            yrot += i.y
        xrot /= 4
        yrot /= 4
        for i in fig:
            dx = i.x - xrot
            dy = i.y - yrot
            i.x = xrot - dy - 25 + 0.000001
            i.y = yrot + dx
            i.rect.y = i.y // 25 * 25
            i.rect.x = i.x // 25 * 25
        sch = 0
        while any([pygame.sprite.spritecollideany(i, all_sprites) for i in fig]) or \
                any([pygame.sprite.spritecollideany(i, left_border) for i in fig]) or \
                any([pygame.sprite.spritecollideany(i, right_border) for i in fig]):
            for i in fig:
                if sch == 0:
                    i.x += 25
                    i.rect.x += 25
                elif sch == 1:
                    i.x -= 50
                    i.rect.x -= 50
                elif sch == 2:
                    i.x += 75
                    i.rect.x += 75
                elif sch == 3:
                    i.x -= 100
                    i.rect.x -= 100
                elif sch == 4:
                    i.x += 50
                    i.rect.x += 50
                elif sch == 5:
                    while any([pygame.sprite.spritecollideany(i, left_border) for i in fig]):
                        for f in fig:
                            f.rect.x += 25
                            f.x += 25
                    while any([pygame.sprite.spritecollideany(i, right_border) for i in fig]):
                        for f in fig:
                            f.rect.x -= 25
                            f.x -= 25
                elif sch > 5:
                    i.y -= 25
                    i.rect.y -= 25
            sch += 1


def create_figure(pos, type):
    col = (rand(0, 1), rand(0, 1))
    if type == 1:
        return [Figure([pos[0], pos[1] - 25], col, speed),
                Figure([pos[0] + 25, pos[1] - 25], col, speed),
                Figure([pos[0] + 25, pos[1]], col, speed),
                Figure([pos[0] + 50, pos[1]], col, speed)]
    elif type == 2:
        return [Figure([pos[0], pos[1]], col, speed),
                Figure([pos[0] + 25, pos[1]], col, speed),
                Figure([pos[0] + 25, pos[1] - 25], col, speed),
                Figure([pos[0] + 50, pos[1] - 25], col, speed)]
    elif type == 3:
        return [Figure([pos[0], pos[1] - 50], col, speed),
                Figure([pos[0] + 25, pos[1] - 50], col, speed),
                Figure([pos[0], pos[1] - 25], col, speed),
                Figure([pos[0], pos[1]], col, speed)]
    elif type == 4:
        return [Figure([pos[0], pos[1] - 50], col, speed),
                Figure([pos[0] + 25, pos[1] - 50], col, speed),
                Figure([pos[0] + 25, pos[1] - 25], col, speed),
                Figure([pos[0] + 25, pos[1]], col, speed)]
    elif type == 5 or type == 7:
        return [Figure([pos[0], pos[1] - 25], col, speed),
                Figure([pos[0] + 25, pos[1] - 25], col, speed),
                Figure([pos[0] + 25, pos[1]], col, speed),
                Figure([pos[0], pos[1]], col, speed)]
    elif type == 6 or type == 8:
        return [Figure([pos[0], pos[1] - 75], col, speed),
                Figure([pos[0], pos[1] - 50], col, speed),
                Figure([pos[0], pos[1] - 25], col, speed),
                Figure([pos[0], pos[1]], col, speed)]
    elif type == 9 or type == 10:
        return [Figure([pos[0], pos[1] - 25], col, speed),
                Figure([pos[0] - 25, pos[1]], col, speed),
                Figure([pos[0], pos[1]], col, speed),
                Figure([pos[0] + 25, pos[1]], col, speed)]


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 50
        self.top = 75
        self.cell_size = 25

    def render(self):
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(screen, (100, 100, 255),
                                 pygame.Rect(self.left + self.cell_size * i,
                                             self.top + self.cell_size * j,
                                             self.cell_size, self.cell_size), 1)

    def check(self):
        global score
        flag = False
        strokes = 0
        for i in range(len(self.board)):
            if all(map(lambda x: x != 0, self.board[i])):
                strokes += 1
                for j in range(len(self.board[i])):
                    self.board[i][j].remove(all_sprites)
                    self.board[i][j] = 0
            if any(map(lambda x: x != 0, self.board[i])):
                flag = True
            if flag and all(map(lambda x: x == 0, self.board[i])):
                for j in range(i):
                    self.board[i - j] = self.board[i - j - 1] + []
                    for f in self.board[i - j]:
                        if f:
                            f.rect.y += 25
                            f.y += 25
                self.board[0] = [0] * self.width
        if strokes == 1:
            score += 10 * speed
        elif strokes == 2:
            score += 25 * speed
        elif strokes == 3:
            score += 65 * speed
        elif strokes == 4:
            score += 150 * speed


class Border(pygame.sprite.Sprite):
    def __init__(self, type, x, y, w, h):
        super().__init__(type)
        self.rect = pygame.Rect(x, y, w, h)


class Button:
    def __init__(self, x, y, w, h, text):
        self.text = text
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.button = pygame.Rect(x, y, w, h)

    def is_mouse_on_button(self, pos):
        return self.x < pos[0] < self.x + self.w and \
               self.y < pos[1] < self.y + self.h

    def draw(self):
        if self.is_mouse_on_button(pygame.mouse.get_pos()):
            col = pygame.Color('#999900')
        else:
            col = pygame.Color('#009999')
        pygame.draw.rect(screen, col, self.button)
        pygame.draw.rect(screen, (255, 255, 255), self.button, 1)

        text = font1.render(self.text, 1, (100, 255, 100))
        text_x = self.x + self.w // 2 - text.get_width() // 2
        text_y = self.y + self.h // 2 - text.get_height() // 2
        screen.blit(text, (text_x, text_y))


class Mode_Button(Button):
    def draw(self):
        super().draw()
        if self.is_mouse_on_button(pygame.mouse.get_pos()):
            if self.text == 'Низкая':
                text = 'Очки копятся медленно'
            elif self.text == 'Средняя':
                text = 'Очки копятся в 2 раза быстрее, чем на низкой'
            elif self.text == 'Высокая':
                text = 'Очки копятся в 2 раза быстрее, чем на средней'
            elif self.text == 'Растущая':
                text = 'Скорость игры постоянно увеличивается, скорость накопления очков зависит от скорости игры'
            text = font2.render(text, 1, (100, 255, 100))
            screen.blit(text, (w // 2 - text.get_width() // 2, 550))
            f = open('results\\' + self.text + '.txt', 'r')
            text = font2.render('Лучший результат: ' + f.read(), 1, (100, 255, 100))
            f.close()
            screen.blit(text, (w // 2 - text.get_width() // 2, 575))


class Button_Group:
    def __init__(self, *args):
        self.buttons = args

    def draw(self):
        for button in self.buttons:
            button.draw()

    def is_mouse_on_button(self, pos):
        return any(map(lambda button: button.is_mouse_on_button(pos), self.buttons))


class Slider:
    def __init__(self, y, text):
        self.y = y
        self.text = text
        self.slider = pygame.Rect(450 - 8, self.y - 15 + 18, 16, 30)

    def draw(self):
        text1 = font1.render(self.text, 1, (100, 255, 100))
        screen.blit(text1, (50, self.y))

        pygame.draw.line(screen, (100, 100, 100), (200, self.y + text1.get_height() // 2),
                         (700, self.y + text1.get_height() // 2), 3)
        pygame.draw.rect(screen, (50, 50, 50), self.slider)

        text2 = font1.render(str(self.procent()), 1, (100, 255, 100))
        screen.blit(text2, (725, self.y))

    def is_mouse_on(self, pos):
        return self.slider.y <= pos[1] <= self.slider.y + self.slider.h and 200 <= pos[0] <= 700

    def move(self, pos):
        self.slider.x = pos[0] - 8
        if self.slider.x + 8 > 700:
            self.slider.x = 700 - 8
        if self.slider.x + 8 < 200:
            self.slider.x = 200 - 8

    def procent(self):
        return (self.slider.x + 8 - 200) * 100 // 500


clock = pygame.time.Clock()
font1 = pygame.font.Font(None, 50)
font2 = pygame.font.Font(None, 25)
font3 = pygame.font.Font(None, 80)
board = Board(10, 20)
Border(left_border, 25 + 12, 0, 1, 500)
Border(right_border, 75 + 250 - 13, 0, 1, 500)
Border(down_border, 50, 600 - 13, 250, 1)
fig = []
next_fig = []

play_button = Button(285, 150, 230, 50, 'Играть')
options_button = Button(285, 275, 230, 50, 'Настройки')
quit_button = Button(285, 400, 230, 50, 'Выход')
start_screen_buttons = Button_Group(play_button, options_button, quit_button)

mode_button_slow = Mode_Button(20, 200, 175, 200, 'Низкая')
mode_button_middle = Mode_Button(215, 200, 175, 200, 'Средняя')
mode_button_fast = Mode_Button(410, 200, 175, 200, 'Высокая')
mode_button_not_constant_speed = Mode_Button(605, 200, 175, 200, 'Растущая')
mode_buttons = Button_Group(mode_button_fast, mode_button_middle, mode_button_slow, mode_button_not_constant_speed)

volume_slider = Slider(75, 'Музыка')
back_button = Button(10, 10, 120, 40, 'Назад')

pause_continue_button = Button(285, 150, 230, 50, 'Продолжить')
pause_options_button = Button(285, 275, 230, 50, 'Настройки')
pause_quit_button = Button(285, 400, 230, 50, 'Выход')
pause_buttons = Button_Group(pause_continue_button, pause_options_button, pause_quit_button)

score_continue_button = Button(285, 400, 230, 50, 'Продолжить')


def clean_board():
    global all_sprites, figure, board, fig, next_fig, constant_speed
    all_sprites = pygame.sprite.Group()
    figure = pygame.sprite.Group()
    board = Board(10, 20)
    fig = []
    next_fig = []
    constant_speed = True


def start_screen():
    running = True
    play = False
    options = False
    while running:
        pygame.mixer.music.set_volume(volume_slider.procent() / 100)
        screen.fill(pygame.Color('#111199'))
        text = font3.render('Тетрис', 1, (100, 255, 100))
        screen.blit(text, (w // 2 - text.get_width() // 2, 25))
        start_screen_buttons.draw()
        pygame.display.flip()
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if play_button.is_mouse_on_button(pygame.mouse.get_pos()):
                        running = False
                        play = True
                    if options_button.is_mouse_on_button(pygame.mouse.get_pos()):
                        running = False
                        options = True
                    if quit_button.is_mouse_on_button(pygame.mouse.get_pos()):
                        running = False
    if play:
        mode_screen()
    elif options:
        options_screen('start_screen')


def game_screen():
    global end, all_sprites, fig, speed, score, board, next_fig, figure
    running = True
    quit = False
    end = False
    pause = False
    if not next_fig:
        next_fig = create_figure((150, 50), rand(1, 10))
    while running:
        pygame.mixer.music.set_volume(volume_slider.procent() / 100)
        screen.fill(pygame.Color('#111199'))
        all_sprites.draw(screen)

        text = font2.render('Следующая:', 1, (100, 255, 100))
        screen.blit(text, (board.left + 270, 50))

        if not fig:
            if not constant_speed:
                speed += 0.5
            fig = next_fig
            fig[0].next_to_now()
            next_fig = create_figure((150, 50), rand(1, 10))
            next_fig[0].next_draw()
        board.render()
        board.check()
        figure.draw(screen)
        pygame.draw.rect(screen, pygame.Color('#111199'), pygame.Rect(0, 0, board.left + 250, 75))
        fig[0].sdvig()

        text = font1.render('Очки: ' + str(int(score)), 1, (100, 255, 100))
        text_x = 400
        text_y = h // 2 - text.get_height() // 2
        screen.blit(text, (text_x, text_y))

        pygame.display.flip()
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit = True
            if event.type == pygame.KEYDOWN:
                if fig:
                    if event.key == pygame.K_LEFT:
                        fig[0].move(-25, 0)
                    if event.key == pygame.K_RIGHT:
                        fig[0].move(25, 0)
                    if event.key == pygame.K_DOWN:
                        fig[0].fall()
                    if event.key == pygame.K_SPACE:
                        fig[0].rotate()
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pause = True
        if end:
            running = False
    if end:
        score_screen()
    elif not quit and not pause:
        start_screen()
    elif pause:
        pause_screen()


def options_screen(caller):
    running = True
    move = False
    quit = False
    while running:
        pygame.mixer.music.set_volume(volume_slider.procent() / 100)
        screen.fill(pygame.Color('#111199'))
        volume_slider.draw()
        back_button.draw()

        text = font3.render('Управление', 1, (100, 255, 100))
        screen.blit(text, (w // 2 - text.get_width() // 2, 150))
        text = font1.render('Пробел - повернуть фигуру', 1, (100, 255, 100))
        screen.blit(text, (w // 2 - text.get_width() // 2, 300))
        text = font1.render('Стрелка вниз - "уронить" фигуру', 1, (100, 255, 100))
        screen.blit(text, (w // 2 - text.get_width() // 2, 350))
        text = font1.render('Стрелка влево - сместить фигуру влево', 1, (100, 255, 100))
        screen.blit(text, (w // 2 - text.get_width() // 2, 400))
        text = font1.render('Стрелка вправо - сместить фигуру вправо', 1, (100, 255, 100))
        screen.blit(text, (w // 2 - text.get_width() // 2, 450))
        text = font1.render('Escape - Пауза', 1, (100, 255, 100))
        screen.blit(text, (w // 2 - text.get_width() // 2, 500))

        pygame.display.flip()
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if volume_slider.is_mouse_on(pygame.mouse.get_pos()):
                        move = True
                    if back_button.is_mouse_on_button(pygame.mouse.get_pos()):
                        running = False
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    move = False
        if move:
            volume_slider.move(pygame.mouse.get_pos())
    if not quit:
        if caller == 'pause':
            pause_screen()
        elif caller == 'start_screen':
            start_screen()


def mode_screen():
    global constant_speed, speed, mode
    running = True
    play = False
    while running:
        pygame.mixer.music.set_volume(volume_slider.procent() / 100)
        screen.fill(pygame.Color('#111199'))
        text = font3.render('Выберете скорость игры', 1, (100, 255, 100))
        screen.blit(text, (w // 2 - text.get_width() // 2, 50))
        mode_buttons.draw()
        pygame.display.flip()
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if mode_button_slow.is_mouse_on_button(pygame.mouse.get_pos()):
                        speed = 25
                        mode = 'Низкая'
                        play = True
                    elif mode_button_middle.is_mouse_on_button(pygame.mouse.get_pos()):
                        speed = 50
                        mode = 'Средняя'
                        play = True
                    elif mode_button_fast.is_mouse_on_button(pygame.mouse.get_pos()):
                        speed = 100
                        mode = 'Высокая'
                        play = True
                    elif mode_button_not_constant_speed.is_mouse_on_button(pygame.mouse.get_pos()):
                        speed = 25
                        mode = 'Растущая'
                        constant_speed = False
                        play = True
        if play:
            running = False
            game_screen()


def pause_screen():
    running = True
    quit = False
    contin = False
    options = False
    while running:
        pygame.mixer.music.set_volume(volume_slider.procent() / 100)
        screen.fill(pygame.Color('#111199'))

        text = font3.render('Пауза', 1, (100, 255, 100))
        screen.blit(text, (w // 2 - text.get_width() // 2, 25))

        pause_buttons.draw()
        pygame.display.flip()
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if pause_continue_button.is_mouse_on_button(pygame.mouse.get_pos()):
                        running = False
                        contin = True
                    elif pause_options_button.is_mouse_on_button(pygame.mouse.get_pos()):
                        running = False
                        options = True
                    elif pause_quit_button.is_mouse_on_button(pygame.mouse.get_pos()):
                        running = False
                        quit = True
    if contin:
        game_screen()
    elif quit:
        score_screen()
    elif options:
        options_screen('pause')


def score_screen():
    global score
    clean_board()
    f = open('results\\' + mode + '.txt', 'r')
    high_score = int(f.read())
    f.close()
    high_score = max(score, high_score)
    f = open('results\\' + mode + '.txt', 'w')
    f.write(str(int(high_score)))
    f.close()
    running = True
    quit = False
    while running:
        pygame.mixer.music.set_volume(volume_slider.procent() / 100)
        screen.fill(pygame.Color('#111199'))

        text = font1.render('Ваш результат: ' + str(int(score)), 1, (100, 255, 100))
        screen.blit(text, (w // 2 - text.get_width() // 2, 200))
        text = font1.render('Лучший результат: ' + str(int(high_score)), 1, (100, 255, 100))
        screen.blit(text, (w // 2 - text.get_width() // 2, 300))

        score_continue_button.draw()
        pygame.display.flip()
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if score_continue_button.is_mouse_on_button(pygame.mouse.get_pos()):
                        running = False
    if not quit:
        score = 0
        start_screen()


if __name__ == '__main__':
    start_screen()
