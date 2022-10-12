import pygame.draw

from globals import *
from labels import Text
from sudoku import deepCopy
from table import Table


class Board(Table):
    def __init__(self, sudoku, solving=False):
        super().__init__(BOARD_SIZE, BOARD_SIZE, border=True)
        self.sudoku = sudoku
        board = self.sudoku.getBoard()
        for j in range(BOARD_SIZE):
            for i in range(BOARD_SIZE):
                font, fixed = ARIALFONT, True
                if board[j][i] == 0:
                    font, fixed = PENCILFONT, False
                self.add_cell(Cell(board[j][i], font, fixed), i, j)

        self.i, self.j = 0, 0
        self.states = []
        self.initial = deepCopy(board)
        self.positions = []
        self.solving = solving
        self.state = SOLVING if solving else IDLE

        if self.solving:
            for j in range(BOARD_SIZE):
                for i in range(BOARD_SIZE):
                    self.findIllegalPositions(board[j][i], i, j)
                    if len(self.positions) > 0:
                        self.state = INCOMPLETE

    def drawBorder(self):
        for i in range(1, BOARD_SIZE):
            if i % 3 == 0:
                size = 5
            else:
                size = 1
            pygame.draw.line(SCREEN, BLACK, (0, i * SIZE), (BOARD_SIZE * SIZE, i * SIZE), size)
            pygame.draw.line(SCREEN, BLACK, (i * SIZE, 0), (i * SIZE, BOARD_SIZE * SIZE), size)

    def reset(self):
        self.i, self.j = 0, 0
        self.sudoku.parseBoard(self.sudoku.temp)
        self.states.clear()
        self.positions.clear()
        board = self.sudoku.getBoard()
        for j in range(BOARD_SIZE):
            for i in range(BOARD_SIZE):
                self.cells[j][i][0].change_text(board[j][i])

    def undo(self):
        if len(self.states) > 0:
            self.states.pop()
            if len(self.states) != 0:
                self.sudoku.parseBoard(self.states[-1][0])
                self.i, self.j = self.states[-1][1]
            else:
                self.sudoku.parseBoard(self.initial)
                self.i, self.j = 0, 0

            board = self.sudoku.getBoard()
            for j in range(BOARD_SIZE):
                for i in range(BOARD_SIZE):
                    self.cells[j][i][0].change_text(board[j][i])

            self.positions.clear()

    def findIllegalPositions(self, num, i, j):
        if num == 0:
            self.positions.clear()
            return

        board = self.sudoku.getBoard()
        row = self.sudoku.getRow(j)
        column = self.sudoku.getColumn(i)
        grid = self.sudoku.getGrid(i, j)

        self.positions.clear()

        if num in grid:
            temp_i = i // 3
            temp_j = j // 3
            for y in range(temp_j * 3, temp_j * 3 + 3):
                for x in range(temp_i * 3, temp_i * 3 + 3):
                    if num == board[y][x] and (i, j) != (x, y) and (x, y) not in self.positions:
                        self.positions.append((x, y))

        if num in row:
            for x in range(BOARD_SIZE):
                if num == board[j][x] and i != x and (x, j) not in self.positions:
                    self.positions.append((x, j))

        if num in column:
            for y in range(BOARD_SIZE):
                if num == board[y][i] and j != y and (i, y) not in self.positions:
                    self.positions.append((i, y))

    def update(self):
        if self.visible:
            if not self.solving:
                if pygame.mouse.get_pressed()[0]:  # the left mouse button is pressed
                    mouse_pos = pygame.mouse.get_pos()
                    i, j = mouse_pos[0] // SIZE, mouse_pos[1] // SIZE
                    if not (self.i == i and self.j == j) and 0 <= i < BOARD_SIZE and 0 <= j < BOARD_SIZE:
                        self.i = i
                        self.j = j
                        self.findIllegalPositions(self.sudoku.getBoard()[self.j][self.i], self.i, self.j)

                key_event = pygame.key.get_pressed()
                num = -1
                if key_event[pygame.K_1]:
                    num = 1
                elif key_event[pygame.K_2]:
                    num = 2
                elif key_event[pygame.K_3]:
                    num = 3
                elif key_event[pygame.K_4]:
                    num = 4
                elif key_event[pygame.K_5]:
                    num = 5
                elif key_event[pygame.K_6]:
                    num = 6
                elif key_event[pygame.K_7]:
                    num = 7
                elif key_event[pygame.K_8]:
                    num = 8
                elif key_event[pygame.K_9]:
                    num = 9
                elif key_event[pygame.K_0] or key_event[pygame.K_BACKSPACE]:
                    num = 0

                if num != -1 and num not in self.sudoku.markup(self.i, self.j) \
                        and not self.cells[self.j][self.i][0].fixed:
                    self.findIllegalPositions(num, self.i, self.j)

                if num != -1 and not self.cells[self.j][self.i][0].fixed:
                    self.cells[self.j][self.i][0].change_text(num)
                    if num != self.sudoku.getBoard()[self.j][self.i]:
                        self.states.append((deepCopy(self.sudoku.getBoard()), (self.i, self.j)))
                    self.sudoku.parseCell(self.i, self.j, num)

            else:
                # key_event = pygame.key.get_pressed()
                # if key_event[pygame.K_UP]:
                # elif key_event[pygame.K_DOWN]:

                board = self.sudoku.getBoard()
                for j in range(BOARD_SIZE):
                    for i in range(BOARD_SIZE):
                        if board[j][i] != int(self.cells[j][i][0].text):
                            self.cells[j][i][0].change_text(board[j][i])

                complete = self.sudoku.isComplete()
                if not complete and self.sudoku.getSolving():
                    self.state = SOLVING
                elif not complete and not self.sudoku.getSolving():
                    self.state = INCOMPLETE
                elif complete:
                    self.state = COMPLETE

    def draw(self):
        if self.visible:
            if not self.solving:
                num = self.sudoku.getBoard()[self.j][self.i]
                for j in range(BOARD_SIZE):
                    for i in range(BOARD_SIZE):
                        color = WHITE
                        if num != 0 and self.sudoku.getBoard()[j][i] == num:
                            color = LIGHTGREY
                        if (i, j) == (self.i, self.j):
                            color = RED
                        pygame.draw.rect(SCREEN, color, (i * SIZE, j * SIZE, SIZE, SIZE))

                for (i, j) in self.positions:
                    pygame.draw.rect(SCREEN, RED, (i * SIZE, j * SIZE, SIZE, SIZE), 7)
            else:
                for j in range(BOARD_SIZE):
                    for i in range(BOARD_SIZE):
                        pygame.draw.rect(SCREEN, WHITE, (i * SIZE, j * SIZE, SIZE, SIZE))

            for k in range(self.rows):
                for j in range(self.columns):
                    for i in range(len(self.cells[k][j])):
                        self.cells[k][j][i].draw()

            if self.border:
                self.drawBorder()


class Cell(Text):
    def __init__(self, text, font, fixed):
        super().__init__(text, font=font, color=BLACK, width=SIZE, height=SIZE)
        self.fixed = fixed
        if text == 0:
            self.visible = False
        else:
            self.visible = True

    def change_text(self, text):
        self.text = str(text)
        self.inflate(self.pos, self.size)
        if text == 0:
            self.visible = False
        else:
            self.visible = True
