from typing import Self
from src.Camera import Camera
import pygame as pg
import numpy as np

# superclass for stuff that can be placed in the level
# got stuff for collision and rendering
class GameObject:
    def __init__(self, pos: np.ndarray, hitbox: np.ndarray):
        self.pos = pos
        self.hitbox = hitbox

    def canCollide(self, other: Self) -> bool:
        return True

    def collide(self, other: Self) -> bool:
        return np.all(self.pos + self.hitbox < other.pos) and np.all(self.pos < other.pos + other.hitbox)

    def render(self, camera: Camera, asset: str = "Assets/images.jpeg"):
        raise NotImplementedError