import os.path

import numpy as np
from src.GameObject import GameObject


class Block(GameObject):
    def __init__(self, pos: np.ndarray, ):
        super().__init__(pos,
                         np.array([[0,0], [32,32]], dtype=np.int32),
                         np.array([32,32], dtype=np.int32),
                         os.path.join("Assets", "32gridmap.png"))