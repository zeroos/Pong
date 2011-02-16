import pygame,random
from pygame.locals import *

from Settings import *
#from Utils import loadImage
#from Utils import getSound
import Utils

class Ball(pygame.sprite.Sprite):
        """simple ball
	
	When ball gets out of the area it emits an userevent, code 0. Sides: 1-left; 2-bottom; 3-right; 4-top
	"""
	
        def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image, self.rect = Utils.loadImage('ball.png')
                self.rect = self.rect.move(
                        random.randint(Settings.safe_borders_width, Settings.screen_size[0]-Settings.safe_borders_width),
                        random.randint(Settings.safe_borders_width, Settings.screen_size[1]-Settings.safe_borders_width))
		xMove = random.choice([-1,1]) * random.randint(Settings.min_start_speed, Settings.max_start_speed)
		yMove = random.choice([-1,1]) * random.randint(Settings.min_start_speed, Settings.max_start_speed)
		
                self.move = (xMove, yMove)

		self.lineColor = Color(random.randint(30, 0xffffffff))
		self._countLineAtr()

		#Sounds.new_ball.play()
		Utils.getSound("new_ball").play()
	def _countLineAtr(self):
		try:
			self.lineA = self.move[1]/float(self.move[0])
		except ZeroDivisionError:
			self.lineA = 0
		self.lineB = self.rect.center[1] - self.lineA*self.rect.center[0]
		return

	def nextPos(self):
		"""Return next position of this object"""
		return self.rect.move(self.move)
        def update(self):
                self.rect = self.nextPos()
                if self.rect.left <= 0 or self.rect.right >= Settings.screen_size[0]:
                        self.xPong()
			if self.rect.left <= 0:
	                        pygame.event.post(pygame.event.Event(USEREVENT, {"code": 0, "side": 1, "ball": self}))
			elif self.rect.right >= Settings.screen_size[0]:
	                        pygame.event.post(pygame.event.Event(USEREVENT, {"code": 0, "side": 3, "ball": self}))
                if self.rect.top <= 0 or self.rect.bottom >= Settings.screen_size[1]:
                        self.yPong()
			if self.rect.top <= 0:
	                        pygame.event.post(pygame.event.Event(USEREVENT, {"code": 0, "side": 4, "ball": self}))
			elif self.rect.bottom >= Settings.screen_size[1]:
	                        pygame.event.post(pygame.event.Event(USEREVENT, {"code": 0, "side": 2, "ball": self}))
		self._countLineAtr() #we must count it everytime due to float precission mistakes
        def xPong(self):
                self.move = (-self.move[0], self.move[1])
        def yPong(self):
                self.move = (self.move[0], -self.move[1])
	def _collisionSide(self, obj):
		"""Checks, if objects collided vertically [returns 1], or horizontally [returns 0]. Returns -1 when objects doesnt collide each other."""
		if obj.rect.collidepoint(self.rect.midtop) ^ obj.rect.collidepoint(self.rect.midbottom):
			return 1
		if obj.rect.collidepoint(self.rect.midleft) ^ obj.rect.collidepoint(self.rect.midright):
			return 0
		return -1 #no collision

	def collision(self, obj, side=None):
		"""Collision with another object [like walls, etc.]"""
		if side == None:
			side = self._collisionSide(obj)
		if side == 1:
			if not obj.rect.colliderect(self.rect.move(self.move[0], -self.move[1])):
				self.yPong()
		elif side == 0:
			if not obj.rect.colliderect(self.rect.move(-self.move[0], self.move[0])):
				self.xPong()

		self.update()
	def pong(self, obj):
		"""Collision with a racket"""
		side = self._collisionSide(obj)
		if side == int(not obj.moving_dir):
			#collision with friction
			speed_inc = obj.speed*Settings.racket_friction

			ball_speed = self.move[int(not side)] + speed_inc
			if ball_speed > Settings.max_speed:
				ball_speed = Settings.max_speed
			
			t = [0,0]
			t[side] = self.move[side]
			t[int(not side)] = ball_speed
			self.move = tuple(t)

		self.collision(obj, side)
		
		soundPos = self.rect.center[0]/float(Settings.screen_size[0])
		s = Utils.getSound("pong").play()
		if s:
			s.set_volume(1-soundPos, soundPos)
	def kill(self):
		Utils.getSound("crash").play()
		pygame.sprite.Sprite.kill(self)

