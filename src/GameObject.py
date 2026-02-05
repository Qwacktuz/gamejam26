from typing import Self
from src.Camera import Camera
import pygame as pg
import numpy as np

# superclass for stuff that can be placed in the level
# got stuff for collision and rendering
class GameObject:
    def __init__(self, pos: np.ndarray, hitbox: np.ndarray):
        self.pos = pos
        self.hitbox = hitbox

    def collide(self, other: type[Self]) -> bool:
        return np.all(self.pos + self.hitbox > other.pos) and np.all(self.pos < other.pos + other.hitbox)

    def render(self, camera: Camera, box: np.ndarray = None, asset: str = "Assets/images.jpeg"):
        if box is None:
            return
        image = pg.image.load(asset).convert_alpha()
        rect = image.get_rect()
        rect.size = (int(box[0] / camera.size[0] * camera.screen.get_size()[0]),
                     int(box[1] / camera.size[1] * camera.screen.get_size()[1]))

        relativePos = (self.pos - camera.pos) / camera.size * camera.screen.get_size()
        rect.center = (relativePos[0], relativePos[1])

        image = pg.transform.scale(image, (rect.w, rect.h))
        camera.screen.blit(image, rect)