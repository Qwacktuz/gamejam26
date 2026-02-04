import sys
import pygame as pg

pg.init()

WIDTH = 1080
HEIGHT = 720

clock = pg.time.Clock()
FPS = 60

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My *first* pg game")


WHITE = (255, 255, 255)
BLUE = (60, 60, 255)

x = 100
y = 100
speed = 5
size = 50

# Game loop
running = True
while running:
    clock.tick(FPS)  # limit FPS

    for event in pg.event.get():
        # Check if QUIT event is sent
        if event.type == pg.QUIT:
            running = False

    screen.fill(WHITE)
    pg.draw.rect(screen, BLUE, (x, y, size, size))

    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        y -= speed
    if keys[pg.K_s]:
        y += speed
    if keys[pg.K_a]:
        x -= speed
    if keys[pg.K_d]:
        x += speed

    pg.display.flip()  # render the stuff to the pg window

pg.quit()
sys.exit()
