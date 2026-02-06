import numpy as np
import json
from src.Camera import Camera
from src.Entity import Entity
from src.GameObject import GameObject
from src.ObjectTypes import createObject, createEntity


class Room:
    def __init__(self, box: np.ndarray, path: str):
        self.box = box
        self.entities: list[Entity] = []
        self.objects: list[GameObject] = [] # no entities

        self.load(path)

    def load(self, path: str):
        with open(path) as f:
            data = json.load(f)
        self.entities = [createEntity(self.box[0], i["type"], i["pos"]) for i in data["entities"]]
        self.objects = [createObject(self.box[0], i["type"], i["pos"], i["size"]) for i in data["objects"]]

    def update(self, deltaTime: float):
        for entity in self.entities:
            entity.update(deltaTime, self.objects)

    def render(self, camera: Camera, animationFrame: int):
        for i in self.objects + self.entities:
            i.render(camera, animationFrame)