import numpy as np
import os
from src.Camera import Camera
from src.GameObject import GameObject


class Platform(GameObject):
    def __init__(self, pos: np.ndarray, hitbox: np.ndarray, asset: str):
        super().__init__(pos, hitbox, asset)

    def render(self, camera: Camera, box: np.ndarray = None, animationFrame=0):
        super().render(camera, self.hitbox, animationFrame)