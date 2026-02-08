import pygame as pg
import numpy as np
from src.Rendering.Camera import Camera
from src.UI.Editor import Editor
from src.World.Entities.Player import Player
from src.World.World import World
import os

pg.init()
pg.mixer.init()


class Game:
    def __init__(self):
        self.camera = Camera(
            np.array([0, 0], dtype=np.float32), np.array([320, 180], dtype=np.float32)
        )
        pg.display.set_caption("Game jam 26")
        pg.mixer.music.load(os.path.join("Assets", "Sounds", "sample_track2.wav"))
        pg.mixer.music.play(-1)
        pg.mixer.music.set_volume(0.5)
        self.clock = pg.time.Clock()

        self.running = True

        self.world = World()
        self.player = Player(np.array([0, 0], dtype=np.float32), self.world.currentRoom)
        self.world.currentRoom.entities.append(self.player)
        self.player.pos[:] = self.world.currentRoom.respawn

        self.animationFrame = 0
        self.music_paused = False

        # self.ui = UI(os.path.join("Assets", "dialogue1.png"))
        self.editing = False
        self.editor = Editor(self.world)

    def run(self):
        while self.running:
            deltaTime = self.clock.tick(60) * 0.001
            if deltaTime > 0.1:
                deltaTime = 1 / 60

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
                if event.key == pg.K_p and self.editing:
                    self.world.save()
                if event.key == pg.K_SPACE:
                    self.player.lastJump = self.player.bufferTime
                if event.key == pg.K_m:
                    if self.music_paused:
                        pg.mixer.music.unpause()
                        self.music_paused = False
                    else:
                        pg.mixer.music.pause()
                        self.music_paused = True

                if self.editing:
                    self.editor.input(pg.key.get_pressed())

            if event.type == pg.MOUSEBUTTONDOWN:
                if self.editing:
                    self.editor.press(self.camera.toWorldPos(event.pos))

        # add inputs here for run every frame button is held down
        keys = pg.key.get_pressed()
        # maybe scuff way to get player class to handle its own inputs
        self.player.input(
            keys[pg.K_s] - keys[pg.K_w],
            keys[pg.K_d] - keys[pg.K_a],
            keys[pg.K_SPACE],
            keys[pg.K_PERIOD],
        )

        # self.editor.input(keys)

    def render(self):
        self.camera.screen.fill((0, 0, 0))

        self.world.render(self.camera, self.animationFrame)
        # self.ui.render(self.camera.screen, 0)
        self.animationFrame += 1

        pg.display.flip()

    def update(self, deltaTime: float):
        self.world.update(deltaTime)
