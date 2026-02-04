import pygame as pg
pg.init()

class Game:
    def __init__(self):
        displayInfo = pg.display.Info()
        self.fullscreen_size = (displayInfo.current_w, displayInfo.current_h)
        self.windowed_size = (1080, 720)

        self.screen = pg.display.set_mode(self.windowed_size, pg.RESIZABLE)
        self.isFullscreen = False
        self.running = True

        self.clock = pg.time.Clock()

    def run(self):
        while self.running:
            deltaTime = self.clock.tick(60) * 0.001

            self.inputhandler()
            self.render()

    def inputhandler(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                return

            # resize window
            if event.type == pg.VIDEORESIZE and not self.isFullscreen:
                self.windowed_size = (event.w, event.h)
                self.screen = pg.display.set_mode(self.windowed_size, pg.RESIZABLE)

            # add here for only on keydown
            if event.type == pg.KEYDOWN:
                # toggle fullscreen
                if event.key == pg.K_F11:
                    self.isFullscreen = not self.isFullscreen
                    if self.isFullscreen:
                        self.screen = pg.display.set_mode(self.fullscreen_size, pg.FULLSCREEN)
                    else:
                        self.screen = pg.display.set_mode(self.windowed_size, pg.RESIZABLE)

            # add here for run every tick button is held down
            keys = pg.key.get_pressed()
            #if keys[pg.K_w]:

    def render(self):
        self.screen.fill((0,0,0))
        pg.draw.rect(self.screen, (255,0,0), (200, 200, 100, 100))
        pg.display.flip()