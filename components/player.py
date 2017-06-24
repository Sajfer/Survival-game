#!/usr/bin/python

import pygame
import Support
import math


class Player(pygame.sprite.Sprite):
    MAX_FORWARD_SPEED = 5
    MAX_REVERSE_SPEED = 1
    ACCELERATION = 2
    TURN_SPEED = 20

    def __init__(self, image, position):
        super(Player, self).__init__()
        self.src_image = self.image = Support.load_image(image, (0, 0, 0))
        self.x, self.y = position
        self.direction = self.speed = 0
        self.k_left = self.k_right = self.k_down = self.k_up = 0
        self.rect = self.src_image.get_rect()
        self.score = 0

    @property
    def pos(self):
        return self.x, self.y

    def update(self):
        # UPDATES THE SPRITE
        self.speed = (self.k_up + self.k_down)
        if self.speed > self.MAX_FORWARD_SPEED:
            self.speed = self.MAX_FORWARD_SPEED
        if self.speed < -self.MAX_REVERSE_SPEED:
            self.speed = -self.MAX_REVERSE_SPEED
        self._rotate()
        self.rad = self.direction * math.pi / 180
        self.x += -self.speed * math.sin(self.rad)
        self.y += -self.speed * math.cos(self.rad)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def _rotate(self):
        self.direction += (self.k_right + self.k_left)
        if self.direction > 360 or self.direction < -360:
            self.direction = 0
        self.image = pygame.transform.rotate(self.src_image, self.angle - 180)