# -*- coding: UTF-8 -*-

import os, sys, math
from random import randint, choice
from Support import load_image

import pygame
from pygame.locals import *


from vec2d import vec2d

#def load_image(name, colorkey=None):
#	fullname = os.path.join('images', name)
#	try:
#		image = pygame.image.load(fullname)
#	except pygame.error, message:
#		print 'Cannot load image:', fullname
#		raise SystemExit, message
#	image = image.convert()
#	if colorkey is not None:
#		if colorkey is -1:
#			colorkey = image.get_at((0,0))
#		image.set_colorkey(colorkey, RLEACCEL)
#	return image, image.get_rect()

# TODO Lägg till ett sikte som följer musen‡

class Player(pygame.sprite.Sprite):
	MAX_FORWARD_SPEED = 10
	MAX_REVERSE_SPEED = 0
	ACCELERATION = 2
	TURN_SPEED = 20
	def __init__(self, image, position):
		pygame.sprite.Sprite.__init__(self)
		self.src_image = load_image(image)
		self.position = position
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
		self.direction += (self.k_right + self.k_left)
		x,y = self.position
		rad = self.direction * math.pi / 180
		x += -self.speed*math.sin(rad)
		y += -self.speed*math.cos(rad)
		self.position = (x,y)
		self.image = pygame.transform.rotate(self.src_image, self.direction)
		self.rect = self.image.get_rect()
		self.rect.center = self.position

def run_game():
	# Game parameters
	WINDOW_HEIGHT, WINDOW_WIDTH = 640,480
	pygame.init()
	screen = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))

	pygame.display.set_caption('Zombie survival')
	pygame.mouse.set_visible(1)
	
	rect = screen.get_rect()
	position = rect.center
	#Prepare objects
	player = Player('bluecreep.png',position)
	
	
	#Create The Backgound
	background = load_image("background.png")
	backgroundRect = background.get_rect()

	#Display The Background
	pygame.display.flip()
	clock = pygame.time.Clock()
	#
    # The main game loop
    #
	while True:
		clock.tick(30)
		for event in pygame.event.get():
			
			if not hasattr(event, 'key'): continue
			if event.key == K_ESCAPE: sys.exit(0)
			down = event.type == KEYDOWN
			if event.key == K_RIGHT: player.k_right = down * -10
			elif event.key == K_LEFT: player.k_left = down * 10
			elif event.key == K_UP: player.k_up = down * 2
			elif event.key == K_DOWN: player.k_down = down * -2

        screen.blit(background, backgroundRect)
        screen.blit(player.src_image, (player.x, player.y))
        pygame.display.flip()


def exit_game():
    sys.exit()


run_game()

