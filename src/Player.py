from src.Entity import Entity
import numpy as np
import pygame as pg

from src.Util import approach


class Player(Entity):
    def __init__(self, pos: np.ndarray, hitbox: np.ndarray):
        super().__init__(pos, hitbox)
        self.lastInput = np.zeros(2, dtype=np.int32)
        self.velocity = np.zeros(2, dtype=np.float32)

        self.maxSpeed = 300
        self.acceleration = 1000
        self.deacceleration = 400

    def input(self, y, x):
        self.lastInput[0] = x
        self.lastInput[1] = y

    def update(self, deltaTime: float):
        self.velocity = approach(self.velocity, self.maxSpeed * self.lastInput, self.acceleration if not np.any(self.lastInput) else self.deacceleration)
        self.pos += self.velocity * deltaTime
        # self.velocity += 100 * self.lastInput * deltaTime

        # self.pos += self.velocity * deltaTime
        # self.pos += self.lastInput * 300 * deltaTime