import pygame as pg
from src.Rendering.SpriteSheet import SpriteSheet


class UI:
    def __init__(self, asset: str):
        self.sheet = SpriteSheet(asset, 320, 180)
        self.state = 0
        self.animationFrame = 0

    def render(self, screen: pg.Surface, animationFrame: int = 0):
        image = self.sheet.get_image(self.state, animationFrame)
        screen.blit(pg.transform.scale(image, screen.get_size()), (0, 0))