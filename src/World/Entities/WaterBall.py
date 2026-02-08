import os.path
from src.Rendering.Camera import Camera
from src.Util import approach
from src.World.Entities.Entity import Entity
import numpy as np
from src.World.Objects.GameObject import GameObject


class WaterBall(Entity):
    def __init__(self, pos, speed):
        super().__init__(pos, np.array([[4,4], [12,12]]), np.array((16, 16)), os.path.join("Assets", "water_ball.png"))
        self.velocity = speed

        self.state = 0
        # states 0:normal, 1:bursting, 2:gone

    def collideWith(self, entity: Entity, move: np.ndarray):
        if entity.isPlayer:
            if entity.state != 2 and entity.dashCooldownTimer < 0.3:
                entity.grow()
            else:
                return
        self.burst()

    def onCollide(self, entity, move: np.ndarray):
        # self.burst()
        return

    def burst(self):
        self.velocity = np.zeros(2)
        self.state = 1
        self.animationFrame = max(0, self.animationFrame)

    def update(self, deltaTime: float, objects: list[GameObject]):
        self.velocity[1] = approach(self.velocity[1], self.maxFall, self.gravity * deltaTime)
        super().update(deltaTime, objects)

    def render(self, camera: Camera, animationFrame=0):
        # super().render(camera, animationFrame)
        # return
        if animationFrame % 6 == 0:
            if self.state == 1:
                if self.animationFrame == 2:
                    self.deleted = True

                self.animationFrame = (self.animationFrame + 1) % 3
        if not self.deleted:
            if self.state == 0:
                self.animationFrame = 0
            super().render(camera, animationFrame)