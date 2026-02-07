import numpy as np

from src.World.Objects.Barrier import Barrier
from src.World.Objects.Block import Block
from src.World.Entities.Entity import Entity
from src.World.Objects.GameObject import GameObject
from src.World.Entities.Player import Player

entityTypes = {
    "Player": Player

}

objectTypes = {
    "Block": Block,
    "Barrier": Barrier,
}

def createEntity(source, id: str, position) -> Entity:
    return entityTypes[id](source + np.array(position))

def createObject(source, id: str, position, size) -> GameObject:
    return objectTypes[id](source + np.array(position), size)