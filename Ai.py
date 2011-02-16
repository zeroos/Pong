import pygame,random
from Settings import *

class Ai():
	"""Base class for artifical intelligences"""
	def __init__(self, obj, balls=None, rackets=None):
		self.obj = obj
		self.balls = balls
		self.rackets = rackets
	def move(self):
		pass

class Silly(Ai):
	def move(self):
		if self.obj.speed == 0:
			if self.obj.move == 1:
				self.obj.startMovingUp()
			else:
				self.obj.startMovingDown()

class BallFollower(Ai):
	def __init__(self, obj, balls, rackets=None):
		Ai.__init__(self,obj, balls, rackets)
	def move(self):
		if len(self.balls.sprites()) > 0:
			def dist(b):
				return abs(b.center[self.obj.moving_dir] - self.obj.rect.center[self.obj.moving_dir])

			
			ball = None
			for b in self.balls.sprites():
				if dist(b.nextPos()) >= dist(b.rect):
					continue #jesli sie oddala olej
				if ball == None:
					ball = b
				elif dist(b.rect) < dist(ball.rect):
					ball = b
			if ball == None:
				ball = b


			if self.obj.moving_dir == 1:
				if ball.rect.top-30 < self.obj.rect.top:
					self.obj.startMovingUp()
				elif ball.rect.bottom+30 > self.obj.rect.bottom:
					self.obj.startMovingDown()
				else:
					self.obj.stopMoving()
			else:
				if ball.rect.left-30 < self.obj.rect.left:
					self.obj.startMovingUp()
				elif ball.rect.right+30 > self.obj.rect.right:
					self.obj.startMovingDown()
				else:
					self.obj.stopMoving()
class Smart(Ai):
	def __init__(self, obj, balls, rackets=None):
		Ai.__init__(self,obj, balls, rackets)

	def _stopping_dist(self):
		"""distance to self-stop"""
		return pow(self.obj.speed, 2)/(2*float(Settings.racket_brake))

	def _braking_dist(self):
		"""distance to stop when braking [trying to go in opposite direction]"""
		return pow(self.obj.speed, 2)/(2*float(Settings.racket_accel))
	def _goTo(self,p):
		if self.obj.rect.center[self.obj.moving_dir] > p+self._stopping_dist()+Settings.racket_accel:
                        self.obj.startMovingUp()
                elif self.obj.rect.center[self.obj.moving_dir] < p-self._stopping_dist()-Settings.racket_accel:
                        self.obj.startMovingDown()
		#elif self.obj.rect.center[self.obj.moving_dir] > p+Settings.racket_accel:
		#	self.obj.startMovingDown()#start braking
                #elif self.obj.rect.center[self.obj.moving_dir] < p-Settings.racket_accel:
                #        self.obj.startMovingUp()#start braking
		else:
			self.obj.stopMoving()

	def move(self):
		try:
			#choose a proper ball
			minT = 999999999 #infinity
			for b in self.balls.sprites():
				k = not self.obj.moving_dir #ball moving_dir
				
				#v=s/t  t=s/v
				s = abs(b.rect.center[k]-self.obj.rect.center[k])
				v = abs(b.rect.center[k]-self.obj.rect.center[k]) - abs((b.nextPos()).center[k]-self.obj.rect.center[k])
				if v>0:
					t=s/v
					if t<minT:
						minT = t
						ball = b
			
			#count where the ball will collide with the racket, and go there

			a = ball.lineA
			b = ball.lineB

			if self.obj.moving_dir == 1: #horizontal
				self._goTo(a*self.obj.rect[0] + b)
			elif self.obj.moving_dir == 0: #vertical
				if a != 0:
					self._goTo((self.obj.rect[1]-b)/a)
				else:
					self._goTo(b)
			
			#self.obj.startMovingDown()
		except UnboundLocalError: #if no ball was selected
			self._goTo(Settings.screen_size[self.obj.moving_dir]/2)


