import numpy as np

from src.World.Entities.Button import Button
from src.World.Entities.Door import Door
from src.World.Entities.WaterBall import WaterBall
from src.World.Objects.Barrier import Barrier
from src.World.Objects.Block import Block
from src.World.Entities.Entity import Entity
from src.World.Objects.GameObject import GameObject
from src.World.Entities.Player import Player

entityTypes = {
    "Player": Player,
    "Button": Button,
    "Door": Door,
    "WaterBall": WaterBall
}

objectTypes = {
    "Block": Block,
    "Barrier": Barrier,
}

def createEntity(source, id: str, position, *args) -> Entity:
    return entityTypes[id](source + np.array(position), *args)

def createObject(source, id: str, position, size, *args) -> GameObject:
    return objectTypes[id](source + np.array(position), size, *args)