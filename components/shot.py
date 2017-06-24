#!/usr/bin/python

import pygame
import Support


class Shot(pygame.sprite.Sprite):
    # Sprite for the shots
    def __init__(self, image, player_pos, mouse_pos, angle, speed):
        super(Shot, self).__init__()
        self.image = image
        self.x, self.y = player_pos
        self.direction = angle
        self.speed = speed
        self.rect = self.image.get_rect()
        self.target_vector = Support.normalize(Support.sub(mouse_pos, player_pos))
        self._rotate()

    @property
    def pos(self):
        return self.x, self.y

    def _rotate(self):
        self.image = pygame.transform.rotate(self.image, self.direction)

    def update(self):
        move_vector = [c * self.speed for c in Support.normalize(self.target_vector)]

        self.x, self.y = Support.add(self.pos, move_vector)