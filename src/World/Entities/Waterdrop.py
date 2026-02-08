from src.Rendering.Camera import Camera
from src.World.Entities.Entity import Entity
from src.World.Objects.GameObject import GameObject
from src.World.Entities.WaterBall import WaterBall
import numpy as np
import os.path
import pygame as pg


class Waterdrop(Entity):
    def __init__(self, pos: np.ndarray, *args):
        super().__init__(pos, np.array([[12, 12], [20, 20]], dtype=np.int32), np.array([7, 11], dtype=np.int32),
                         os.path.join("Assets", "waterdrop.png"))
        self.spriteSheet.images[0] = [pg.transform.flip(i, True, False) for i in self.spriteSheet.images[0]]

        self.state = 0
        self.respawnTimer = 0
        self.respawnTime = 5

    def save(self, type: str = "", *args):
        return super().save("Waterdrop", *args)

    def update(self, deltaTime: float, objects: list[GameObject]):
        self.respawnTimer -= deltaTime
        if self.respawnTimer <= 0:
            self.state = 0
        return

    def render(self, camera: Camera, animationFrame=0):
        # self.renderHitbox(camera)
        if self.state == 2:
            return
        if self.state == 0:
            super().render(camera, animationFrame)
        else:
            self.animationFrame = (self.animationFrame + 1) % 5
            if self.animationFrame == 0:
                self.state = 2
                self.respawnTimer = self.respawnTime
                return
            super().render(camera, animationFrame)

    def onCollide(self, entity, move):
        if entity.isPlayer and self.state == 0:
            self.state = 1
            entity.grow()

    def collideWith(self, other: GameObject, move: np.ndarray):
        if other.isPlayer:
            self.unlocked = True