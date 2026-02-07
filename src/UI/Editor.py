import numpy as np

from src.UI.UI import UI
from src.World.Objects.GameObject import GameObject
from src.World.World import World
import pygame as pg

class Editor(UI):
    def __init__(self, world: World):
        super().__init__(None)
        self.world = world
        self.mode = 0
        self.currentRoom = None
        self.currentBlock: GameObject|None = None

    def input(self, keys):
        if keys[pg.K_z]: self.mode = 0
        elif keys[pg.K_x]: self.mode = 1
        elif keys[pg.K_c]: self.mode = 2

        elif keys[pg.K_q]:
            self.currentRoom = None
            self.currentBlock = None
        elif keys[pg.K_e]:
            self.currentBlock = None

        if self.currentBlock is not None:
            if keys[pg.K_UP]:
                if self.mode == 0: self.currentBlock.pos[1] -= 1
                elif self.mode == 2: self.currentBlock.hitbox[1, 1] -= 1
                elif self.mode == 1:
                    self.currentBlock.pos[1] -= 1
                    self.currentBlock.hitbox[1, 1] += 1
            elif keys[pg.K_DOWN]:
                if self.mode == 0: self.currentBlock.pos[1] += 1
                elif self.mode == 1: self.currentBlock.hitbox[1, 1] += 1
                elif self.mode == 2:
                    self.currentBlock.pos[1] += 1
                    self.currentBlock.hitbox[1, 1] -= 1
            elif keys[pg.K_LEFT]:
                if self.mode == 0: self.currentBlock.pos[0] -= 1
                elif self.mode == 2: self.currentBlock.hitbox[1, 0] -= 1
                elif self.mode == 1:
                    self.currentBlock.pos[0] -= 1
                    self.currentBlock.hitbox[1, 0] += 1
            elif keys[pg.K_RIGHT]:
                if self.mode == 0: self.currentBlock.pos[0] += 1
                elif self.mode == 1: self.currentBlock.hitbox[1, 0] += 1
                elif self.mode == 2:
                    self.currentBlock.pos[0] += 1
                    self.currentBlock.hitbox[1, 0] -= 1

    def press(self, pos):
        if self.currentRoom is None:
            for room in self.world.rooms:
                if room.contains(pos, np.zeros(2)):
                    self.currentRoom = room
                    break

        if self.currentBlock is None:
            for block in self.currentRoom.objects:
                if block.collidePoint(pos):
                    self.currentBlock = block
                    break