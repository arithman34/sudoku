from functools import partial

from button import Button
from container import Container
from labels import Text, Icon
from sudoku import Sudoku, deepCopy
from globals import *
from table import Table


class HomeActivity:
    def __init__(self):
        self.containers = []

        container = Container((0, 0), (WIDTH, HEIGHT))
        container.add(Button("Mode", ModeActivity))
        container.add(Button("Solve", partial(GameActivity, "EMPTY")))
        container.add(Button("Instructions", InstructionActivity))
        container.add(Button("Quit", destroy))
        container.inflate()
        self.containers.append(container)

        self.run()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    destroy()

                for container in self.containers:
                    container.update()

            SCREEN.fill(BACKGROUND)

            for container in self.containers:
                container.draw()
            pygame.display.flip()
            CLOCK.tick(FPS)
        destroy()


class ModeActivity:
    def __init__(self):
        self.containers = []

        container = Container((0, 0), (WIDTH, HEIGHT))
        container.add(Button("Easy", partial(GameActivity, "EASY")))
        container.add(Button("Normal", partial(GameActivity, "NORMAL")))
        container.add(Button("Hard", partial(GameActivity, "HARD")))
        container.add(Button("Return", HomeActivity))
        container.inflate()
        self.containers.append(container)

        self.run()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    destroy()
                for container in self.containers:
                    container.update()

            SCREEN.fill(BACKGROUND)

            for container in self.containers:
                container.draw()
            pygame.display.flip()
            CLOCK.tick(FPS)
        destroy()


class InstructionActivity:
    def __init__(self):
        self.containers = []

        container = Container((0, 0), (WIDTH // 2, 150), 0, (0, 255, 0))
        container.add(Text("Welcome to Sudoku", font=LARGEFONT, margin=50))

        container.inflate()
        self.containers.append(container)

        container = Container((0, 150), (WIDTH // 2, HEIGHT - 150), 0, (255, 0, 255))
        container.add(Text("Sudoku is a game where all rows, columns and 3x3 grids must contain " +
                           "the numbers 1-9 at least once and only once. This implementation can also solve any " +
                           "sudoku board provided, of course, it is legal. You will have several modes to choose " +
                           "from ranging from easy to evil. Good luck!", margin=100))
        container.inflate()
        self.containers.append(container)

        container = Container((0, HEIGHT - 150), (WIDTH, HEIGHT), color=(255, 255, 0))
        container.add(Button("Return", HomeActivity))
        container.inflate()

        self.containers.append(container)

        container = Container((WIDTH // 2, 0), (WIDTH, HEIGHT - 150), color=(0, 255, 255))
        table = Table(2, 7, True)

        table.add_cell(Text("Key", alignment="center"), 0, 0)
        table.add_cell(Icon(WHITE, width=SIZE, height=SIZE), 0, 1)
        table.add_cell(Icon(RED, width=SIZE, height=SIZE), 0, 2)
        table.add_cell(Icon(GREY, width=SIZE, height=SIZE), 0, 3)
        table.add_cell(Icon(RED, width=SIZE, height=SIZE), 0, 4)
        table.add_cell(Icon(GREY, width=SIZE - 20, height=SIZE - 20), 0, 4)
        table.add_cell(Icon(WHITE, width=SIZE, height=SIZE), 0, 5)
        table.add_cell(Text("6", font=LARGEFONT, color=BLACK, width=SIZE, height=SIZE), 0, 5)
        table.add_cell(Icon(WHITE, width=SIZE, height=SIZE), 0, 6)
        table.add_cell(Text("6", font=PENCILFONT, color=BLACK, width=SIZE, height=SIZE), 0, 6)

        table.add_cell(Text("Description", alignment="center"), 1, 0)
        table.add_cell(Text("This cell is empty", alignment="midleft"), 1, 1)
        table.add_cell(Text("This cell is currently selected", alignment="midleft"), 1, 2)
        table.add_cell(Text("Cells with same value as the selected cell but not invalid", alignment="midleft"), 1, 3)
        table.add_cell(Text("Cells that make selected cell invalid", alignment="midleft"), 1, 4)
        table.add_cell(Text("This cell cannot change", alignment="midleft"), 1, 5)
        table.add_cell(Text("This cell can change", alignment="midleft"), 1, 6)

        container.add(table)
        container.inflate()

        self.containers.append(container)
        self.run()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    destroy()

                for container in self.containers:
                    container.update()

            SCREEN.fill(BACKGROUND)
            for container in self.containers:
                container.draw()
            pygame.display.flip()
            CLOCK.tick(FPS)
        destroy()


class GameActivity:
    def __init__(self, mode):
        self.mode = mode
        self.sudoku = Sudoku()
        self.sudoku.create(mode)
        self.i = 0
        self.j = 0
        board = self.sudoku.getBoard()
        self.uneditable = populateDictionary(board)
        self.states = []
        self.initial = deepCopy(board)
        self.positions = []

        self.containers = []

        container = Container((SIZE * BOARD_SIZE, 0), (WIDTH, HEIGHT))
        container.add(Button("New Game", HomeActivity))
        container.add(Button("Reset", self.reload))
        container.add(Button("Solve", self.solve))

        container.add(Button("Undo", self.previousBoardState))
        container.inflate()

        self.containers.append(container)

        self.run()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    destroy()

                if pygame.mouse.get_pressed()[0]:  # the left mouse button is pressed
                    mouse_pos = pygame.mouse.get_pos()
                    i, j = mouse_pos[0] // SIZE, mouse_pos[1] // SIZE
                    if 0 <= i < BOARD_SIZE and 0 <= j < BOARD_SIZE:
                        self.i = i
                        self.j = j
                        self.positions.clear()
                        self.positions = self.findIllegalPositions(self.sudoku.getBoard()[self.j][self.i])

                if event.type == pygame.KEYDOWN:
                    num = -1
                    if event.key == pygame.K_1:
                        num = 1
                    elif event.key == pygame.K_2:
                        num = 2
                    elif event.key == pygame.K_3:
                        num = 3
                    elif event.key == pygame.K_4:
                        num = 4
                    elif event.key == pygame.K_5:
                        num = 5
                    elif event.key == pygame.K_6:
                        num = 6
                    elif event.key == pygame.K_7:
                        num = 7
                    elif event.key == pygame.K_8:
                        num = 8
                    elif event.key == pygame.K_9:
                        num = 9
                    elif event.key == pygame.K_0 or event.key == pygame.K_BACKSPACE:
                        num = 0

                    self.positions.clear()

                    if num not in (-1, 0) and num not in self.sudoku.markup(self.i, self.j) \
                            and (self.i, self.j) not in self.uneditable:
                        self.positions = self.findIllegalPositions(num)

                    if num != -1 and (self.i, self.j) not in self.uneditable:
                        self.sudoku.parseCell(self.i, self.j, num)
                        self.states.append((deepCopy(self.sudoku.getBoard()), (self.i, self.j)))

                for container in self.containers:
                    container.update()

            SCREEN.fill(BACKGROUND)
            for container in self.containers:
                container.draw()
            self.draw_cells()
            draw_grid()
            SCREEN.blit(get_fps(), (WIDTH - 94, 20))

            pygame.display.flip()
            CLOCK.tick(FPS)

    def findIllegalPositions(self, num):
        if num == 0:
            return []

        board = self.sudoku.getBoard()
        row = self.sudoku.getRow(self.j)
        column = self.sudoku.getColumn(self.i)
        grid = self.sudoku.getGrid(self.i, self.j)

        positions = []

        if num in grid:
            temp_i = self.i // 3
            temp_j = self.j // 3
            for j in range(temp_j * 3, temp_j * 3 + 3):
                for i in range(temp_i * 3, temp_i * 3 + 3):
                    if num == board[j][i] and (self.i, self.j) != (i, j):
                        positions.append((i, j))

        if num in row:
            for i in range(BOARD_SIZE):
                if num == board[self.j][i] and self.i != i:
                    positions.append((i, self.j))

        if num in column:
            for j in range(BOARD_SIZE):
                if num == board[j][self.i] and self.j != j:
                    positions.append((self.i, j))

        return positions

    def draw_cells(self):
        board = self.sudoku.getBoard()
        num = board[self.j][self.i]
        for j in range(BOARD_SIZE):
            for i in range(BOARD_SIZE):
                color = WHITE
                if num != 0 and board[j][i] == num:
                    color = GREY
                if (i, j) == (self.i, self.j):
                    color = RED
                pygame.draw.rect(SCREEN, color, (i * SIZE, j * SIZE, SIZE, SIZE))
                if board[j][i] == 0:
                    continue
                if (i, j) in self.uneditable.keys():
                    font = LARGEFONT
                else:
                    font = PENCILFONT
                text = font.render(str(board[j][i]), True, BLACK)
                width, height = text.get_width(), text.get_height()
                SCREEN.blit(text, (i * SIZE + SIZE / 2 - width / 2, j * SIZE + SIZE / 2 - height / 2))

        for (i, j) in self.positions:
            pygame.draw.rect(SCREEN, RED, (i * SIZE, j * SIZE, SIZE, SIZE), 7)

    def reload(self):
        self.i = 0
        self.j = 0
        self.sudoku.parseBoard(deepCopy(self.sudoku.temp))
        self.states = []
        self.positions.clear()

    def solve(self):
        SolvingActivity(deepCopy(self.sudoku.getBoard()))

    def previousBoardState(self):
        if len(self.states) > 0:
            self.states.pop()
            if len(self.states) != 0:
                self.sudoku.parseBoard(deepCopy(self.states[-1][0]))
                self.i, self.j = self.states[-1][1]
            else:
                self.sudoku.parseBoard(deepCopy(self.initial))
                self.i, self.j = 0, 0
            self.positions.clear()


class SolvingActivity:
    def __init__(self, board):
        self.containers = []

        container = Container((SIZE * BOARD_SIZE, 0), (WIDTH, HEIGHT))
        container.add(Button("New Game", HomeActivity))
        container.add(Button("Solve", partial(GameActivity, "EMPTY")))
        container.inflate()

        self.containers.append(container)

        self.solving = False
        self.sudoku = Sudoku(board)
        self.uneditable = populateDictionary(board)
        self.board = board
        self.begin_solver()
        self.run()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    destroy()

                for container in self.containers:
                    container.update()

            SCREEN.fill(BACKGROUND)
            for container in self.containers:
                container.draw()
            self.draw_cells()
            draw_grid()
            SCREEN.blit(get_fps(), (WIDTH - 94, 20))

            pygame.display.flip()
            CLOCK.tick(FPS)

    def draw_cells(self):
        for j in range(BOARD_SIZE):
            for i in range(BOARD_SIZE):
                pygame.draw.rect(SCREEN, WHITE, (i * SIZE, j * SIZE, SIZE, SIZE))
                if self.board[j][i] == 0:
                    continue

                if (i, j) in self.uneditable.keys():
                    font = LARGEFONT
                else:
                    font = PENCILFONT

                text = font.render(str(self.board[j][i]), True, BLACK)
                width, height = text.get_width(), text.get_height()
                SCREEN.blit(text, (i * SIZE + SIZE / 2 - width / 2, j * SIZE + SIZE / 2 - height / 2))

    def begin_solver(self):
        self.solving = True
        self.sudoku.backtrackingSolution()

    def update(self):
        for j in range(BOARD_SIZE):
            for i in range(BOARD_SIZE):
                if self.board[j][i] != self.sudoku.getBoard()[j][i]:
                    self.board[j][i] = self.sudoku.getBoard()[j][i]


def draw_grid():
    for i in range(1, BOARD_SIZE):
        if i % 3 == 0:
            size = 5
        else:
            size = 1
        pygame.draw.line(SCREEN, BLACK, (0, i * SIZE), (BOARD_SIZE * SIZE, i * SIZE), size)
        pygame.draw.line(SCREEN, BLACK, (i * SIZE, 0), (i * SIZE, BOARD_SIZE * SIZE), size)


def destroy():
    pygame.quit()
    quit()


def get_fps():
    return FONT.render("FPS: " + str(int(CLOCK.get_fps())), True, BLACK)


def populateDictionary(board):
    dictionary = {}
    for j in range(BOARD_SIZE):
        for i in range(BOARD_SIZE):
            if board[j][i] != 0:
                dictionary[(i, j)] = board[j][i]
    return dictionary
