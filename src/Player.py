from src.Camera import Camera
from src.Entity import Entity
import numpy as np
import os
from src.GameObject import GameObject
from src.Util import approach


class Player(Entity):
    def __init__(self, pos: np.ndarray, hitbox: np.ndarray):
        super().__init__(pos, hitbox, os.path.join("Assets", "Sprite-0003-Sheet.png"))
        self.lastInput = np.zeros(2, dtype=np.int32)

        self.maxSpeed = 300
        self.acceleration = 1000
        self.deacceleration = 400

    def input(self, y, x):
        self.lastInput[0] = x
        self.lastInput[1] = y

    def update(self, deltaTime: float, objects: list[GameObject]):
        self.velocity = approach(self.velocity, self.maxSpeed * self.lastInput, self.acceleration if not np.any(self.lastInput) else self.deacceleration)
        super().update(deltaTime, objects)
        
    def render(self, camera: Camera, box: np.ndarray = None, animationFrame=0):
        if animationFrame % 10 == 0:
            self.animationFrame = (self.animationFrame + 1) % 6
        # self.animationState = 1 if np.any(self.lastInput) else 0
        super().render(camera, box, animationFrame)