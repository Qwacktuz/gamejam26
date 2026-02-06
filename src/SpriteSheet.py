import os
import pygame as pg

class SpriteSheet:
    def __init__(self, path: str, width: int, height: int):
        if not os.path.exists(path):
            return
        self.sheet = pg.image.load(path).convert_alpha()

        self.images = self.get_images(width, height)

    def get_image(self, state, frame):
        return self.images[state][frame]

    def load_image(self, state, frame, width, height):
        image = pg.Surface((width, height), pg.SRCALPHA, 32)
        image.blit(self.sheet, (0, 0), (frame * width, state * height, width, height))
        return image

    def get_images(self, width, height):
        size = self.sheet.get_size()
        return [[self.load_image(i, j, width, height) for j in range(size[0] // height)] for i in range(size[1] // width)]