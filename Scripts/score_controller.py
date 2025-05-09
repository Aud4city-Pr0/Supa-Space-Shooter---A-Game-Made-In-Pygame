# The UI Controller
import pygame
from pygame import font
#UI controller class
class ScoreController():
	def __init__(self, game_display: pygame.Surface, text_font: str, text_color: tuple, text_size: int):
		# Score conrtoller setup
		font.init()
		self.game_display = game_display
		self.font_name = text_font
		self.font = font.Font(text_font, text_size)
		self.color = text_color
		
	def draw_as_text(self, msg: str, value_to_display, position: tuple):
		# draws a message and a value as text
		RENDERD_FONT = self.font.render(msg + str(value_to_display), True, self.color)
		self.game_display.blit(RENDERD_FONT, position)
		
	def draw_message(self, msg: str, position: tuple, color: tuple, size: int):
		#draws a message
		MESSAGE_FONT = font.Font(self.font_name, size)
		RENDERD_FONT = MESSAGE_FONT.render(msg, True, color)
		self.game_display.blit(RENDERD_FONT, position)
		
