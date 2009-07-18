# -*- coding: UTF-8 -*-

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
	
	def __init__(self, img_filename,pos):
		
		pygame.sprite.Sprite.__init__(self)

		self.img, self.img_rect =  load_image(img_filename, -1)
		self.img = self.img.convert_alpha()
		self._img = self.img
		self.img_rect = self.img_rect.move(pos)
		self.angle = 360
		self.speed = 2
		self.x, self.y = self.img_rect.center
		
	def update(self,keys):
		turn_speed = 5
		self.rotate()
		if keys[K_UP] or keys[K_w]:
			self.x += math.sin(math.radians(self.angle))*- self.speed
			self.y += math.cos(math.radians(self.angle))*-self.speed
			if keys[K_RIGHT] or keys[K_d]:
				self.angle -= turn_speed
			elif keys[K_LEFT] or keys[K_a]:
				self.angle += turn_speed
		elif keys[K_DOWN] or keys[K_s]:
			self.x += math.sin(math.radians(self.angle))*self.speed
			self.y += math.cos(math.radians(self.angle))*self.speed
			if keys[K_RIGHT] or keys[K_d]:
				self.angle += turn_speed
			elif keys[K_LEFT] or keys[K_a]:
				self.angle -= turn_speed
		elif keys[K_LEFT] or keys[K_a]:
			self.angle += turn_speed		
		elif keys[K_RIGHT] or keys[K_d]:
			self.angle -= turn_speed
		
		if self.angle > 360:
			self.angle = self.angle-360
		if self.angle <0:
			self.angle = self.angle+360
		
		self.img_rect.center = self.x, self.y
		
		x = self.img_rect.centerx
		y = self.img_rect.centery
		
	def rotate(self):
		# TODO gör rotationen mer flytande och inte hackig
		center = self.img_rect.center
		self.img = pygame.transform.rotozoom(self._img, self.angle, 1.0)
		self.img_rect = self.img.get_rect(center = center)

def run_game():
	# Game parameters
	WINDOW_HEIGHT, WINDOW_WIDTH = 640,480
	pygame.init()
	screen = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))

	pygame.display.set_caption('Zombie survival')
	pygame.mouse.set_visible(0)

	#Prepare objects
	player = Player('bluecreep.png',(300,200))
	
	
	#Create The Backgound
	background,backgroundRect = load_image("background.png")

	#Display The Background
	pygame.display.flip()
	clock = pygame.time.Clock()
	#
    # The main game loop
    #
	while True:
		clock.tick(60)
		
		keys = pygame.key.get_pressed()
		# TODO Lägg till framåt, strafe och backa
		
		
		for event in pygame.event.get():
			if event.type == QUIT:
				exit_game()
				
		player.update(keys)
		screen.blit(background, backgroundRect)
		screen.blit(player.img, (player.x, player.y))
		pygame.display.flip()


def exit_game():
    sys.exit()


run_game()

