import pygame as pg
import numpy as np
from src.Camera import Camera
from src.Player import Player
from src.World import World

pg.init()

class Game:
    def __init__(self):
        self.camera = Camera(np.array([0,0], dtype=np.float32), np.array([320, 180], dtype=np.float32))
        pg.display.set_caption("Game jam 26")
        self.clock = pg.time.Clock()

        self.running = True

        self.player = Player(np.array([0,0], dtype=np.float32))
        self.world = World()
        self.world.rooms[0].entities.append(self.player)

        self.animationFrame = 0

    def run(self):
        while self.running:
            deltaTime = self.clock.tick(60) * 0.001

            self.inputhandler()

            self.world.update(deltaTime)

            self.camera.smoothTo(self.player.pos, deltaTime, 0.25, 10)
            self.render()

    def inputhandler(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                return

            # resize window
            if event.type == pg.VIDEORESIZE:
                self.camera.resize(event)

            # add inputs here for only on keydown
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_F11:
                    self.camera.toggleFullscreen()
                if event.key == pg.K_PLUS:
                    self.camera.zoom(0.8)
                if event.key == pg.K_MINUS:
                    self.camera.zoom(1.25)

        # add inputs here for run every frame button is held down
        keys = pg.key.get_pressed()
        # maybe scuff way to get player class to handle its own inputs
        self.player.input(keys[pg.K_s] - keys[pg.K_w], keys[pg.K_d] - keys[pg.K_a])

    def render(self):
        self.camera.screen.fill((0,0,0))

        self.world.render(self.camera, self.animationFrame)
        self.animationFrame += 1

        pg.display.flip()

    def update(self, deltaTime: float):
        self.world.update(deltaTime)