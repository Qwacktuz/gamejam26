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
        self.jumpPressed = False

        self.maxSpeed = 90
        self.acceleration = 1000
        self.deacceleration = 400
        self.airFactor = 0.65

        self.jumpPower = -125
        self.jumpHBoost = 40
        self.halfGravThreshold = 40
        self.jumpThruBoost = -40

        self.bufferTime = 0.1
        self.cayoteTime = 0.1

        self.lastJump = 0
        self.lastGrounded = 0

    def input(self, y, x, jump):
        self.lastInput[0] = x
        self.lastInput[1] = y
        self.jumpPressed = jump

    def update(self, deltaTime: float, objects: list[GameObject]):
        self.velocity[0] = approach(self.velocity[0],
                                    self.maxSpeed * self.lastInput[0],
                                    (1 if self.isGrounded else self.airFactor) *
                                        (self.acceleration if np.any(self.lastInput) else self.deacceleration) *
                                        deltaTime)

        self.velocity[1] = approach(self.velocity[1],
                                    self.maxFall,
                                    self.gravity *
                                        deltaTime *
                                        (0.5 if self.jumpPressed and self.velocity[1] < self.halfGravThreshold else 1))

        if self.jumpPressed and self.velocity[1] < 0:
            self.pos[1] += self.jumpThruBoost * deltaTime

        if self.isGrounded:
            self.lastGrounded = self.cayoteTime
        else:
            self.lastGrounded -= deltaTime

        if self.lastJump > 0 and self.lastGrounded > 0:
            self.velocity[1] = self.jumpPower
            self.velocity[0] += self.lastInput[0] * self.jumpHBoost
            self.lastGrounded = 0
            self.isGrounded = False

        self.lastJump -= deltaTime
        self.lastGrounded -= deltaTime

        super().update(deltaTime, objects)
        
    def render(self, camera: Camera, animationFrame=0):
        if animationFrame % 6 == 0:
            self.animationFrame = (self.animationFrame + 1) % 6
        # self.animationState = 1 if np.any(self.lastInput) else 0
        super().render(camera, animationFrame)