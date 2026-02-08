from src.World.Entities.Entity import Entity
from src.World.Objects.GameObject import GameObject
import numpy as np
import os.path

class Door(Entity):
    def __init__(self, pos: np.ndarray, *args):
        super().__init__(pos, np.array([[0, 0], [8, 8]], dtype=np.int32), np.array([8, 8], dtype=np.int32),
                         os.path.join("Assets", "door.png"))
        self.unlock = args[0]

    def save(self, type: str = "", *args):
        return super().save("Door", *args)

    def onCollide(self, entity, move):
        self.unlock = 1
        super().onCollide(entity, move)

    def update(self, deltaTime: float, objects: list[GameObject]):
        return

    def onUnlock(self):
        self.deleted = True