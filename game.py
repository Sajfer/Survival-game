# -*- coding: UTF-8 -*-

import sys
import math
import os
# from random import randint, choice
import Support

import pygame
from pygame.locals import *

# TODO Lägg till ett sikte som följer musen


class Player(pygame.sprite.Sprite):
    MAX_FORWARD_SPEED = 5
    MAX_REVERSE_SPEED = 1
    ACCELERATION = 2
    TURN_SPEED = 20

    def __init__(self, image, position):
        super(Player, self).__init__()
        self.src_image = self.image = Support.load_image(image, (0, 0, 0))
        self.position = position
        self.x, self.y = position
        self.direction = self.speed = 0
        self.k_left = self.k_right = self.k_down = self.k_up = 0
        self.rect = self.src_image.get_rect()
        self.score = 0

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

    def _rotate(self):
        self.direction += (self.k_right + self.k_left)
        if self.direction > 360 or self.direction < -360:
            self.direction = 0
        self.image = pygame.transform.rotate(self.src_image, self.angle - 180)


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
            mouse_pos = pygame.mouse.get_pos()
            self.bullets.add(Shot(self.bullet, self.player.position, mouse_pos, self.player.angle, 10))

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
        self.myfont = pygame.font.SysFont("monospace", 15)

        pygame.display.set_caption('Zombie survival')
        pygame.mouse.set_visible(1)

        rect = screen.get_rect()
        position = rect.center

        pygame.mouse.set_cursor((8, 8), (4, 4), (24, 24, 24, 231, 231, 24, 24, 24), (0, 0, 0, 0, 0, 0, 0, 0))

        fullname = os.path.join('images')
        fullname = os.path.join(fullname, 'M484BulletCollection1.png')

        ss = Support.spritesheet(fullname)
        self.bullet = ss.image_at((328, 230, 10, 13), (0, 0, 0))

        self.bullets = pygame.sprite.Group()

        # Prepare objects

        self.player = Player('bluecreep.bmp', position)
        self.running = True

        # Create The Backgound
        background = Support.load_image("background.bmp")
        backgroundRect = background.get_rect()

        # Display The Background
        pygame.display.flip()
        clock = pygame.time.Clock()
        alive = 0
        #
        # The main game loop
        #
        while self.running:
            clock.tick(30)

            if alive > 10:
                self.player.score += 1
                alive = 0

            target_vector = Support.normalize(Support.sub(pygame.mouse.get_pos(), self.player.position))
            aangle = 180 * Support.angle(target_vector, [0, 1]) / math.pi
            if target_vector[0] < 0:
                aangle *= -1
            self.player.angle = aangle

            score = self.myfont.render("Score: {}".format(self.player.score), 1, (0, 0, 0))
            fps = self.myfont.render("fps: {0:.2f}".format(clock.get_fps()), 1, (0, 0, 0))

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                if hasattr(event, 'key'):
                    self.handle_keypress(event)
                if hasattr(event, 'pos'):
                    self.handle_mouse(event)

            screen.blit(background, backgroundRect)
            screen.blit(self.player.image, (self.player.x, self.player.y))
            screen.blit(score, (0, 0))
            screen.blit(fps, (0, 20))
            for bullet in self.bullets:
                screen.blit(bullet.image, (bullet.x, bullet.y))
            pygame.display.flip()
            self.player.update()
            self.bullets.update()

            alive += 1

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
