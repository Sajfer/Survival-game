# -*- coding: UTF-8 -*-

import sys
import math
# from random import randint, choice
from Support import load_image

import pygame
from pygame.locals import *

# TODO Lägg till ett sikte som följer musen


class Player(pygame.sprite.Sprite):
    MAX_FORWARD_SPEED = 5
    MAX_REVERSE_SPEED = 0
    ACCELERATION = 2
    TURN_SPEED = 20

    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = self.image = load_image(image)
        self.position = position
        self.x, self.y = position
        self.direction = self.speed = 0
        self.k_left = self.k_right = self.k_down = self.k_up = 0
        self.rect = self.src_image.get_rect()

    def update(self):
        # UPDATES THE SPRITE
        self.speed += (self.k_up + self.k_down)
        if self.speed > self.MAX_FORWARD_SPEED:
            self.speed = self.MAX_FORWARD_SPEED
        if self.speed < -self.MAX_REVERSE_SPEED:
            self.speed = -self.MAX_REVERSE_SPEED
        self._rotate()
        self.rad = self.direction * math.pi / 180
        self.x += -self.speed * math.sin(self.rad)
        self.y += -self.speed * math.cos(self.rad)
        self.position = (self.x, self.y)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def _rotate(self):
        self.direction += (self.k_right + self.k_left)
        if self.direction > 360 or self.direction < -360:
            self.direction = 0
        self.image = pygame.transform.rotate(self.src_image, self.direction)

    def shoot(self):
        pass


class ShotSprite(pygame.sprite.Sprite):
    # Sprite for the shots
    def __init__(self, image, position, direction, speed):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = load_image(image)
        self.position = position
        self.direction = direction
        self.speed = speed + 10
        self.rect = self.src_image.get_rect()

    def update(self):
        pass


def run_game():
    # Game parameters
    WINDOW_HEIGHT, WINDOW_WIDTH = 640, 480
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))

    pygame.display.set_caption('Zombie survival')
    pygame.mouse.set_visible(1)

    rect = screen.get_rect()
    position = rect.center

    pygame.mouse.set_cursor((8, 8), (4, 4), (24, 24, 24, 231, 231, 24, 24, 24), (0, 0, 0, 0, 0, 0, 0, 0))

    # Prepare objects
    player = Player('bluecreep.bmp', position)
    running = True

    # Create The Backgound
    background = load_image("background.bmp")
    backgroundRect = background.get_rect()

    # Display The Background
    pygame.display.flip()
    clock = pygame.time.Clock()
    #
    # The main game loop
    #
    while running:
        clock.tick(30)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if not hasattr(event, 'key'):
                continue
            if event.key == K_ESCAPE:
                sys.exit(0)
            down = event.type == KEYDOWN

            # Arrow keys
            if event.key == K_RIGHT:
                player.k_right = down * -10
            elif event.key == K_LEFT:
                player.k_left = down * 10
            elif event.key == K_UP:
                player.k_up = down * 2
            elif event.key == K_DOWN:
                player.k_down = down * -2

            # WSAD
            elif event.key == K_w:
                player.k_up = down * 2
            elif event.key == K_s:
                player.k_down = down * -2
            elif event.key == K_d:
                player.k_right = down * -10
            elif event.key == K_a:
                player.k_left = down * 10

        screen.blit(background, backgroundRect)
        screen.blit(player.image, (player.x, player.y))
        pygame.display.flip()
        player.update()


def exit_game():
    sys.exit()


def test_Setup():
    WINDOW_HEIGHT, WINDOW_WIDTH = 640, 480
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
    assert screen.get_width() == WINDOW_HEIGHT
    assert screen.get_height() == WINDOW_WIDTH
    assert pygame.display.get_init() is True
    # background = load_image("background.bmp")
    assert 'b' == 'b'


if __name__ == "__main__":
    run_game()
