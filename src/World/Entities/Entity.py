from src.Rendering.Camera import Camera
from src.World.Objects.GameObject import GameObject
import numpy as np

class Entity(GameObject):
    def __init__(self, pos: np.ndarray, hitbox: np.ndarray, renderingBox: np.ndarray, asset: str|None):
        super().__init__(pos, hitbox, renderingBox, asset)
        self.velocity = np.array([0,0], dtype=np.float32)

        self.isGrounded = False
        self.maxFall = 160
        self.gravity = 900

    def render(self, camera: Camera, animationFrame=0):
        super().render(camera, animationFrame)

    def update(self, deltaTime: float, objects: list[GameObject]):

        self.pos += self.velocity * deltaTime
        for i in objects:
            if self.collide(i):
                i.onCollide(self, self.velocity * deltaTime)

    def adjustPos(self, other: GameObject, lastMove: np.ndarray):
        # move self out of others hitbox
        needed = np.where(lastMove < 0,
                          other.pos + other.hitbox[1] - self.pos - self.hitbox[0],
                          other.pos + other.hitbox[0] - self.pos - self.hitbox[1])
        idx = np.argmin(np.abs(needed))
        self.pos[idx] += needed[idx]
        self.velocity[idx] = 0
        if idx == 1 and needed[1] < 0:
            self.isGrounded = True

    def save(self, type: str = ""):
        data = dict()
        data["type"] = type
        data["pos"] = self.pos.tolist()
        return data

    def collideWith(self, other: GameObject, move: np.ndarray):
        return