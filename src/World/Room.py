import os

import numpy as np
import pygame as pg
import json
from src.Rendering.Camera import Camera
from src.World.Entities.Entity import Entity
from src.World.Entities.Player import Player
from src.World.Objects.GameObject import GameObject
from src.World.ObjectTypes import createObject, createEntity


class Room:
    def __init__(self, path: str):
        self.box = np.zeros((2,2), dtype=np.int32)
        self.entities: list[Entity] = []
        self.objects: list[GameObject] = [] # no entities
        self.background: None | pg.Surface = None
        self.path = path
        self.backgroundPath = None
        self.respawn = np.zeros(2, dtype=np.float32)

        self.load(path)

    def load(self, path: str):
        with open(path) as f:
            data = json.load(f)
        self.box = np.array(data["box"], dtype=np.int32)
        self.respawn = np.array(data["respawn"], dtype=np.float32)
        self.entities = [createEntity(self.box[0], i["type"], i["pos"]) for i in data["entities"]]
        self.objects = [createObject(self.box[0], i["type"], i["pos"], i["size"]) for i in data["objects"]]
        if data["background"]:
            self.background = pg.image.load(os.path.join("Assets", data["background"])).convert_alpha()
            self.backgroundPath = data["background"]

    def save(self):
        data = dict()
        data["box"] = self.box.tolist()
        data["respawn"] = self.respawn.astype(int).tolist()
        data["background"] = self.backgroundPath
        data["entities"] = [i.save() for i in self.entities if not i.isPlayer]
        data["objects"] = [i.save() for i in self.objects]
        with open(self.path, "w") as f:
            json.dump(data, f)

    def contains(self, pos: np.ndarray, size: np.ndarray) -> bool:
        return np.all(self.box[0] + self.box[1] > pos - size[0]) and np.all(self.box[0] < pos + size[1])

    def isOnscreen(self, camera: Camera) -> bool:
        return np.all(self.box[0] + self.box[1] > camera.pos) and np.all(self.box[0] < camera.pos + camera.size)

    def update(self, deltaTime: float):
        moved = []
        idx = 0
        while idx < len(self.entities):
            entity = self.entities[idx]
            if entity.deleted:
                self.entities.pop(idx)
                continue

            if not self.contains(entity.pos, entity.hitbox):
                moved.append(self.entities.pop(idx))
            else:
                entity.update(deltaTime, self.objects)
                idx += 1

        return moved

    def render(self, camera: Camera, animationFrame: int):
        if self.background:
            rect = self.background.get_rect()
            rect.size = (self.box[1] / camera.size * camera.screen.get_size()).astype(int)
            rect.topleft = ((self.box[0] - camera.pos) / camera.size * camera.screen.get_size()).astype(int)
            camera.screen.blit(pg.transform.scale(self.background, (rect.w, rect.h)), rect)

        for i in self.objects + self.entities:
            i.render(camera, animationFrame)

    def addEntity(self, entity: Entity):
        self.entities.append(entity)

    def addObject(self, newObject: GameObject):
        self.objects.append(newObject)