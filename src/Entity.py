from typing import Self
from src.Camera import Camera
from src.GameObject import GameObject
import numpy as np


class Entity(GameObject):
    def __init__(self, pos: np.ndarray, hitbox: np.ndarray):
        super().__init__(pos, hitbox)
        self.velocity = np.array([0,0], dtype=np.float32)

    def render(self, camera: Camera, box: np.ndarray = None, asset: str = "Assets/images.jpeg"):
        super().render(camera, self.hitbox, asset)

    def update(self, deltaTime: float, objects: list[GameObject]):
        self.pos += self.velocity * deltaTime
        for i in objects:
            if self.collide(i):
                self.adjustPos(i, self.velocity * deltaTime)

    def adjustPos(self, other: type[Self], lastMove: np.ndarray):
        # move self out of others hitbox
        # make better in the future (brain hurt)
        self.pos -= lastMove
#        change = np.zeros(2, dtype=np.float32)
#        self.pos -= change[0]
#        if not self.collide(other):
#            pass