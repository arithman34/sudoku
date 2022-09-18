import pygame

from globals import BLUE, WHITE, RED, FONT, SCREEN, DARKBLUE, topleft


class Button:
    def __init__(self, text, onclick, alignment="midleft"):
        # Core attributes
        self.pressed = False
        self.elevation = 10
        self.dynamic_elevation = self.elevation
        self.original_y_pos = None

        # top rectangle
        self.top_rect = None
        self.top_color = BLUE

        # bottom rectangle
        self.bottom_rect = None
        self.bottom_color = DARKBLUE

        # text
        self.text = FONT.render(text, True, WHITE)
        self.width, self.height = self.text.get_width(), self.text.get_height()
        self.alignment = alignment
        self.padding = 10  # padding for x and y if too close to center
        self.text_rect = None

        self.size = None
        self.pos = None
        self.onclick = onclick

    def inflate(self, pos, size):
        self.size = size
        self.pos = pos

        self.original_y_pos = self.pos[1]

        self.top_rect = pygame.Rect(topleft(self.pos, self.size), self.size)
        self.bottom_rect = pygame.Rect(topleft(self.pos, self.size), self.size)

        if self.alignment == "center":
            self.text_rect = self.text.get_rect(center=self.top_rect.center)
        elif self.alignment == "midleft":
            self.text_rect = self.text.get_rect(midleft=self.top_rect.midleft)
        # elif self.alignment == "midright":
        #     self.text_rect = self.text.get_rect(midright=self.top_rect.midright)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = RED
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed:
                    self.onclick()
                    self.pressed = False
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = BLUE
            self.pressed = False

    def draw(self):
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        if self.alignment == "center":
            self.text_rect.center = self.top_rect.center
        elif self.alignment == "midleft":
            self.text_rect.midleft = self.top_rect.midleft
            self.text_rect.x += self.padding
        elif self.alignment == "midright":
            self.text_rect.midright = self.top_rect.midright
            self.text_rect.x -= self.padding

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(SCREEN, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(SCREEN, self.top_color, self.top_rect, border_radius=12)
        SCREEN.blit(self.text, self.text_rect)
