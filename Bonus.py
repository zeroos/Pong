import pygame,random
from pygame.locals import *

from Settings import *
import Utils

class Bonus(pygame.sprite.Sprite):
        """bonuses base-class"""
	
        def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image, self.rect = Utils.loadImage(str.lower(self.__class__.__name__) + '.png')
                self.rect = self.rect.move(
                        random.randint(Settings.safe_borders_width, Settings.screen_size[0]-Settings.safe_borders_width),
                        random.randint(Settings.safe_borders_width, Settings.screen_size[1]-Settings.safe_borders_width))

		Utils.getSound("new_bonus")	
        def update(self):
		pass
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
	def kill(self):
		Sounds.get("bonus_destroy").play()
		#Sounds.bonus_destroy.play()
		pygame.sprite.Sprite.kill(self)

