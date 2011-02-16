import pygame

from Settings import *

class Counter():
        """counter class
	
	pos could be 1-topLeft;2-bottomLeft;3-bottomRight;4-topRight or touple (x, y)
	
	"""
        def __init__(self, pos=1, color=(230, 230, 230)):
                self.font = pygame.font.Font(None, 36)
                self.val = 0
                self.change = True

		if pos == 1:
			self.fontColor = (230, 0, 0)
			self.pos = (10,10)
		elif pos == 2:
			self.fontColor = (0, 230, 0)
			self.pos = (10, Settings.screen_size[1]-40)
		elif pos == 3:
			self.fontColor = (0, 0, 230)
			self.pos = (Settings.screen_size[0]-30, Settings.screen_size[1]-40)
		elif pos == 4:
			self.fontColor = (230, 230, 0)
			self.pos = (Settings.screen_size[0]-30, 10)
		else:
                	self.fontColor = color
	                self.pos = pos
                self.text = self.font.render(str(self.val), 1, (self.fontColor))
        def add(self, val = 1):
                self.val += val
                self.change = True
        def set(self, val = 0):
                self.val = val
                self.change = True

        def draw(self, surface):
                if self.change:
                        rect = self.text.get_rect()
                        self.text = self.font.render(str(self.val), 1, (self.fontColor))
                surface.blit(self.text, self.pos)
                if not self.change:
                        return None
                else:
                        self.change = False
                        rect.union_ip(self.text.get_rect())
                        return rect.move(self.pos)
