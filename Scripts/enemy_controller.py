# The enemy controller
import pygame
from pygame.sprite import Sprite

# the enemy class
class Enemy(Sprite):
	def __init__(self, enemy_image_name: str, size: tuple, speed: int, enemy_center_pos: tuple):
		#basic setup
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(pygame.transform.rotate(pygame.image.load(enemy_image_name), -90), size)
		self.speed = speed
		
		#setting up enemy hit box
		self.rect = self.image.get_rect()
		self.rect.centerx = enemy_center_pos[0]
		self.rect.centery = enemy_center_pos[1]
		
	def update(self):
		self.rect.move_ip(-self.speed, 0)
		if self.rect.x <= -1000:
			self.kill()
		
