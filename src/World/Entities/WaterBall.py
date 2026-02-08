import os.path
from src.Rendering.Camera import Camera
from src.World.Entities.Entity import Entity
import numpy as np
from src.World.Objects.GameObject import GameObject


class WaterBall(Entity):
    def __init__(self, pos, speed):
        super().__init__(pos,
                         np.array([[8,8],[24,24]]),
                         np.array((32,32)),
                         os.path.join("Assets", "32gridmap.png"))
        self.velocity = speed

        # states 0:normal, 1:bursting, 2:gone

    def collideWith(self, entity: Entity, move: np.ndarray):
        if entity.isPlayer:
            if entity.state != 2:
                entity.grow()
        self.burst()

    def burst(self):
        self.velocity = np.zeros(2)
        self.animationState = 1
        self.animationFrame = 0

    def update(self, deltaTime: float, objects: list[GameObject]):
        super().update(deltaTime, objects)

    def render(self, camera: Camera, animationFrame=0):
        # super().render(camera, animationFrame)
        # return
        if animationFrame % 6 == 0:
            if self.animationState == 1 and self.animationFrame == 5:
                self.deleted = True
            self.animationFrame = (self.animationFrame + 1) % 6
        if not self.deleted:
            if self.animationState == 0:
                self.animationFrame = 0
                super().render(camera, animationFrame)