from functools import partial

from button import *
from container import Container
from labels import Text, Icon
from board import Board
from sudoku import Sudoku, deepCopy
from globals import *
from table import Table


class Activity:
    def __init__(self):
        self.containers = []

    def run(self):
        running = True
        while running:
            SCREEN.blit(BACKGROUND, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            for container in self.containers:
                container.update()

            for container in self.containers:
                container.draw()
            pygame.display.flip()
            CLOCK.tick(FPS)
        destroy()

    def getContainerById(self, id):
        for container in self.containers:
            if container.id == id:
                return container
        return None


class WelcomeActivity(Activity):
    def __init__(self):
        super().__init__()
        self.containers = []

        container = Container(0, (WIDTH / 2, 75), (WIDTH, 150), 0, RED)
        container.add(Text("Welcome to Sudoku", font=LARGEFONT, margin=50))
        container.inflate()
        self.containers.append(container)

        container = Container(1, (WIDTH / 2, 360), (WIDTH, 420), 0, GREY)
        container.add(Text("Sudoku is a game where all rows, columns and 3x3 grids must contain " +
                           "the numbers 1-9 at least once and only once. This implementation can also solve any " +
                           "sudoku board provided, of course, it is legal. You will have several modes to choose " +
                           "from ranging from easy to hard. Good luck!", margin=250))
        container.inflate()
        self.containers.append(container)

        container = Container(2, (WIDTH / 2, 645), (WIDTH, 150), 0, (255, 255, 0))
        container.add(Text("Press a key to play"))
        container.inflate()
        self.containers.append(container)

        self.blink_event = pygame.USEREVENT
        pygame.time.set_timer(self.blink_event, 1000)

        self.run()

    def run(self):
        running = True
        while running:
            SCREEN.blit(BACKGROUND, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    destroy()

                if event.type == pygame.KEYDOWN:
                    running = False

                if event.type == self.blink_event:
                    self.containers[2].setVisibility()

            for container in self.containers:
                container.update()

            for container in self.containers:
                container.draw()

            pygame.display.flip()
            CLOCK.tick(FPS)
        HomeActivity()


class HomeActivity(Activity):
    def __init__(self):
        super().__init__()
        self.containers = []

        container = Container(0, (WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
        container.add(Button("Mode", ModeActivity))
        container.add(Button("Solve", partial(GameActivity, "EMPTY")))
        container.add(Button("Instructions", InstructionActivity))
        container.add(Button("Quit", destroy))
        container.inflate()
        self.containers.append(container)

        self.run()


class ModeActivity(Activity):
    def __init__(self):
        super().__init__()
        self.containers = []

        container = Container(0, (WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
        container.add(Button("Easy", partial(GameActivity, "EASY")))
        container.add(Button("Normal", partial(GameActivity, "NORMAL")))
        container.add(Button("Hard", partial(GameActivity, "HARD")))
        container.add(Button("Return", HomeActivity))
        container.inflate()
        self.containers.append(container)

        self.run()


class InstructionActivity(Activity):
    def __init__(self):
        super().__init__()
        self.containers = []

        container = Container(0, (WIDTH / 2, 285), (WIDTH, HEIGHT - 150))
        table = Table(2, 7)

        table.add_cell(Text("Key", alignment="center"), 0, 0)
        table.add_cell(Icon(WHITE, width=SIZE, height=SIZE), 0, 1)
        table.add_cell(Icon(RED, width=SIZE, height=SIZE), 0, 2)
        table.add_cell(Icon(LIGHTGREY, width=SIZE, height=SIZE), 0, 3)
        table.add_cell(Icon(RED, width=SIZE, height=SIZE), 0, 4)
        table.add_cell(Icon(LIGHTGREY, width=SIZE - 20, height=SIZE - 20), 0, 4)
        table.add_cell(Icon(WHITE, width=SIZE, height=SIZE), 0, 5)
        table.add_cell(Text("6", font=ARIALFONT, color=BLACK, width=SIZE, height=SIZE), 0, 5)
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

        container = Container(1, (WIDTH / 2, 645), (WIDTH, 150), 0)
        container.add(Button("Return", HomeActivity))
        container.inflate()

        self.containers.append(container)

        self.run()


class GameActivity(Activity):
    def __init__(self, mode):
        super().__init__()
        self.containers = []

        self.sudoku = Sudoku()
        self.sudoku.create(mode)

        container = Container(0, (HEIGHT / 2, HEIGHT / 2), (HEIGHT, HEIGHT))
        container.add(Board(self.sudoku))
        container.inflate()
        self.containers.append(container)

        container = Container(1, (960, HEIGHT / 2), (480, HEIGHT))
        container.add(Button("New Game", HomeActivity))
        container.add(Button("Reset", self.getContainerById(0).sprites[0].reset))
        container.add(Button("Solve", self.solve))
        container.add(Button("Undo", self.getContainerById(0).sprites[0].undo))
        container.inflate()
        self.containers.append(container)

        self.run()

    def solve(self):
        SolvingActivity(deepCopy(self.getContainerById(0).sprites[0].sudoku.getBoard()))


class SolvingActivity(Activity):
    def __init__(self, board):
        super().__init__()
        self.containers = []
        self.sudoku = Sudoku(board)

        container = Container(0, (HEIGHT / 2, HEIGHT / 2), (HEIGHT, HEIGHT))
        container.add(Board(self.sudoku, True))
        container.inflate()
        self.containers.append(container)

        container = Container(1, (960, HEIGHT / 2), (480, HEIGHT))
        container.add(Button("New Game", ModeActivity))
        container.add(Button("Solve", partial(GameActivity, "EMPTY")))
        container.inflate()
        self.containers.append(container)

        container = Container(2, (HEIGHT / 2, HEIGHT / 2), (HEIGHT, HEIGHT))
        container.add(Text("", font=LARGEFONT))
        container.setVisibility(False)
        container.inflate()
        self.containers.append(container)

        self.state = self.getContainerById(0).sprites[0].state
        if self.state == INCOMPLETE:
            self.getContainerById(0).setVisibility(False)
            self.getContainerById(2).sprites[0].change_text("No solution")
            self.getContainerById(2).setVisibility(True)

        self.board = board
        if self.getContainerById(0).sprites[0].state == SOLVING:
            self.sudoku.backtrackingSolution()
        self.run()

    def run(self):
        running = True
        while running:
            state = self.getContainerById(0).sprites[0].state
            if self.state != state:
                if state == COMPLETE:
                    self.getContainerById(0).setVisibility(False)
                    self.getContainerById(2).sprites[0].change_text("Found a solution")
                    self.getContainerById(2).setVisibility(True)
                elif state == INCOMPLETE:
                    self.getContainerById(0).setVisibility(False)
                    self.getContainerById(2).sprites[0].change_text("No solution")
                    self.getContainerById(2).setVisibility(True)
                self.state = state

            SCREEN.blit(BACKGROUND, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            for container in self.containers:
                container.update()

            for container in self.containers:
                container.draw()
            pygame.display.flip()
            CLOCK.tick(FPS)
        destroy()


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


# undo not working with 3 sixs
# slow down the solution through user control
