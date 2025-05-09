# This is the main game script
# to run it use "python3 main.py"
# it also has imports for the project
import pygame, random, os, time
pygame.init()
pygame.font.init()
pygame.mixer.init()
from Scripts import player_controller, enemy_controller, laser_controller, score_controller
from Scripts.player_controller import Player
ENEMY_SPAWN_EVENT = pygame.USEREVENT + 2
TIMER_TICK_EVENT = pygame.USEREVENT + 4
GAME_BACKGROUND = pygame.image.load(os.path.join("/home/zach-d/Documents/Programming-Projects/Programing-Club-Projects/My Space Shooter Game/Assets", "Images", "GameBackground.png"))

# Main game loop
class GameWindow():
	def __init__(self, window_size: tuple, background_image: pygame.Surface, name: str, FPS: int, timer_amount: int, default_timer_amount: int):
		self.game_window = pygame.display.set_mode(window_size)
		self.BG = pygame.transform.scale(background_image, window_size)
		self.frames_per_second = FPS
		pygame.display.set_caption(name)
		self.player_group = pygame.sprite.Group()
		self.enemy_group = pygame.sprite.Group()
		self.player = Player(os.path.join("/home/zach-d/Documents/Programming-Projects/Programing-Club-Projects/My Space Shooter Game/Assets", "Images", "Playership.png"), (150, 150), 9, 590, (85, 560), os.path.join("/home/zach-d/Documents/Programming-Projects/Programing-Club-Projects/My Space Shooter Game/Assets", "Images", "laserBlue01.png"), 50, self.enemy_group, 50, self.game_window, os.path.join("/home/zach-d/Documents/Programming-Projects/Programing-Club-Projects/My Space Shooter Game/Assets", "Sounds", "laserShoot.wav"), os.path.join("/home/zach-d/Documents/Programming-Projects/Programing-Club-Projects/My Space Shooter Game/Assets", "Sounds", "hitHurt.wav"))
		self.player_group.add(self.player)
		self.score = 0
		self.round_timer_amount = timer_amount
		self.default_timer_amount = default_timer_amount
		self.text_display = score_controller.ScoreController(self.game_window, os.path.join("/home/zach-d/Documents/Programming-Projects/Programing-Club-Projects/My Space Shooter Game/Assets", "Fonts", "Nulshock Bd.otf"), (255, 255, 255), 50)
		
	# the main run function
	def run(self):
		pygame.time.set_timer(ENEMY_SPAWN_EVENT, 2000)
		pygame.time.set_timer(TIMER_TICK_EVENT, 1000)
		running = True
		self.game_over = False
		self.game_win = False
		clock = pygame.time.Clock()
		while running:
			clock.tick(self.frames_per_second)
			for game_event in pygame.event.get():
				# checking to see if player has pressed the close button
				if game_event.type == pygame.QUIT:
					running = False
					break
				if game_event.type == player_controller.PLAYER_DIED:
					self.game_over = True
					self.player.set_movement(False)
					for enemy in self.enemy_group.sprites():
						enemy.kill()
				if self.round_timer_amount == 0 and not game_event.type == player_controller.PLAYER_DIED:
					self.game_win = True
					self.player.set_movement(False)
					for enemy in self.enemy_group.sprites():
						enemy.kill()
				
				if game_event.type == TIMER_TICK_EVENT and self.game_over != True and self.game_win != True:
					self.round_timer_amount -= 1
				
				if game_event.type == ENEMY_SPAWN_EVENT and self.game_over != True and self.game_win != True:
					y = random.randint(174, 931)
					new_enemy = enemy_controller.Enemy(os.path.join("/home/zach-d/Documents/Programming-Projects/Programing-Club-Projects/My Space Shooter Game/Assets", "Images", "enemyBlack3.png"), (120, 120), 7, (1900, y))
					self.enemy_group.add(new_enemy)
				if game_event.type == laser_controller.LASER_HIT and self.game_over != True and self.game_win != True:
					self.score += 1
				if pygame.key.get_pressed()[pygame.K_SPACE] == True and self.game_over == True:
					self.reset_game()
					self.player.set_movement(True)
				elif pygame.key.get_pressed()[pygame.K_SPACE] == True and self.game_win == True:
					self.reset_game()
					self.player.set_movement(True)
				
			self.game_window.blit(self.BG, (0, 0))
			self.player.laser_group.draw(self.game_window) 
			self.player_group.draw(self.game_window)
			self.enemy_group.draw(self.game_window)
			self.text_display.draw_as_text("Score: ", self.score, (6, 0))
			self.text_display.draw_as_text("Player Health: ",  self.player.health, (6, 67))
			self.text_display.draw_message("Time: " + time.strftime("%M:%S", time.gmtime(float(self.round_timer_amount))), (760, 20), (255, 255, 255), 50)
			if self.game_over == True:
				self.text_display.draw_message("GAME OVER", (580, 300), (255, 0, 0), 120)
				self.text_display.draw_as_text("Your score was: ", self.score, (550, 450))
				self.text_display.draw_message("Press the space key to play agian!", (550, 500), (255, 255, 255), 50)
			elif self.game_win == True:
				self.text_display.draw_message("YOU WIN", (580, 300), (0, 255, 0), 120)
				self.text_display.draw_as_text("Your score was: ", self.score, (550, 450))
				self.text_display.draw_message("Press the space key to play agian!", (550, 500), (255, 255, 255), 50)
			pygame.display.update()
			self.enemy_group.update()
			self.player_group.update()
			self.player.laser_group.update()
	pygame.quit()
	
	def reset_game(self):
		print("reseting game")
		self.game_over = False
		self.game_win = False
		self.score = 0
		self.player.reset_health()
		self.round_timer_amount = self.default_timer_amount


# making sure that is isn't reimported
if __name__ == "__main__":
	game = GameWindow((1900, 1100), GAME_BACKGROUND, "Supa Space Shoota", 30, 120, 120)
	game.run()
