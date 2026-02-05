from src.Camera import Camera
from src.GameObject import GameObject
import pygame as pg
import numpy as np


class Entity(GameObject):
    def __init__(self, pos: np.ndarray, hitbox: np.ndarray):
        super().__init__(pos, hitbox)
        self.velocity = np.array([0,0], dtype=np.float32)

    def render(self, camera: Camera, asset: str = "Assets/images.jpeg"):
        image = pg.image.load(asset).convert_alpha()
        rect = image.get_rect()
        rect.size = (self.hitbox[0] / camera.size[0] * camera.screen.get_size()[0],
                     self.hitbox[1] / camera.size[1] * camera.screen.get_size()[1])

        relativePos = (self.pos - camera.pos) / camera.size * camera.screen.get_size()
        rect.center = (relativePos[0], relativePos[1])

        image = pg.transform.scale(image, (rect.w, rect.h))
        camera.screen.blit(image, rect)

    def update(self, deltaTime: float):
        pass