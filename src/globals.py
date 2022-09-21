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
GREY = (133, 133, 133)
DARKBLUE = (53, 75, 94)
BACKGROUNDCOLOR = WHITE
RED = (215, 75, 75)
LIGHTGREY = (161, 161, 161)
DARKGREY = (89, 89, 89)

# pygame related definitions and setup
pygame.init()
pygame.display.set_caption(TITLE)
LARGEFONT = pygame.font.Font("res\\main.ttf", 40)
PENCILFONT = pygame.font.Font("res\\pencil.ttf", 60)
ARIALFONT = pygame.font.SysFont("arial.ttf", 60)
FONT = pygame.font.Font("res\\main.ttf", 15)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

# loading image resources
SELECTED_TEMPLATE = pygame.image.load("res\\images\\selected.png").convert()
DEFAULT_TEMPLATE = pygame.image.load("res\\images\\default.png").convert()
BACKGROUND = pygame.transform.scale(pygame.image.load("res\\images\\background.png"), (WIDTH, HEIGHT)).convert()


def getTopleft(position, size):
    return position[0] - size[0] / 2, position[1] - size[1] / 2
