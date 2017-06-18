# -*- coding: UTF-8 -*-

import sys
import math
# from random import randint, choice
from Support import load_image, get_angle

import pygame
from pygame.locals import *

from vec2d import vec2d

# TODO Lägg till ett sikte som följer musen


class Player(pygame.sprite.Sprite):
    MAX_FORWARD_SPEED = 5
    MAX_REVERSE_SPEED = 1
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
        self.shots = []

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
        self.position = (self.x, self.y)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

        for shot in self.shots:
            shot.update()

    def _rotate(self):
        self.direction += (self.k_right + self.k_left)
        if self.direction > 360 or self.direction < -360:
            self.direction = 0
        self.image = pygame.transform.rotate(self.src_image, self.direction)

    def shoot(self, direction):
        print("Shooting")
        print(type((320, 240)))
        self.shots.append(ShotSprite('pinkcreep.png', self.position, (320, 240), 10))


class ShotSprite(pygame.sprite.Sprite):
    # Sprite for the shots
    def __init__(self, image, position, direction, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(image)
        self.position = position
        self.x, self.y = position
        self.direction = 0
        self.speed = speed
        self.rect = self.image.get_rect()

    def update(self):
        self.rad = self.direction * math.pi / 180
        self.x += -self.speed * math.sin(self.rad)
        self.y += -self.speed * math.cos(self.rad)


class game(object):
    """ Class for the main game logic """
    def __init__(self):
        pass

    @staticmethod
    def keyPressed(inputKey):
        keysPressed = pygame.key.get_pressed()
        if keysPressed[inputKey]:
            return True
        else:
            return False

    def handle_mouse(self, event):
        button_pressed = pygame.mouse.get_pressed()
        if button_pressed[0]:
            direction = pygame.mouse.get_pos()
            angle = get_angle(direction, self.player.position)
            self.player.shoot(angle)

    def handle_keypress(self, event):
        if event.key == K_ESCAPE:
            sys.exit(0)

        # Arrow keys
        if event.key == K_RIGHT:
            if self.keyPressed(K_RIGHT):
                self.player.k_right = -10
            else:
                self.player.k_right = 0
        elif event.key == K_LEFT:
            if self.keyPressed(K_LEFT):
                self.player.k_left = 10
            else:
                self.player.k_left = 0
        elif event.key == K_UP:
            if self.keyPressed(K_UP):
                self.player.k_up = 3
            else:
                self.player.k_up = 0
        elif event.key == K_DOWN:
            if self.keyPressed(K_DOWN):
                self.player.k_up = -2
            else:
                self.player.k_up = 0

        # WSAD
        elif event.key == K_w:
            if self.keyPressed(K_w):
                self.player.k_up = 3
            else:
                self.player.k_up = 0
        elif event.key == K_s:
            if self.keyPressed(K_s):
                self.player.k_up = -2
            else:
                self.player.k_up = 0
        elif event.key == K_d:
            if self.keyPressed(K_d):
                self.player.k_right = -10
            else:
                self.player.k_right = 0
        elif event.key == K_a:
            if self.keyPressed(K_a):
                self.player.k_left = 10
            else:
                self.player.k_left = 0

    def run_game(self):
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
        self.player = Player('bluecreep.bmp', position)
        self.running = True

        # Create The Backgound
        background = load_image("background.bmp")
        backgroundRect = background.get_rect()

        # Display The Background
        pygame.display.flip()
        clock = pygame.time.Clock()
        #
        # The main game loop
        #
        while self.running:
            clock.tick(30)
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                if hasattr(event, 'key'):
                    self.handle_keypress(event)
                if hasattr(event, 'pos'):
                    self.handle_mouse(event)

            screen.blit(background, backgroundRect)
            screen.blit(self.player.image, (self.player.x, self.player.y))
            for shot in self.player.shots:
                screen.blit(shot.image, (shot.x, shot.y))
            pygame.display.flip()
            self.player.update()

    def exit_game(self):
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
    game = game()
    game.run_game()
