import pygame

from globals import getTopleft, BLACK, SCREEN


# assume everything in the container is centralised
class Container:
    def __init__(self, id, midpoint, size, margin=70, color=BLACK):
        self.id = id
        self.midpoint = midpoint
        self.margin = margin
        self.size = size
        self.type = None
        self.sprites = []
        self.color = color

    def add(self, sprite):
        if len(self.sprites) == 0:
            self.sprites.append(sprite)
            self.type = sprite.__class__.__name__
            return

        if len(self.sprites) > 0 and sprite.__class__.__name__ == self.type:
            self.sprites.append(sprite)
            return

        raise RuntimeError("Invalid container entry, attempting to add a " + sprite.__class__.__name__ +
                           " object to a " + self.type + " container!")

    def inflate(self):
        y = self.midpoint[1]

        if self.type == "Button":
            size = 320, 64
            y -= ((len(self.sprites) // 2) * (size[1] + self.margin))
            if len(self.sprites) % 2 == 0:
                y += (size[1] + self.margin) / 2

            for sprite in self.sprites:
                sprite.inflate((self.midpoint[0], y), size)
                y += size[1] + self.margin

        elif self.type == "Table":
            for sprite in self.sprites:
                sprite.inflate(getTopleft(self.midpoint, self.size), self.size)

        elif self.type == "Text":
            for sprite in self.sprites:
                sprite.inflate(self.midpoint, self.size)

        elif self.type == "Board":
            for sprite in self.sprites:
                sprite.inflate(getTopleft(self.midpoint, self.size), self.size)

    def change_visibility(self):
        for sprite in self.sprites:
            sprite.visible = not sprite.visible

    def update(self):
        for sprite in self.sprites:
            sprite.update()

    def draw(self):
        for sprite in self.sprites:
            sprite.draw()
