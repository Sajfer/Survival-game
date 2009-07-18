# -*- coding: utf-8 -*-

import os, sys, math
from random import randint, choice

import pygame
from pygame.locals import *


from vec2d import vec2d

def load_image(name, colorkey=None):
	fullname = os.path.join('images', name)
	try:
		image = pygame.image.load(fullname)
	except pygame.error, message:
		print 'Cannot load image:', fullname
		raise SystemExit, message
	image = image.convert()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = image.get_at((0,0))
		image.set_colorkey(colorkey, RLEACCEL)
	return image, image.get_rect()

# TODO Lägg till ett sikte som följer musen‡

class Player(pygame.sprite.Sprite):
	
	def __init__(self, img_filename):
		
		pygame.sprite.Sprite.__init__(self)

		self.image, self.image_rect =  load_image(img_filename, -1)
		self.image = self.image.convert_alpha()
		self.base_img = self.image
		
		self.pos = vec2d((300,200))
		
	def update(self):
		self.rotate()
		
	def rotate(self):
		# TODO gör rotationen mer flytande och inte hackig
		pos = pygame.mouse.get_pos()
		x = pos[0] - self.pos[0]
		y = pos[1] - self.pos[1]
		angle = math.atan2(x,y)
		angle = (angle * 180) / math.pi
		print x, y
		self.image = pygame.transform.rotate(self.base_img, -angle)

def run_game():
	# Game parameters
	WINDOW_HEIGHT, WINDOW_WIDTH = 640,480
	pygame.init()
	screen = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))

	pygame.display.set_caption('Zombie survival')
	pygame.mouse.set_visible(0)

	#Prepare objects
	player = Player('bluecreep.png')

	#Create The Backgound
	background,backgroundRect = load_image("background.png")

	#Display The Background
	pygame.display.flip()
	clock = pygame.time.Clock()

    # The main game loop
    #
	while True:
		clock.tick(60)
		# TODO Lägg till framåt, strafe och backa
		for event in pygame.event.get():
			if event.type == QUIT:
				exit_game()
			elif event.type == KEYDOWN and event.key == K_w:
				pass
			elif event.type == KEYDOWN and event.key == K_a:
				pass
			elif event.type == KEYDOWN and event.key == K_s:
				pass
			elif event.type == KEYDOWN and event.key == K_d:
				pass
				
		player.update()
		screen.blit(background, backgroundRect)
		screen.blit(player.image, player.pos)
		pygame.display.flip()


def exit_game():
    sys.exit()


run_game()

