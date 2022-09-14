import time
import threading
import random
from globals import BOARD_SIZE, NUMBERS


class Grader:
    def __init__(self, sudoku, difficulty):
        self.sudoku = sudoku
        self.__difficulty = difficulty
        self.total = 0
        self.empty_cells = 0
        # self.__markup()

    def __markup(self):
        self.total = 0
        self.empty_cells = 0
        markup = [[[] for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        for j in range(BOARD_SIZE):
            for i in range(BOARD_SIZE):
                if self.sudoku.board[j][i] == 0:
                    markup[j][i] = list(self.sudoku.markup(i, j))
                    self.total += len(markup[j][i])
                    self.empty_cells += 1

    def update(self):
        self.__markup()

    def check(self):
        # print(self.total)
        if self.total < 90:
            return "NOT GOOD ENOUGH"
        elif 90 <= self.total < 130:
            return "EASY"
        elif 130 <= self.total < 170:
            return "NORMAL"
        elif self.total > 170:
            return "HARD"


class Sudoku:
    def __init__(self, board=None):
        self.board = board
        self.temp = board
        self.__thread = None
        self.__solving = False

    def initBoard(self):
        self.board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]

    def getRow(self, j):
        return set(self.board[j])

    def getColumn(self, i):
        return set([self.board[x][i] for x in range(BOARD_SIZE)])

    def getGrid(self, i, j):
        i = i // 3
        j = j // 3
        return set([self.board[y][x] for y in range(j * 3, j * 3 + 3) for x in range(i * 3, i * 3 + 3)])

    def markup(self, i, j):
        row = NUMBERS - self.getRow(j)
        column = NUMBERS - self.getColumn(i)
        box = NUMBERS - self.getGrid(i, j)
        return row.intersection(column, box)

    def emptyPosition(self, pos):
        for j in range(BOARD_SIZE):
            for i in range(BOARD_SIZE):
                if self.board[j][i] == 0:
                    pos[0] = i
                    pos[1] = j
                    return True
        return False

    def answer(self):
        self.__solving = True
        self.temp = deepCopy(self.board)
        while self.__solving:
            try:
                self.__solve()
                self.temp = None
            except RuntimeError:
                self.board = deepCopy(self.temp)
            self.__solving = False

    def __solve(self):
        # a thread has been initiated but is about to be killed. Throwing an error is the best way to leave a thread
        # that is backtracking

        if not self.__solving and self.__thread is not None:
            raise RuntimeError()

        current = [0, 0]

        if not self.emptyPosition(current):
            return True

        i = current[0]
        j = current[1]

        numbers = list(self.markup(i, j))
        random.shuffle(numbers)  # this line ensures that each board generated is generally unique

        for num in numbers:
            self.board[j][i] = num

            if self.__solving:
                time.sleep(0.01)

            if self.__solve():
                return True

            self.board[j][i] = 0

            if self.__solving:
                time.sleep(0.01)
        return False

    def solution(self):
        self.initBoard()

        if not self.__solve():
            print("There are no solutions, creating a new table")
            self.solution()

    def create(self, flag):
        if flag == "EMPTY":
            self.initBoard()
        else:
            self.solution()
            for _ in range(10):
                i, j = random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1)
                while self.board[j][i] == 0:
                    i, j = random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1)
                self.board[j][i] = 0
            grader = Grader(self, None)
            grader.update()
            while grader.check() != flag:
                i, j = random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1)
                while self.board[j][i] == 0:
                    i, j = random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1)
                self.board[j][i] = 0
                grader.update()

        self.temp = deepCopy(self.board)

    def backtrackingSolution(self):
        # grader = Grader(self, None)
        # grader.update()
        # print(grader.check())
        self.__thread = threading.Thread(target=self.answer, args=())
        self.__thread.start()


def deepCopy(array):
    temp = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    for j in range(BOARD_SIZE):
        for i in range(BOARD_SIZE):
            temp[j][i] = array[j][i]
    return temp
