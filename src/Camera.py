import pygame as pg
import numpy as np
from src.Util import lerp, approach


class Camera:
    def __init__(self, pos: np.ndarray, size: np.ndarray):
        self.pos = pos
        self.size = size

        displayInfo = pg.display.Info()
        self.fullscreen_size = (displayInfo.current_w, displayInfo.current_h)
        self.windowed_size = (1080, 720)

        self.screen = pg.display.set_mode(self.windowed_size, pg.RESIZABLE)
        self.isFullscreen = False

    def toggleFullscreen(self):
        self.isFullscreen = not self.isFullscreen
        if self.isFullscreen:
            self.screen = pg.display.set_mode(self.fullscreen_size, pg.FULLSCREEN)
        else:
            self.screen = pg.display.set_mode(self.windowed_size, pg.RESIZABLE)

    def resize(self, event):
        if not self.isFullscreen:
            self.windowed_size = (event.w, event.h)
            self.screen = pg.display.set_mode(self.windowed_size, pg.RESIZABLE)

    def smoothTo(self, target: np.ndarray, deltaTime: float, speed: float, minDistance: float):
        # if speed = -t/log_2(p) then the camera moves p% closer to the target in t seconds
        # p=0.01 is 1%
        self.pos = lerp(self.pos, approach(target - self.size * 0.5, self.pos, minDistance), deltaTime, speed)