from src.Rendering.Camera import Camera
from src.World.Entities.Entity import Entity
import numpy as np
import os
from src.World.Objects.GameObject import GameObject
from src.Util import approach


class Player(Entity):
    def __init__(self, pos: np.ndarray):
        super().__init__(pos,
                         np.array([[10,11],[20, 22]], dtype=np.int32),
                         np.array([32, 32], dtype=np.int32),
                         os.path.join("Assets", "Player-idle.png"))

        self.lastInput = np.zeros(2, dtype=np.int32)

        self.maxSpeed = 90
        self.acceleration = 1000
        self.deacceleration = 400

    def input(self, y, x):
        self.lastInput[0] = x
        self.lastInput[1] = y
        if y and x:
            self.lastInput * 0.7071067812

    def update(self, deltaTime: float, objects: list[GameObject]):
        self.velocity = approach(self.velocity, self.maxSpeed * self.lastInput, (self.acceleration if np.any(self.lastInput) else self.deacceleration) * deltaTime)
        super().update(deltaTime, objects)
        
    def render(self, camera: Camera, animationFrame=0):
        if animationFrame % 6 == 0:
            self.animationFrame = (self.animationFrame + 1) % 6
        # self.animationState = 1 if np.any(self.lastInput) else 0
        super().render(camera, animationFrame)