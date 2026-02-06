import numpy as np

from src.Barrier import Barrier
from src.Block import Block
from src.Entity import Entity
from src.GameObject import GameObject
from src.Player import Player

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