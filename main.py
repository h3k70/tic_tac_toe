import pygame
import random


# Цвета (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (82, 82, 82)
DARK_GRAY = (50, 50, 50)
DARK_PURPLE = (57, 0, 81)
PURPLE = (147, 0, 210)
DARK_ORANGE = (81, 70, 0)
ORANGE = (220, 190, 0)


class Button():
    def __init__(self, x,y,w,h, text=''):
        self.color = DARK_ORANGE
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.active = False
    def draw(self,win, text_size=40, outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.w+4,self.h+4),0)
        pygame.draw.rect(win, self.color, (self.x,self.y,self.w,self.h),0)
        if self.text != '':
            font = pygame.font.SysFont('comicsans', text_size)
            text = font.render(self.text, True, (0,0,0))
            win.blit(text, (self.x + (self.w/2 - text.get_width()/2), self.y + (self.h/3 - text.get_height()/2)))
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = ORANGE if self.active else DARK_ORANGE
    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.w:
            if pos[1] > self.y and pos[1] < self.y + self.h:
                self.active = True
                self.color = ORANGE
                return True
        self.active = False
        self.color = DARK_ORANGE
        return False

# Хотел сделать отдельный класс игрока, но немного не успеваю в срок
""""
class player():
    def __init__(self, sing='x'):
        self.sing = sing
"""

# Класс для ИИ в игре (хотя ИИ это очень громко сказано)
 # При инициализации создает массив со всеми возможными вариантами ходов
class Pc():
    def __init__(self, grid_size):
        self.move_list = []
        for i in range(grid_size):
            for j in range(grid_size):
                self.move_list.append((i, j))
        random.shuffle(self.move_list)
    def move(self):
        return self.move_list.pop()
    # Проверка на возможность хода (Остались ли варианты ходов)
    def can_move(self):
        if not len(self.move_list) == 0:
            return True

# Класс игрового поля, содержит в себе данные об размерах игрового поля, его составляющих
 # и массив по которому отрисовывается само поле,
 # а также проверку на победителя и его вывод на экран.
class Board():
    def __init__(self,  grid_size=10, block_size=50, gap=2, point=5, reverse= True):
        self.block_size = block_size
        # Зазор между блоками
        self.gap = gap
        # Размер игрового поля х*х
        self.grid_size = grid_size
        # Высота и ширина окна
        self.width = block_size * grid_size + gap * (grid_size + 1)
        self.height = block_size * grid_size + gap * (grid_size + 1) + block_size
        # массив поля
        self.grid = [[''] * grid_size for i in range(grid_size)]
        # Кол-во очков до победы
        self.point = point
        # Обратные ли крестики нолики или стандартные
        self.reverse = reverse

    # очистка игрового поля
    def cleaning_grid(self):
        self.grid = [[''] * self.grid_size for i in range(self.grid_size)]

    # Проверка на свободную ячейку поля
    def free_space(self, col, row):
        if self.grid[row][col] == '':
            return True
    # Проверка на поражение (победу)
    def check_loose(self, row, col):
        sign = self.grid[row][col]
        if self.check_col(sign, row, col) or \
           self.check_row(sign, row, col) or \
           self.check_diagonal(sign, row, col) or \
           self.check_reverse_diagonal(sign, row, col):
            return True

    def check_row(self,sign, row, col):
        counter = 0
        for cell in self.grid[row]:
            if cell == sign:
                counter += 1
            else:
                counter = 0
            if counter == self.point:
                return True

    def check_col(self,sign, row, col):
        counter = 0
        for row in self.grid:
            if row[col] == sign:
                counter += 1
            else:
                counter = 0
            if counter == self.point:
                return True

    def check_diagonal(self, sign, row_position, col_position):
        counter = 0
        bias = min(row_position, col_position)
        row_bias = bias
        for row in self.grid[row_position - row_bias:]:
            if col_position - bias > (self.grid_size - 1):
                break
            if row[col_position - bias] == sign:
                counter += 1
            else:
                counter = 0
            if counter == self.point:
                return True
            bias -= 1

    def check_reverse_diagonal(self, sign, row_position, col_position):
        counter = 0
        bias = max(col_position, row_position)
        while True:
            if (col_position + bias) <= (self.grid_size - 1) and (row_position - bias) >= 0:
                break
            bias -= 1
        row_bias = bias
        for row in self.grid[row_position - row_bias:]:
            if (col_position + bias) < 0:
                break
            if row[col_position + bias] == sign:
                counter += 1
            else:
                counter = 0
            if counter == self.point:
                return True
            bias -= 1

    # Заполняет игровое поля символом игрока - победителя
    def print_win(self, sign):
        self.grid = [[sign] * self.grid_size for i in range(self.grid_size)]

    def win(self, sign):
        if sign == "x":
            if self.reverse:
                self.print_win("o")
            else:
                self.print_win("x")
        else:
            if self.reverse:
                self.print_win("x")
            else:
                self.print_win("o")


class InputBox:

    def __init__(self, font, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = DARK_ORANGE
        self.text = text
        self.txt_surface = font.render(text, True, self.color)
        self.active = False
        self.font = font

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = ORANGE if self.active else DARK_ORANGE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    pass
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

# Окно настроек игры
def settings():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    font = pygame.font.Font(None, 32)
    pygame.display.set_caption("Settings")

    input_grid_size = InputBox(font,400, 100, 140, 32, '10')
    input_block_size = InputBox(font,400, 200, 140, 32, '50')
    input_gap = InputBox(font, 400, 300, 140, 32, '2')
    input_point = InputBox(font, 400, 0, 140, 32, '5')
    input_boxes = [input_grid_size, input_block_size, input_gap, input_point]

    b_start_pvp = Button((450), (480 - 100), 150, 60, "Player vs Player")
    b_start_pvpc = Button((250), (480 - 100), 150, 60, "Player vs PC")
    b_start_pcvpc = Button((50), (480 - 100), 150, 60, "PC vs PC")
    buttons = [b_start_pvp, b_start_pvpc, b_start_pcvpc]

    # цикл игры
    running = True
    while running:
        # ивент выхода
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
                #running = False

            for box in input_boxes:
                box.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if b_start_pvp.isOver(pygame.mouse.get_pos()):
                    game_mode = "player vs player"
                    running = False
                elif b_start_pvpc.isOver(pygame.mouse.get_pos()):
                    game_mode = "player vs pc"
                    running = False
                elif b_start_pcvpc.isOver(pygame.mouse.get_pos()):
                    game_mode = "pc vs pc"
                    running = False

            # подсветка кнопок
            elif event.type == pygame.MOUSEMOTION:
                for button in buttons:
                    if button.isOver(pygame.mouse.get_pos()):
                        button.active = True

        for box in input_boxes:
            box.update()
        # отрисовка
        screen.fill((30, 30, 30))
        for button in buttons:
            button.draw(screen, 20)
        for box in input_boxes:
            box.draw(screen)

        # Отрисовка текста (этот участок когда нужно переработать)
        text1 = "Размер сетки х*х:"
        font = pygame.font.SysFont('comicsans', 25)
        text1 = font.render(text1, True, ORANGE)
        screen.blit(text1, (170, 95))

        text2 = "Размер одного блока:"
        font = pygame.font.SysFont('comicsans', 25)
        text2 = font.render(text2, True, ORANGE)
        screen.blit(text2, (170 - 45, 95 + 100))

        text3 = "Растояние между блоками:"
        font = pygame.font.SysFont('comicsans', 25)
        text3 = font.render(text3, True, ORANGE)
        screen.blit(text3, (170 - 110, 95 + 200))

        text4 = "Очки до победы\поражения:"
        font = pygame.font.SysFont('comicsans', 25)
        text4 = font.render(text4, True, ORANGE)
        screen.blit(text4, (170 - 140, 0))

        pygame.display.flip()
    return game_mode, int(input_boxes[0].text), int(input_boxes[1].text), int(input_boxes[2].text), int(input_boxes[3].text)

def player_vs_player(board):
    # создаем игру и окно
    pygame.init()
    # для звука не успел реализовать
    #pygame.mixer.init()
    screen = pygame.display.set_mode((board.width, board.height))
    pygame.display.set_caption("X/O")
    b_restart = Button((board.width / 2 - board.block_size*2), (board.height - board.block_size), board.block_size*4, board.block_size, "restart")
    # очередь принимает значения 1 (первый игрок) 2 (второй игрок) и 0 (никто не ходит)
    queue = 1
    # Цикл игры
    running = True
    while running:

        for event in pygame.event.get():
            # проверить закрытие окна
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x_mouse, y_mouse = pygame.mouse.get_pos()

                # проверка на нахождение мышки в области игрового поля во время клика
                if y_mouse < (board.height - board.block_size):
                    # нахождение нужной ячейки
                    col = x_mouse // (board.block_size + board.gap)
                    row = y_mouse // (board.block_size + board.gap)
                    # проверка свобона ли ячейка
                    if board.free_space(col, row):
                        if queue == 1:
                            board.grid[row][col] = 'x'
                            queue = 2
                            # Проверка на победителя\проигравшего
                            if board.check_loose(row, col):
                                board.win(board.grid[row][col])
                                queue = 1
                        elif queue == 2:
                            board.grid[row][col] = 'o'
                            queue = 1
                            if board.check_loose(row, col):
                                board.win(board.grid[row][col])
                                queue = 1
                elif b_restart.isOver((x_mouse, y_mouse)):
                    board.cleaning_grid()

            elif event.type == pygame.MOUSEMOTION:
                if b_restart.isOver(pygame.mouse.get_pos()):
                    b_restart.active = True

        # отрисовываем ячейки в соответсвии с их содержимым
        for row in range(board.grid_size):
            for col in range(board.grid_size):
                if board.grid[row][col] == 'x':
                    color = ORANGE
                    text = 'x'
                elif board.grid[row][col] == "o":
                    color = PURPLE
                    text = 'o'
                else:
                    text = ''
                    color = GRAY
                x = col * board.block_size + (col + 1) * board.gap
                y = row * board.block_size + (row + 1) * board.gap
                pygame.draw.rect(screen, color, (x, y, board.block_size, board.block_size))
                font = pygame.font.SysFont('comicsans', board.block_size)
                text = font.render(text, True, BLACK)
                screen.blit(text,
                            (x + (board.block_size / 2 - text.get_width() / 2), y + (board.block_size / 3 - text.get_height() / 2)))

        b_restart.draw(screen, board.block_size)

        pygame.display.update()

    pygame.quit()

def player_vs_pc(board):
    pygame.init()
    # для звука не успел реализовать
    #pygame.mixer.init()
    screen = pygame.display.set_mode((board.width, board.height))
    pygame.display.set_caption("X/O")
    b_restart = Button((board.width / 2 - board.block_size * 2), (board.height - board.block_size),
                       board.block_size * 4, board.block_size, "restart")

    # второй игрок бот
    pc = Pc(board.grid_size)
    # очередь принимает значения 1 (первый игрок) 2 (второй игрок) и 0 (никто не ходит)
    queue = 1

    running = True
    while running:

        for event in pygame.event.get():
            # проверить закрытие окна
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x_mouse, y_mouse = pygame.mouse.get_pos()

                if y_mouse < (board.height - board.block_size):
                    col = x_mouse // (board.block_size + board.gap)
                    row = y_mouse // (board.block_size + board.gap)
                    if board.free_space(col, row):
                        if queue == 1:
                            board.grid[row][col] = 'x'
                            queue = 2
                            if board.check_loose(row, col):
                                board.win(board.grid[row][col])
                                queue = 0
                elif b_restart.isOver((x_mouse, y_mouse)):
                    board.cleaning_grid()
                    pc = Pc(board.grid_size)
                    queue = 1

            elif event.type == pygame.MOUSEMOTION:
                if b_restart.isOver(pygame.mouse.get_pos()):
                    b_restart.active = True

        #Ход PC
        if queue == 2:
            row, col = pc.move()
            if board.free_space(col, row):
                board.grid[row][col] = 'o'
                queue = 1
                if board.check_loose(row, col):
                    board.win(board.grid[row][col])
                    queue = 0

        # отрисовываем ячейки в соответсвии с их содержимым
        for row in range(board.grid_size):
            for col in range(board.grid_size):
                if board.grid[row][col] == 'x':
                    color = ORANGE
                    text = 'x'
                elif board.grid[row][col] == "o":
                    color = PURPLE
                    text = 'o'
                else:
                    text = ''
                    color = GRAY
                x = col * board.block_size + (col + 1) * board.gap
                y = row * board.block_size + (row + 1) * board.gap
                pygame.draw.rect(screen, color, (x, y, board.block_size, board.block_size))
                font = pygame.font.SysFont('comicsans', board.block_size)
                text = font.render(text, True, BLACK)
                screen.blit(text,
                            (x + (board.block_size / 2 - text.get_width() / 2),
                             y + (board.block_size / 3 - text.get_height() / 2)))

        b_restart.draw(screen, board.block_size)

        pygame.display.update()

    pygame.quit()

def pc_vs_ps(board):
    pygame.init()
    screen = pygame.display.set_mode((board.width, board.height))
    pygame.display.set_caption("X/O")
    b_restart = Button((board.width / 2 - board.block_size * 2), (board.height - board.block_size),
                       board.block_size * 4, board.block_size, "restart")

    # два бота для игры
    pc1 = Pc(board.grid_size)
    pc2 = Pc(board.grid_size)
    queue = 1

    running = True
    while running:

        for event in pygame.event.get():
            # проверить закрытие окна
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x_mouse, y_mouse = pygame.mouse.get_pos()

                if b_restart.isOver((x_mouse, y_mouse)):
                    board.cleaning_grid()
                    pc1 = Pc(board.grid_size)
                    pc2 = Pc(board.grid_size)
                    queue = 1

            elif event.type == pygame.MOUSEMOTION:
                if b_restart.isOver(pygame.mouse.get_pos()):
                    b_restart.active = True


        # Ход PC1
        if queue == 1:
            if pc1.can_move():
                row, col = pc1.move()
                if board.free_space(col, row):
                    board.grid[row][col] = 'x'
                    queue = 2
                    if board.check_loose(row, col):
                        board.win(board.grid[row][col])
                        queue = 0

        # Ход PC2
        if queue == 2:
            if pc2.can_move():
                row, col = pc2.move()
                if board.free_space(col, row):
                    board.grid[row][col] = 'o'
                    queue = 1
                    if board.check_loose(row, col):
                        board.win(board.grid[row][col])
                        queue = 0

        for row in range(board.grid_size):
            for col in range(board.grid_size):
                if board.grid[row][col] == 'x':
                    color = ORANGE
                    text = 'x'
                elif board.grid[row][col] == "o":
                    color = PURPLE
                    text = 'o'
                else:
                    text = ''
                    color = GRAY
                x = col * board.block_size + (col + 1) * board.gap
                y = row * board.block_size + (row + 1) * board.gap
                pygame.draw.rect(screen, color, (x, y, board.block_size, board.block_size))
                font = pygame.font.SysFont('comicsans', board.block_size)
                text = font.render(text, True, BLACK)
                screen.blit(text,
                            (x + (board.block_size / 2 - text.get_width() / 2),
                             y + (board.block_size / 3 - text.get_height() / 2)))

        b_restart.draw(screen, board.block_size)

        pygame.display.update()

    pygame.quit()


def main():
    # Получение настроек из settings
    game_mode, grid_size, block_size, gap, point = settings()

    board = Board(grid_size, block_size, gap, point, reverse=True)

    if game_mode == "player vs player":
        player_vs_player(board)
    elif game_mode == "player vs pc":
        player_vs_pc(board)
    elif game_mode == "pc vs pc":
        pc_vs_ps(board)

if __name__ == '__main__':
    main()
    pygame.quit()