import pygame

# app related definitions
BOARD_SIZE = 9
SIZE = 80  # size of each grid
NUMBERS = {1, 2, 3, 4, 5, 6, 7, 8, 9}  # set of all numbers in the sudoku board
WIDTH = 1200
HEIGHT = SIZE * BOARD_SIZE
TITLE = "Sudoku"
FPS = 60

# color related definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (71, 95, 119)
DARKBLUE = (53, 75, 94)
BACKGROUND = (222, 228, 231)
RED = (215, 75, 75)
GREY = (192, 192, 192)
DARKGREY = (110, 110, 110)

# pygame related definitions and setup
pygame.init()
pygame.display.set_caption(TITLE)
FONT = pygame.font.SysFont("arial.ttf", 30)  # default font
LARGEFONT = pygame.font.SysFont('arial.ttf', 60)
PENCILFONT = pygame.font.Font("pencil.ttf", 60)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
CLOCK = pygame.time.Clock()


def topleft(position, size):
    return position[0] - size[0] // 2, position[1] - size[1] // 2
