from typing import Self
from src.Rendering.Camera import Camera
import pygame as pg
import numpy as np
from src.Rendering.SpriteSheet import SpriteSheet

# superclass for stuff that can be placed in the level
# got stuff for collision and rendering
class GameObject:
    def __init__(self, pos: np.ndarray, hitbox: np.ndarray, renderingBox: np.ndarray, asset: str|None):
        self.pos = pos
        self.hitbox = hitbox
        self.renderingBox = renderingBox
        if asset is None:
            self.spriteSheet = None
        else:
            self.spriteSheet = SpriteSheet(asset, self.renderingBox[0], self.renderingBox[1])

        self.animationFrame = 0
        self.animationState = 0 # make a statemachine handle this or some shit
        self.lookDir = np.ones(2)
        self.isPlayer = False
        self.deleted = False

    def collide(self, other: type[Self]) -> bool:
        return np.all(self.pos + self.hitbox[1] > other.pos - other.hitbox[0]) and np.all(self.pos + self.hitbox[0] < other.pos + other.hitbox[1])

    def collidePoint(self, pos: np.ndarray):
        return np.all(self.pos + self.hitbox[0] < pos) and np.all(pos < self.pos + self.hitbox[1])

    def onCollide(self, entity, move: np.ndarray):
        entity.collideWith(self, move)
        entity.adjustPos(self, move)

    def render(self, camera: Camera, animationFrame: int = 0, box = None):
        if box is None:
            box = self.renderingBox
        if self.renderingBox is None or self.spriteSheet is None:
            return
        image = self.spriteSheet.get_image(self.animationState, self.animationFrame)
        self.renderImage(image, box, camera, animationFrame)

    def renderImage(self, image, box, camera: Camera, animationFrame: int = 0):
        rect = image.get_rect()
        rect.size = (box / camera.size * camera.screen.get_size()).astype(int)

        relativePos = (self.pos - camera.pos) / camera.size * camera.screen.get_size()
        rect.center = (relativePos[0], relativePos[1])

        image = pg.transform.scale(image, (rect.w, rect.h))
        image = pg.transform.flip(image, bool(self.lookDir[0] == 1), False)
        camera.screen.blit(image, rect)

    def renderHitbox(self, camera: Camera):
        size = (self.hitbox[1] / camera.size * camera.screen.get_size()).astype(int)
        topLeft = ((self.pos + self.hitbox[0] - camera.pos - 16) / camera.size * camera.screen.get_size()).astype(int)
        pg.draw.rect(camera.screen, (0, 255, 0), (topLeft, size))

    def save(self, type: str = ""):
        data = dict()
        data["type"] = type
        data["pos"] = self.pos.tolist()
        data["size"] = self.hitbox[1].tolist()
        return data