from src.Rendering.Camera import Camera
import os
import pygame as pg

class Skybox:
    def __init__(self):
        self.skybox = pg.image.load(os.path.join("Assets", "skybox.png")).convert_alpha()
        self.clouds = pg.image.load(os.path.join("Assets", "clouds.png")).convert_alpha()

        self.skyboxSpeed = -1.5
        self.cloudsSpeed = -3

    def render(self, camera: Camera):
        image = pg.transform.scale(self.skybox, self.skybox.get_size() * (camera.screen.get_size() / camera.size))
        pos = (int(camera.pos[0] * self.skyboxSpeed)) // image.get_width() * image.get_width()
        camera.screen.blit(image, (pos, int(camera.pos[1] * self.skyboxSpeed)- 200))
        camera.screen.blit(pg.transform.scale(self.skybox, self.skybox.get_size() * (camera.screen.get_size() / camera.size)),
                          (pos + image.get_width(), int(camera.pos[1] * self.skyboxSpeed) - 200))

        image = pg.transform.scale(self.clouds, self.clouds.get_size() * (camera.screen.get_size() / camera.size))
        pos = (int(camera.pos[0] * self.skyboxSpeed)) // image.get_width() * image.get_width()
        camera.screen.blit(image, (pos, int(camera.pos[1] * self.cloudsSpeed) - 50))
        camera.screen.blit(image, (pos + image.get_width(), int(camera.pos[1] * self.cloudsSpeed) - 50))