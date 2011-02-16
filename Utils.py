import pygame,os
from Settings import *


pygame.mixer.init()
def loadSound(name):
	class NoneSound:
		def play(self): pass
	if not pygame.mixer or not Settings.sounds:
		return NoneSound()
	
	fullname = os.path.join(data_dir, 'sounds', name)
	try:
		sound = pygame.mixer.Sound(fullname)
	except pygame.error, message:
		print 'Cannot load sound:', fullname
		raise SystemExit, message
	return sound



def getSound(sound):
	return loadSound(sound + '.ogg')


def loadImage(name, colorkey=None):
        fullName = os.path.join(data_dir, name)
        try:
                image = pygame.image.load(fullName)
        except pygame.error:
                print 'Cannot load image:', fullName
                raise SystemExit()
        return image, image.get_rect()
