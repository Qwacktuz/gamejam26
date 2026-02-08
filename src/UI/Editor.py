import numpy as np
from src.World.ObjectTypes import createObject, createEntity
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
        step = 1 if keys[pg.K_LSHIFT] else 8
        if keys[pg.K_z]: self.mode = 0
        elif keys[pg.K_x]: self.mode = 1
        elif keys[pg.K_c]: self.mode = 2

        elif keys[pg.K_q]:
            self.currentRoom = None
            self.currentBlock = None
        elif keys[pg.K_e]:
            self.currentBlock = None
        elif keys[pg.K_n]:
            if self.currentRoom is not None:
                self.currentBlock = createObject(self.currentRoom.box[0], "Barrier", self.currentRoom.box[1]*0.5, (32, 32))
                self.currentRoom.addObject(self.currentBlock)

        move = np.array([keys[pg.K_RIGHT] - keys[pg.K_LEFT], keys[pg.K_DOWN] - keys[pg.K_UP]])

        if self.currentBlock is not None:
            if self.mode == 0:
                self.currentBlock.pos += move * step
            elif self.mode == 1:
                self.currentBlock.hitbox[0] += move * step
                self.currentBlock.hitbox[1] -= move * step
            elif self.mode == 2:
                self.currentBlock.hitbox[1] += move * step

    def press(self, pos):
        if self.currentRoom is None:
            for room in self.world.rooms:
                if room.contains(pos, np.zeros(2)):
                    self.currentRoom = room
                    break
            else:
                return

        if self.currentBlock is None:
            for block in self.currentRoom.objects + self.currentRoom.entities:
                if block.collidePoint(pos):
                    self.currentBlock = block
                    break