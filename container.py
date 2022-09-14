import pygame.sprite

from globals import SCREEN, BLACK, BACKGROUND


# assume everything in the container is centralised
class Container:
    def __init__(self, topleft, bottomright, margin=70, color=BACKGROUND):
        self.topleft = topleft
        self.midpoint = (topleft[0] + bottomright[0]) // 2, (topleft[1] + bottomright[1]) // 2
        self.margin = margin
        self.size = [bottomright[0] - topleft[0], bottomright[1] - topleft[1]]
        self.color = color
        self.type = None
        self.sprites = []

    def add(self, sprite):
        if len(self.sprites) == 0:
            self.sprites.append(sprite)
            self.type = sprite.__class__.__name__
            return

        if len(self.sprites) > 0 and sprite.__class__.__name__ == self.type:
            self.sprites.append(sprite)
            return

        raise RuntimeError("Invalid container entry, attempting to add a " + sprite.__class__.__name__ +
                           " object to a " + self.type + " array")

    def inflate(self):
        y = self.midpoint[1]

        if self.type == "Button":
            size = 250, 50
            y -= (len(self.sprites) // 2 * (size[1] + self.margin))
            if len(self.sprites) % 2 == 0:
                y += (size[1] + self.margin) // 2

            for sprite in self.sprites:
                sprite.inflate((self.midpoint[0], y), size)
                y += size[1] + self.margin

        elif self.type == "Table":
            for sprite in self.sprites:
                sprite.inflate(self.topleft, self.size)

        elif self.type == "Text":
            for sprite in self.sprites:
                sprite.inflate(self.midpoint, self.size)

    def update(self):
        for sprite in self.sprites:
            sprite.update()

    def draw(self):
        # pygame.draw.rect(SCREEN, self.color, (
        #     self.topleft[0], self.topleft[1], self.size[0], self.size[1]))

        for sprite in self.sprites:
            sprite.draw()

        # pygame.draw.circle(SCREEN, BLACK, (self.midpoint[0] - 2, self.midpoint[1] - 2), 4)
