from typing import Self
from src.Rendering.Camera import Camera
from src.World.Objects.GameObject import GameObject
import numpy as np

class Entity(GameObject):
    def __init__(self, pos: np.ndarray, hitbox: np.ndarray, renderingBox: np.ndarray, asset: str):
        super().__init__(pos, hitbox, renderingBox, asset)
        self.velocity = np.array([0,0], dtype=np.float32)

    def render(self, camera: Camera, animationFrame=0):
        super().render(camera, animationFrame)

    def update(self, deltaTime: float, objects: list[GameObject]):
        self.pos += self.velocity * deltaTime
        for i in objects:
            if self.collide(i):
                self.adjustPos(i, self.velocity * deltaTime)

    def adjustPos(self, other: GameObject, lastMove: np.ndarray):
        # move self out of others hitbox
        # make better in the future (brain hurt)
        self.pos -= lastMove
#        change = np.zeros(2, dtype=np.float32)
#        self.pos -= change[0]
#        if not self.collide(other):
#            pass

    def save(self, type: str = ""):
        data = dict()
        data["type"] = type
        data["pos"] = self.pos.tolist()
        return data