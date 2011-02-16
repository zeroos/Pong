#!/usr/bin/env python2

import os, pygame, random
from pygame.locals import *


import Ai
from Settings import *
from Ball import *
from Bonus import *
from Racket import *
from Counter import *
from MsgBox import *

class Background:
	"""background of the game, including fps meter"""
	def __init__(self):
		self.font = pygame.font.Font(None, 20)
		self.surface = pygame.Surface(Settings.screen_size)
	def update(self):
	
		self.surface.fill((0,0,0))

		if Settings.show_fps:
			self.fps = self.font.render(str(int(clock.get_fps()))+"fps", 1, (70, 70, 70))
			self.surface.blit(self.fps,  (Settings.screen_size[0]-40,1))
	def draw(self):
		if Settings.show_fps:
			return self.fps.get_rect().inflate(10,0).move((Settings.screen_size[0]-40,1))


def main():
	"""main function"""
	if not pygame.font:
		print("Cannot initialize fonts.")
		return
	global clock
	clock = pygame.time.Clock()
	pygame.init()
	screen = pygame.display.set_mode(Settings.screen_size)
	pygame.display.set_caption('Pong')
	pygame.mouse.set_visible(0)

	background = Background()
	c1 = Counter(1)
	c2 = Counter(2)
	c3 = Counter(3)
	c4 = Counter(4)
	co = Counter((Settings.screen_size[0]/2, Settings.screen_size[1]/2))
	

	#prepare sprites
	#ball = Ball()
	racket1 = Racket(1)
	racket2 = Racket(2)
	racket3 = Racket(3)
	racket4 = Racket(4)

	#allsprites = pygame.sprite.RenderUpdates((racket1, racket2, racket3, racket4))
	allsprites = pygame.sprite.RenderUpdates((racket1, racket2, racket3, racket4))

	#prepare groups
	balls = pygame.sprite.Group()
	rackets = pygame.sprite.Group()
	#balls.add(ball)
	#rackets.add([racket1, racket2, racket3, racket4])
	rackets.add([racket1, racket2, racket3, racket4])

	#set controlls
	#upKey = [(273, racket1), (273, racket4), (276, racket2)]
	#downKey = [(274, racket1), (274, racket4), (275, racket2)]
	upKey = [(273, racket1)]
	downKey = [(274, racket1)]

	msgBox = MsgBox()



	ais = []
	ais += [Ai.Smart(racket1, balls), Ai.Smart(racket3, balls), Ai.Smart(racket2, balls), Ai.Smart(racket4, balls)]


	def requestBall():
		msgBox.display("Press space to throw a new ball.", 0)

	def addBall():
		ball = Ball()
		allsprites.add(ball)
		balls.add(ball)
	def newBonus():
		bonus = Bonus()
		allsprites.add(bonus)
		
	requestBall()


	while True:
		clock.tick(50)
		
		for ai in ais:
			ai.move()

		for event in pygame.event.get():
			if event.type == USEREVENT and event.code == 0:
				co.add(1)
				if event.side == 1:
					c1.add(1)
					event.ball.kill()
					requestBall()
				elif event.side == 2:
					c2.add(1)
					event.ball.kill()
					requestBall()
				elif event.side == 3:
					c3.add(1)
					event.ball.kill()
					requestBall()
				elif event.side == 4:
					c4.add(1)
					event.ball.kill()
					requestBall()
			elif event.type == KEYDOWN:
				for key, v in upKey:
					if event.key == key:
						v.startMovingUp()
				for key, v in downKey:
					if event.key == key:
						v.startMovingDown()
				if event.key == 32:
					msgBox.clear()
					addBall()
				elif event.key == 98:
					newBonus()

			elif event.type == KEYUP:
				for key, v in upKey:
					if event.key == key:
						v.stopMovingUp()
				for key, v in downKey:
					if event.key == key:
						v.stopMovingDown()

			elif event.type == QUIT:
				return


		for iBall, iRackets in pygame.sprite.groupcollide(balls, rackets, False, False).items(): #collision between racket and a ball
			msgBox.display("boom", 70)
			for iRacket in iRackets:
				iBall.pong(iRacket)
				iRacket.pong(iBall)

		for iRacket1, iRackets in pygame.sprite.groupcollide(rackets, rackets, False, False).items(): #collision between two rackets
			for iRacket2 in iRackets:
				if iRacket1 != iRacket2:
					iRacket1.collision(iRacket2)
					iRacket2.collision(iRacket1)

			
		background.update()
		screen.blit(background.surface, (0,0))

		
		drawLines = []
		if Settings.helpLines:
			for ball in balls.sprites():
				a = ball.lineA
				b = ball.lineB
				c = ball.lineColor
				drawLines += [pygame.draw.aaline(screen, c, (0,b), (Settings.screen_size[0],a*Settings.screen_size[0]+b), 3)]


		allsprites.update()

		drawCounters = [c1.draw(screen), c2.draw(screen), c3.draw(screen), c4.draw(screen)]
		pygame.display.update(allsprites.draw(screen)+[background.draw()]+drawCounters+[msgBox.draw(screen)]+drawLines)
		pygame.display.flip()

if __name__ == '__main__':
	main()
