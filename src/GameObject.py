from typing import Self
from src.Camera import Camera
import pygame as pg
import numpy as np

from src.SpriteSheet import SpriteSheet


# superclass for stuff that can be placed in the level
# got stuff for collision and rendering
class GameObject:
    def __init__(self, pos: np.ndarray, hitbox: np.ndarray, asset: str|None):
        self.pos = pos
        self.hitbox = hitbox
        self.spriteSheet = SpriteSheet(asset, 32, 32)

        self.animationFrame = 0
        self.animationState = 0 # make a statemachine handle this or some shit

    def collide(self, other: type[Self]) -> bool:
        return np.all(self.pos + self.hitbox > other.pos) and np.all(self.pos < other.pos + other.hitbox)

    def render(self, camera: Camera, box: np.ndarray = None, animationFrame: int = 0):
        if box is None or self.spriteSheet is None:
            return
        image = self.spriteSheet.get_image(self.animationState, self.animationFrame)
        rect = image.get_rect()
        rect.size = (int(box[0] / camera.size[0] * camera.screen.get_size()[0]),
                     int(box[1] / camera.size[1] * camera.screen.get_size()[1]))

        relativePos = (self.pos - camera.pos) / camera.size * camera.screen.get_size()
        rect.center = (relativePos[0], relativePos[1])

        image = pg.transform.scale(image, (rect.w, rect.h))
        camera.screen.blit(image, rect)