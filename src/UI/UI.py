from typing import Callable

import pygame as pg
from src.Rendering.SpriteSheet import SpriteSheet


class UI:
    def __init__(self, asset: str|None):
        if asset is None:
            self.sheet = None
        else:
            self.sheet = SpriteSheet(asset, 320, 180)
        self.state = 0
        self.animationFrame = 0

        self.buttons: dict[tuple[int], Callable] = dict()

    def render(self, screen: pg.Surface, animationFrame: int = 0):
        if self.sheet is None:
            return
        image = self.sheet.get_image(self.state, animationFrame)
        screen.blit(pg.transform.scale(image, screen.get_size()), (0, 0))

    def addButton(self, pos, size, func):
        self.buttons[(pos[0], pos[1], pos[0]+size[0], pos[1]+size[1])] = func

    def press(self, pos):
        for (l, t, r, b), func in self.buttons.items():
            if l <= pos[0] <= r and t <= pos[1] <= b:
                func()

    def input(self, keys):
        pass