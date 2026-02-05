import numpy as np
import pygame as pg
from src.Camera import Camera
from src.GameObject import GameObject


class Platform(GameObject):
    def __init__(self, pos: np.ndarray, hitbox: np.ndarray):
        super().__init__(pos, hitbox)

    def render(self, camera: Camera, box: np.ndarray = None, asset: str = "Assets/images.jpeg"):
        super().render(camera, self.hitbox, asset)