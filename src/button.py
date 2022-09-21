from globals import *


class Button:
    def __init__(self, text, onclick, alignment="center"):
        # Core attributes
        # super().__init__()
        self.pressed = False
        self.hovering = False

        # top rectangle
        self.rect = None
        self.image = None
        self.top_color = GREY

        # bottom rectangle
        self.bottom_rect = None
        self.bottom_color = BLACK

        # text
        self.text = FONT.render(text, True, WHITE)
        self.width, self.height = self.text.get_width(), self.text.get_height()
        self.alignment = alignment
        self.padding = 10  # padding for x and y if too close to center
        self.text_rect = self.text.get_rect()

        self.size = None
        self.pos = None
        self.onclick = onclick

        self.selectedImg = None
        self.defaultImg = None

        self.image = self.defaultImg

    def inflate(self, pos, size):
        self.size = size
        self.pos = pos

        self.selectedImg = pygame.transform.scale(SELECTED_TEMPLATE, self.size)
        self.defaultImg = pygame.transform.scale(DEFAULT_TEMPLATE, self.size)

        self.image = self.defaultImg

        self.rect = self.defaultImg.get_rect(center=self.pos)

        if self.alignment == "center":
            self.text_rect.center = self.rect.center

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.image = self.selectedImg
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed:
                    self.onclick()
                    self.pressed = False
        else:
            self.top_color = GREY
            self.pressed = False
            self.image = self.defaultImg

    def draw(self):
        SCREEN.blit(self.image, self.rect)
        SCREEN.blit(self.text, self.text_rect)
