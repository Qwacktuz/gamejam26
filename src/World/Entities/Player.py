from src.Rendering.Camera import Camera
from src.Rendering.SpriteSheet import SpriteSheet
from src.World.Entities.Entity import Entity
import numpy as np
import os
from src.World.Entities.WaterBall import WaterBall
from src.World.Objects.GameObject import GameObject
from src.Util import approach
import pygame as pg

class Player(Entity):
    def __init__(self, pos: np.ndarray, room):
        self.hitboxes = np.array([[[16,15],[22,21]],
                                         [[10,11],[20,22]]], dtype=np.int32)
        self.renderingBoxes = np.array([[16,10],
                                               [32,32]], dtype=np.int32)
        self.maxSize = 1
        self.size = 1

        super().__init__(pos,
                         self.hitboxes[self.size],
                         self.renderingBoxes[self.size],
                         None)
        self.room = room
        self.isPlayer = True

        self.dashArrow = SpriteSheet(os.path.join("Assets", "arrows.png"), 64, 64)
        for i in range(5):
            self.dashArrow.images[0].insert(i * 3 + 1, pg.transform.rotate(self.dashArrow.images[0][i * 3], -90))
        self.dashArrowFrame = 0

        self.spriteSheets = [SpriteSheet(os.path.join("Assets", "kitty_small.png"),  16, 10),
                             SpriteSheet(os.path.join("Assets", "kitty_normal.png"), 32, 32)]
        self.spriteSheet = self.spriteSheets[self.size]

        self.frameTimes = [6, 4, 4, 6]

        self.lastInput = np.zeros(2, dtype=np.int32)
        self.jumpPressed = False
        self.dashPressed = False

        self.state = 0  # 0:normal, 1:dash, 2: dashing

        self.maxSpeed = 90
        self.acceleration = 1000
        self.deacceleration = 400
        self.airFactor = 0.65

        self.jumpSound = pg.mixer.Sound(
            os.path.join("Assets", "Sounds", "sfx_jump1.wav")
        )
        self.dashSound = pg.mixer.Sound(
            os.path.join("Assets", "Sounds", "sfx_swish1.wav")
        )
        self.shrinkSound = pg.mixer.Sound(
            os.path.join("Assets", "Sounds", "sfx_dash2.wav")
        )
        self.growSound = pg.mixer.Sound(
            os.path.join("Assets", "Sounds", "sfx_water_swirl1.wav")
        )

        self.jumpPower = -125
        self.jumpHBoost = 40
        self.halfGravThreshold = 40
        self.jumpThruBoost = -40
        self.stoppedJump = False

        self.bufferTime = 0.1
        self.cayoteTime = 0.3

        self.lastJump = 0
        self.lastGrounded = 0

        self.lastDash = 0
        self.dashTransTimer = 0
        self.dashTransTime = 0.6
        self.dashCooldownTimer = 0
        self.dashCooldown = 0.25
        self.dashTimer = 0
        self.dashTime = 0.15
        self.dashSpeed = 200
        self.lastDashDirection = np.array([1, 0], dtype=int)
        self.dashDirection = np.zeros(2)

    def input(self, y, x, jump, dash):
        self.lastInput[0] = x
        self.lastInput[1] = y
        self.jumpPressed = jump
        self.dashPressed = dash
        if np.any(self.lastInput):
            self.lastDashDirection[:] = (x, y)
        if x != 0:
            self.lookDir[0] = x
        if not jump:
            self.stoppedJump = True

    def update(self, deltaTime: float, objects: list[GameObject]):
        if (
            self.lastDash > 0
            and self.state == 0
            and self.dashCooldownTimer < 0
            and self.size > 0
        ):
            self.state = 1
            self.lastJump = 0
            self.lastGrounded = 0
            self.animationFrame = 0
            self.lastDash = 0
            self.dashTransTimer = self.dashTransTime
            self.dashArrowFrame = 0
            self.stoppedJump = True

        if self.state == 0:
            self.velocity[0] = approach(
                self.velocity[0],
                self.maxSpeed * self.lastInput[0],
                (1 if self.isGrounded else self.airFactor)
                * (self.acceleration if np.any(self.lastInput) else self.deacceleration)
                * deltaTime,
            )

            self.velocity[1] = approach(
                self.velocity[1],
                self.maxFall,
                self.gravity
                * deltaTime
                * (
                    0.5
                    if self.jumpPressed and self.velocity[1] < self.halfGravThreshold
                    else 1
                ),
            )

            if self.jumpPressed and self.velocity[1] < 0 and not self.stoppedJump and self.dashCooldownTimer < -0.5:
                self.pos[1] += self.jumpThruBoost * deltaTime

            if self.isGrounded:
                self.lastGrounded = self.cayoteTime
                self.stoppedJump = False
            else:
                self.lastGrounded -= deltaTime

            if self.lastJump > 0 and self.lastGrounded > 0:
                self.velocity[1] = self.jumpPower
                self.velocity[0] += self.lastInput[0] * self.jumpHBoost
                self.lastGrounded = 0
                self.animationFrame = 0
                self.jumpSound.play()

            self.lastJump -= deltaTime
            self.lastDash -= deltaTime
            self.lastGrounded -= deltaTime
            self.dashCooldownTimer -= deltaTime

        elif self.state == 1:
            self.velocity = approach(self.velocity, 0, self.acceleration * deltaTime)
            self.dashTransTimer -= deltaTime
            if self.dashTransTimer < 0 or not self.dashPressed:
                self.state = 2
                self.dashTimer = self.dashTime
                self.dashDirection = self.lastDashDirection.copy()
                self.room.addEntity(WaterBall(self.pos.copy(), -2 * self.dashDirection * self.dashSpeed))
                self.shrink()
                self.dashSound.play()

        elif self.state == 2:
            self.velocity = self.dashDirection * self.dashSpeed

            self.dashTimer -= deltaTime
            if self.dashTimer < 0:
                self.state = 0
                self.dashCooldownTimer = self.dashCooldown
                self.animationState = 1
                self.animationFrame = 2

        self.updateState()
        self.isGrounded = False
        super().update(deltaTime, objects)

    def render(self, camera: Camera, animationFrame=0):
        if animationFrame % self.frameTimes[self.animationState] == 0:
            if self.animationState == 2 and self.animationFrame == 5:  # go to dashBall
                self.animationState = 3
                self.animationFrame = -1
            self.animationFrame = (self.animationFrame + 1) % 6

        if self.jumpPressed and self.velocity[1] < 0:
            self.animationFrame = min(self.animationFrame, 2)

        if self.state == 1 or self.state == 2:
            if animationFrame % 3 == 0:
                self.dashArrowFrame = min(self.dashArrowFrame + 1, 4)
            image = self.dashArrow.get_image(
                0,
                3 * self.dashArrowFrame
                + abs(self.lastDashDirection[1])
                + 2 * abs(self.lastDashDirection[0])
                - 1,
            )
            image = pg.transform.flip(image, True, bool(self.lastDashDirection[1] == 1))
            self.renderImage(image, (64, 64), camera, 0)

        super().render(camera, animationFrame)

    def updateState(self):
        # 0: idle, 1: running, 2: enterDash, 3: dashBall
        if self.isGrounded:
            if not np.any(np.abs(self.velocity) > 30):
                self.animationState = 0
            else:
                self.animationState = 1
        if self.state == 1 and self.animationState != 3:
            self.animationState = 2

    def grow(self):
        self.size = min(self.maxSize, self.size + 1)
        self.spriteSheet = self.spriteSheets[self.size]
        self.hitbox = self.hitboxes[self.size]
        self.renderingBox = self.renderingBoxes[self.size]
        self.growSound.play()

    def shrink(self):
        self.size = max(0, self.size - 1)
        self.spriteSheet = self.spriteSheets[self.size]
        self.hitbox = self.hitboxes[self.size]
        self.renderingBox = self.renderingBoxes[self.size]
        self.animationState = 1
        self.shrinkSound.play()

    def onCollide(self, entity: Entity, move: np.ndarray):
        entity.collideWith(self, move)
        return
