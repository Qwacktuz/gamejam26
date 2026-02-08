from src.Rendering.Camera import Camera
from src.World.Entities.Entity import Entity
from src.World.Objects.GameObject import GameObject
from src.World.Entities.WaterBall import WaterBall
import numpy as np
import os.path
import pygame as pg

class Button(Entity):
    def __init__(self, pos: np.ndarray, *args):
        super().__init__(pos, np.array([[12, 12], [20, 20]], dtype=np.int32), np.array([8, 8], dtype=np.int32),
                         os.path.join("Assets", "button.png"))
        self.spriteSheet.images[0] = [pg.transform.flip(i, True, False) for i in self.spriteSheet.images[0]]
        self.unlock = 1

    def save(self, type: str = "", *args):
        return super().save("Button", *args)

    def update(self, deltaTime: float, objects: list[GameObject]):
        return
    
    def render(self, camera: Camera, animationFrame=0):
        self.animationFrame = 1 - self.unlock
        super().render(camera, animationFrame)

    def onCollide(self, entity, move):
        if entity.isPlayer or isinstance(entity, WaterBall):
            self.unlocked = True

    def collideWith(self, other: GameObject, move: np.ndarray):
        if other.isPlayer:
            self.unlocked = True