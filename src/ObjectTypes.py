import numpy as np

from src.Block import Block
from src.Player import Player

entityTypes = {
    "Player": Player

}

objectTypes = {
    "Block": Block
}

def createEntity(source, id: str, position):
    return entityTypes[id](source + np.array(position))

def createObject(source, id: str, position, size):
    return objectTypes[id](source + np.array(position))