import os.path

import numpy as np
from src.Camera import Camera
from src.Entity import Entity
from src.GameObject import GameObject
from src.Platform import Platform


class World:
    def __init__(self):
        self.entities: list[Entity] = []
        self.objects: list[GameObject] = [] # no entities

        self.objects.append(Platform(np.array([100,100]),
                                     np.array([[0,0],[32,32]]),
                                     np.array([32,32]),
                                     os.path.join("Assets", "32gridmap.png")))

    def update(self, deltaTime: float):
        for entity in self.entities:
            entity.update(deltaTime, self.objects)

    def render(self, camera: Camera, animationFrame: int):
        for i in self.objects + self.entities:
            i.render(camera, animationFrame)