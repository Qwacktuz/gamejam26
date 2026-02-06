import numpy as np
import os
from src.Camera import Camera
from src.GameObject import GameObject


class Platform(GameObject):
    def __init__(self, pos: np.ndarray, hitbox: np.ndarray, renderingBox: np.ndarray, asset: str):
        super().__init__(pos, hitbox, renderingBox, asset)

    def render(self, camera: Camera, animationFrame=0):
        super().render(camera, animationFrame)