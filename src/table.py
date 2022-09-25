import pygame

from globals import BLACK, SCREEN


class Table:
    def __init__(self, columns, rows, border=False):
        self.size = []
        self.pos = None
        self.border = border
        self.columns = columns
        self.rows = rows
        self.cells = [[[] for _ in range(self.columns)] for _ in range(self.rows)]

        self.width = [0 for _ in range(self.columns)]
        self.height = [0 for _ in range(self.rows)]
        self.visible = True

    def add_cell(self, cell, i, j):
        self.cells[j][i].append(cell)

        if cell.width > self.width[i]:
            self.width[i] = cell.width

        if cell.height > self.height[j]:
            self.height[j] = cell.height

    def inflate(self, pos, size):
        self.pos = pos
        self.size = size
        self.width = self.fillSize(self.width, 0)
        self.height = self.fillSize(self.height, 1)

        y = pos[1]
        for k in range(self.rows):
            x = pos[0]
            for j in range(self.columns):
                for i in range(len(self.cells[k][j])):
                    cell = self.cells[k][j][i]
                    cell.inflate((x + self.width[j] // 2, y + self.height[k] // 2), (self.width[j], self.height[k]))
                    # heights.append(self.height[j])
                x += self.width[j]
            y += self.height[k]

    def fillSize(self, array, index):
        total = sum(array)
        remainder = self.size[index] - total
        num_of_zeros = len([0 for num in array if num == 0])
        for i in range(len(array)):
            if array[i] == 0:
                array[i] = remainder / num_of_zeros
        return array

    def update(self):
        pass

    def drawBorder(self):
        size = 2
        x = self.pos[0]
        for i in range(len(self.width)):
            pygame.draw.line(SCREEN, BLACK, (x, self.pos[1]), (x, self.pos[1] + self.size[1]), size)
            x += self.width[i]
        pygame.draw.line(SCREEN, BLACK, (x, self.pos[1]), (x, self.pos[1] + self.size[1]), size)

        y = self.pos[1]
        for i in range(len(self.height)):
            pygame.draw.line(SCREEN, BLACK, (self.pos[0], y), (self.pos[0] + self.size[0], y), size)
            y += self.height[i]
        pygame.draw.line(SCREEN, BLACK, (self.pos[0], y), (self.pos[0] + self.size[0], y), size)

    def draw(self):
        if self.visible:
            for k in range(self.rows):
                for j in range(self.columns):
                    for i in range(len(self.cells[k][j])):
                        self.cells[k][j][i].draw()
            if self.border:
                self.drawBorder()
