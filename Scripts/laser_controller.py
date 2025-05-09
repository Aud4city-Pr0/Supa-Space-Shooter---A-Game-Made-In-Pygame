# The laser script
import pygame
from pygame.sprite import Sprite, Group
LASER_HIT = pygame.USEREVENT + 3


# the laser class
class Laser(Sprite):
	def __init__(self, laser_image: str, size: tuple, speed: int, position, group_to_kill: Group):
		# basic setup
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(pygame.transform.rotate(pygame.image.load(laser_image), -90), size)
		self.speed = speed
		
		# getting laser hitbox
		self.rect = self.image.get_rect()
		self.rect.center = position
		self.to_kill = group_to_kill
		self.LASER_HIT_EVENT = pygame.event.Event(LASER_HIT)

	# the laser code
	def update(self):
		self.rect.move_ip(self.speed, 0)

		if self.rect.x >= 1900:
			self.kill()
		for collider in self.to_kill.sprites():
			if self.rect.colliderect(collider.rect):
				collider.kill()
				self.kill()
				pygame.event.post(self.LASER_HIT_EVENT)
		

