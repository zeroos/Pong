import pygame

from Utils import loadImage
from Settings import *

class Racket(pygame.sprite.Sprite):
	"""One racket
	
	positions: 1-left; 2-bottom; 3-right; 4-top
	
	"""
	def __init__(self, position=1):
		pygame.sprite.Sprite.__init__(self)

		if position == 1:
			imgFile = 'red_racket.png'
			startPos = (Settings.racket_distance, Settings.screen_size[1]/2)
			self.moving_dir = 0 #0-horizontal; 1-vertical
		elif position == 2:
			imgFile = 'green_racket.png'
			startPos = (Settings.screen_size[0]/2, Settings.screen_size[1]-Settings.racket_distance)
			self.moving_dir = 1 #0-horizontal; 1-vertical
		elif position == 3:
			imgFile = 'blue_racket.png'
			startPos = (Settings.screen_size[0]-Settings.racket_distance, Settings.screen_size[1]/2)
			self.moving_dir = 0 #0-horizontal; 1-vertical
		else:
			imgFile = 'yellow_racket.png'
			startPos = (Settings.screen_size[0]/2, Settings.racket_distance)
			self.moving_dir = 1 #0-horizontal; 1-vertical


		self.moving_dir = int(not self.moving_dir)
		self.image, self.rect = loadImage(imgFile)
		self.image = pygame.transform.rotate(self.image, 90*position)
		self.rect = self.image.get_rect()
		self.rect.center = startPos


		self.speed = 0 #current racket speed
		self.move = 0 #direction of the speed
	def update(self):
		if self.move:
			if abs(self.speed) < Settings.max_racket_speed:
				self.speed += Settings.racket_accel*self.move
		elif self.speed != 0:
			if abs(self.speed) < Settings.racket_brake:
				self.speed = 0
			elif self.speed < 0:
				self.speed += Settings.racket_brake
			else:
				self.speed -= Settings.racket_brake

		if self.moving_dir == 1:
			if self.rect.top+self.move < 0:
				self.rect.top = 0
				self.speed=0
			elif self.rect.bottom+self.move > Settings.screen_size[1]:
				self.rect.bottom = Settings.screen_size[1]
				self.speed=0
			else:
				self.rect.top += self.speed
		else:
			if self.rect.left+self.move < 0:
				self.rect.left = 0
				self.speed=0
			elif self.rect.right+self.move > Settings.screen_size[0]:
				self.rect.right = Settings.screen_size[0]
				self.speed=0
			else:
				self.rect.right += self.speed


	def startMovingUp(self):
		self.move=-1
	def stopMovingUp(self):
		self.move=0
	def startMovingDown(self):
		self.move=1
	def stopMovingDown(self):
		self.move=0
	def stopMoving(self):
		self.move=0

	def collision(self, obj):
		pass
	def pong(self, obj):#collision with a ball
		pass
