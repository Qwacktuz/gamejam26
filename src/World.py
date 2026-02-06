import os.path
import numpy as np
from src.Room import Room
from src.Camera import Camera


class World:
    def __init__(self):
        self.rooms: list[Room] = []

        self.rooms.append(Room(np.array([0,0, 500, 500]), os.path.join("Assets", "Rooms", "start.json")))

    def update(self, deltaTime: float):
        for room in self.rooms:
            room.update(deltaTime)

    def render(self, camera: Camera, animationFrame: int):
        for room in self.rooms:
            room.render(camera, animationFrame)