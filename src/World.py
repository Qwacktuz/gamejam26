import os.path
import numpy as np

from src.Player import Player
from src.Room import Room
from src.Camera import Camera


class World:
    def __init__(self):
        self.rooms: list[Room] = []

        self.rooms.append(Room(os.path.join("Assets", "Rooms", "start.json")))
        self.currentRoom = self.rooms[0]

        self.rooms.append(Room(os.path.join("Assets", "Rooms", "other.json")))

    def update(self, deltaTime: float):
        moved = self.currentRoom.update(deltaTime)
        for entity in moved:
            for room in self.rooms:
                if room.contains(entity.pos, entity.hitbox):
                    if isinstance(entity, Player):
                        self.currentRoom = room
                    room.addEntity(entity)
                    entity.update(deltaTime, room.objects)

    def render(self, camera: Camera, animationFrame: int):
        for room in self.rooms:
            room.render(camera, animationFrame)