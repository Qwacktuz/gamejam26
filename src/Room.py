import os

import numpy as np
import pygame as pg
import json
from src.Camera import Camera
from src.Entity import Entity
from src.GameObject import GameObject
from src.ObjectTypes import createObject, createEntity


class Room:
    def __init__(self, path: str):
        self.box = np.zeros((2,2), dtype=np.int32)
        self.entities: list[Entity] = []
        self.objects: list[GameObject] = [] # no entities
        self.background: None | pg.Surface = None

        self.load(path)

    def load(self, path: str):
        with open(path) as f:
            data = json.load(f)
        self.box = np.array(data["box"], dtype=np.int32)
        self.entities = [createEntity(self.box[0], i["type"], i["pos"]) for i in data["entities"]]
        self.objects = [createObject(self.box[0], i["type"], i["pos"], i["size"]) for i in data["objects"]]
        if data["background"]:
            self.background = pg.image.load(os.path.join("Assets", data["background"])).convert_alpha()

    def contains(self, pos: np.ndarray, box: np.ndarray) -> bool:
        return np.all(self.box[0] + self.box[1] > pos - box[0]) and np.all(self.box[0] < pos + box[1])

    def isOnscreen(self, camera: Camera) -> bool:
        return True

    def update(self, deltaTime: float):
        moved = []
        for idx, entity in enumerate(self.entities):
            if not self.contains(entity.pos, entity.hitbox):
                moved.append(idx - len(moved))
            else:
                entity.update(deltaTime, self.objects)

        return [self.entities.pop(i) for i in moved]

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