from typing import Self

from src.Rendering.Camera import Camera
from src.World.Entities.Entity import Entity
from src.World.Objects.GameObject import GameObject
import numpy as np
import os.path

class Door(Entity):
    def __init__(self, pos: np.ndarray, *args):
        super().__init__(pos, np.array([[12,12], [20,20]], dtype=np.int32), np.array([8, 8], dtype=np.int32),
                         os.path.join("Assets", "door.png"))
        self.unlock = args[0]

    def save(self, type: str = "", *args):
        return super().save("Door", self.unlock)

    def onCollide(self, entity, move):
        if not self.unlocked and entity.isPlayer:
            super().onCollide(entity, move)
    
    def collide(self, other: type[Self]) -> bool:
        if not self.unlocked and other.isPlayer:
            return super().collide(other)
        return False

    def update(self, deltaTime: float, objects: list[GameObject]):
        return

    def onUnlock(self):
        self.unlocked = True 
    
    def render(self, camera: Camera, animationFrame=0):
        if not self.unlocked:
            super().render(camera, animationFrame)

    def adjustPos(self, other: GameObject, lastMove: np.ndarray):
        return