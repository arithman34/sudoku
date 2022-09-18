import pygame

from globals import FONT, BLACK, SCREEN, topleft

padding = (50, 30)


class Text:
    def __init__(self, text, font=FONT, color=BLACK, alignment="center", border=False, width=0, height=0, margin=0):
        self.text = text

        self.width, self.height = width, height

        self.pos = None
        self.font = font
        self.color = color
        self.border = border
        self.rects = []
        self.text_surfs = []
        self.text_rects = []
        self.alignment = alignment
        self.padding = 10
        self.margin = margin
        self.size = None

    def inflate(self, pos, size):
        self.pos = pos
        self.size = size

        width = self.font.size(self.text)[0]
        if width <= size[0]:
            self.oneline_text()
        else:
            self.multiline_text()

    def update(self):
        pass

    def oneline_text(self):
        self.rects.append(pygame.Rect(topleft(self.pos, self.size), self.size))
        self.text_surfs.append(self.font.render(self.text, True, self.color))
        if self.alignment == "center":
            self.text_rects.append(self.text_surfs[0].get_rect(center=self.rects[0].center))
        elif self.alignment == "midleft":
            self.text_rects.append(self.text_surfs[0].get_rect(midleft=self.rects[0].midleft))
            self.text_rects[0].x += self.padding

    def multiline_text(self):
        words = self.text.split(" ")
        max_width, max_height = self.size[0] - self.margin, self.font.size(self.text)[1] + self.padding

        rows = []
        text = []

        for i in range(len(words)):
            word = words[i]
            text.append(word)
            width = self.font.size(" ".join(text))[0]
            if width >= max_width - self.padding:
                text.pop(len(text) - 1)
                rows.append(" ".join(text))
                text = [word]

        rows.append(" ".join(text))

        y = self.pos[1]
        y -= (len(rows) // 2 * max_height)
        if len(rows) % 2 == 0:
            y += max_height // 2

        x = self.pos[0]

        for i in range(len(rows)):
            self.text_surfs.append(self.font.render(rows[i], True, self.color))
            self.rects.append(pygame.Rect((x - max_width // 2, y - max_height // 2), (max_width, max_height)))
            if self.alignment == "center":
                self.text_rects.append(self.text_surfs[i].get_rect(center=self.rects[i].center))
            elif self.alignment == "midleft":
                self.text_rects.append(self.text_surfs[i].get_rect(midleft=self.rects[i].midleft))
                self.text_rects[i].x += self.padding
            y += max_height

    def draw(self):
        for i in range(len(self.rects)):
            SCREEN.blit(self.text_surfs[i], self.text_rects[i])
            if self.border:
                pygame.draw.rect(SCREEN, BLACK, self.rects[i], width=1)


class Icon:
    def __init__(self, color, border=False, width=0, height=0):
        self.color = color
        self.border = border
        self.width = width
        self.height = height
        self.rect = None
        self.pos = None

    def inflate(self, pos, size):
        if self.width == 0:
            self.width = size[0]
        if self.height == 0:
            self.height = size[1]

        self.pos = pos
        self.rect = pygame.Rect(topleft(self.pos, (self.width, self.height)), (self.width, self.height))

    def update(self):
        pass

    def draw(self):
        pygame.draw.rect(SCREEN, self.color, self.rect)
        if self.border:
            pygame.draw.rect(SCREEN, BLACK, self.rect, width=1)

