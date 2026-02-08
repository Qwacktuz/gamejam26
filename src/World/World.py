import os.path
from src.World.Room import Room
from src.Rendering.Camera import Camera


class World:
    def __init__(self):
        self.rooms: list[Room] = []

        self.rooms.append(Room(os.path.join("Assets", "Rooms", "level1.json")))
        self.currentRoom = self.rooms[0]
        self.rooms.append(Room(os.path.join("Assets", "Rooms", "level2.json")))

    def update(self, deltaTime: float):
        moved = self.currentRoom.update(deltaTime)
        for entity in moved:
            for room in self.rooms:
                if room.contains(entity.pos, entity.hitbox):
                    if entity.isPlayer:
                        self.currentRoom = room
                        entity.room = room
                    room.addEntity(entity)
                    entity.update(deltaTime, room.objects)
                    break
            else:
                if entity.isPlayer:
                    entity.pos[:] = self.currentRoom.respawn
                    self.currentRoom.addEntity(entity)

    def render(self, camera: Camera, animationFrame: int):
        for room in self.rooms:
            room.render(camera, animationFrame)

    def save(self):
        for room in self.rooms:
            room.save()