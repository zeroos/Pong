import pygame

from Settings import *

class MsgBox():
        """A box to display messages"""
        def __init__(self, color=(230, 230, 230)):
                self.font = pygame.font.Font(None, 36)
		self.fontColor = color
		self.genericFontColor = color
                self.val = ""
                self.change = True	
                self.text = self.font.render(str(self.val), 1, (self.fontColor))
		self.time = 0

		self.redR = color[0]/40
		self.redG = color[1]/40
		self.redB = color[2]/40
	def clear(self):
		self.val = " "
		self.change = True
        def draw(self, surface):
		if self.time == 1:
			self.clear()
		if self.time > 0:
			self.time -= 1
			if self.time < 40:
				self.fontColor = (self.fontColor[0]-self.redR, self.fontColor[1]-self.redG, self.fontColor[2]-self.redB)
				self.change = True
				

                if self.change:
                        rect = self.text.get_rect()
                        self.text = self.font.render(str(self.val), 1, (self.fontColor))
		nrect = self.text.get_rect()
		nrect.center = (Settings.screen_size[0]/2, Settings.screen_size[1]/2)
                surface.blit(self.text, nrect.topleft)
                if not self.change:
                        return None
                else:
                        self.change = False
                        rect.union_ip(self.text.get_rect())
                        rect.center = nrect.center
			return rect
	def display(self, txt, time=200):
		self.fontColor = self.genericFontColor
		self.val = txt
		self.change = True
		self.time = time
