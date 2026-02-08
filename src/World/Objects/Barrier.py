import numpy as np

from src.Rendering.Camera import Camera
from src.World.Objects.GameObject import GameObject


class Barrier(GameObject):
    def __init__(self, pos: np.ndarray, size: tuple[int, int], *args):
        super().__init__(pos, np.array([[0, 0], size], dtype=np.int32), np.array([32, 32], dtype=np.int32), None)

    def render(self, camera: Camera, animationFrame: int = 0):
        self.renderHitbox(camera)
        super().render(camera, animationFrame)

    def save(self, path: str = "", *args):
        return super().save("Barrier", *args)