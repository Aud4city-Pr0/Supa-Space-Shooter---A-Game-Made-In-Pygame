# the player script
import pygame
from pygame.sprite import Sprite, Group
from pygame import mixer
from Scripts import laser_controller
PLAYER_DIED = pygame.USEREVENT + 1


# The player class
class Player(Sprite):
	def __init__(self, image_name: str, size: tuple, speed: int, debounce: int, player_center_pos: tuple, laser_image_name: str, health: int, enemys: Group, default_health: int, game_area: pygame.Surface, laser_sound: str, hit_sound: str):
		# basic setup
		mixer.init()
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(pygame.transform.rotate(pygame.image.load(image_name), -90), size)
		self.speed = speed
		self.laser_group = Group()
		self.debounce_delay = debounce
		self.current_time = 0
		self.is_moving_enabled = True
		self.normal_health = default_health
		self.hit_sfx = mixer.Sound(hit_sound)
		self.laser_sfx = mixer.Sound(laser_sound)
		self.inbounds_box = game_area.get_rect()
		
		
		#getting our players hitbox
		self.rect = self.image.get_rect()
		self.rect.centerx = player_center_pos[0]
		self.rect.centery = player_center_pos[1]
		self.health = health
		self.laser_image = laser_image_name
		self.PLAYERDIED = pygame.event.Event(PLAYER_DIED)
		self.enemy_container = enemys
		self.window_edge = game_area
	
	def update(self):
		self.current_ticks = pygame.time.get_ticks()
		keys = pygame.key.get_pressed()
		# right and left controlls
		if keys[pygame.K_RIGHT] == True and self.is_moving_enabled == True:
			self.rect.x += self.speed
		elif keys[pygame.K_LEFT] == True and self.is_moving_enabled == True:
			self.rect.x -= self.speed
			
		# up and down controlls
		if keys[pygame.K_UP] == True and self.is_moving_enabled == True:
			self.rect.y -= self.speed
		elif keys[pygame.K_DOWN] == True and self.is_moving_enabled == True:
			self.rect.y += self.speed
		
		self.rect.clamp_ip(self.inbounds_box)
		
		#shooting controlls
		if keys[pygame.K_SPACE] == True and self.current_ticks - self.current_time > self.debounce_delay and self.is_moving_enabled == True:
			new_laser = self.shoot_laser()
			self.laser_sfx.play()
			self.laser_group.add(new_laser)
			self.current_time = self.current_ticks
		#health system
		for collider in self.enemy_container.sprites():
			if self.rect.colliderect(collider.rect):
				self.health -= 2
				self.hit_sfx.play()
				collider.kill()
			
		#Death system
		if self.health == 0:
			pygame.event.post(self.PLAYERDIED)
			
	def shoot_laser(self):
		return laser_controller.Laser(self.laser_image, (120, 34), 22, self.rect.center, self.enemy_container)
	
	def set_movement(self, is_enabled: bool):
		self.is_moving_enabled = is_enabled
		
	def reset_health(self):
		self.health = self.normal_health
