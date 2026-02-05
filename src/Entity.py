from src.Camera import Camera
from src.GameObject import GameObject
import pygame as pg
import numpy as np


class Entity(GameObject):
    def __init__(self, pos: np.ndarray, hitbox: np.ndarray):
        super().__init__(pos, hitbox)
        self.velocity = np.array([0,0], dtype=np.float32)

    def render(self, camera: Camera, box: np.ndarray, asset: str = "Assets/images.jpeg"):
        super().render(camera, self.hitbox, asset)

    def update(self, deltaTime: float):
        pass