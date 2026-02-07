import pygame as pg
from typing import Self

class SpriteSheet:
    sheets: dict[str, Self] = dict()

    def __new__(cls, path: str, width: int, height: int):
        if path in cls.sheets:
            return cls.sheets[path]

        self = super().__new__(cls)

        print(f"Loading {path}")
        self.sheet = pg.image.load(path).convert_alpha()
        self.images = self.get_images(width, height)

        cls.sheets[path] = self
        return self

    def get_image(self, state, frame):
        return self.images[state][frame]

    def load_image(self, state, frame, width, height):
        image = pg.Surface((width, height), pg.SRCALPHA, 32)
        image.blit(self.sheet, (0, 0), (frame * width, state * height, width, height))
        return image

    def get_images(self, width, height):
        size = self.sheet.get_size()
        return [[self.load_image(i, j, width, height) for j in range(size[0] // width)] for i in range(size[1] // height)]