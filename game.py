
import internalboard, display
import pygame

class Game:

	def __init__(pixels, size):

		self.pixels = pixels
		self.size = size

		self.display = display.Display()
		self.board = internalboard.Board(self.size)

		self.set_up()

		self.game_loop()


	def set_up(self):
		""" sets up the board """
		pass


	def game_loop(self):
		""" goes through each event and does stuff """
		exit = False
		while not exit:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit = True
				if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					exit = True

			pygame.display.update()