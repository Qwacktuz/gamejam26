from src.Entity import Entity
import numpy as np
import pygame as pg

class Player(Entity):
    def __init__(self, pos: np.ndarray, hitbox: np.ndarray):
        super().__init__(pos, hitbox)
        self.lastInput = np.zeros(2, dtype=np.int32)

    def input(self, y, x):
        self.lastInput[0] = x
        self.lastInput[1] = y

    def update(self, deltaTime: float):
        # self.velocity += 100 * self.lastInput * deltaTime

        # self.pos += self.velocity * deltaTime
        self.pos += self.lastInput * 300 * deltaTime