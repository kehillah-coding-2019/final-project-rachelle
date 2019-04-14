
import internalboard, graphics
import pygame

class Game:

	def __init__(self, pixels, size):

		self.pixels = pixels
		self.size = size

		self.graphics = graphics.Graphics(self.size, self.pixels)
		self.board = internalboard.Board(self.size)

		self.selected = None # will be a Cell

		self.set_up()
		self.game_loop()


	def set_up(self):
		""" sets up the board """
		self.graphics.clear()
		self.graphics.make_board(self.board)
		self.graphics.setup_corner_text(self.board)
		self.select(0, 0)


	def select(self, r, c):
		surfaces = []
		if self.selected != None:
			surfaces.append(self.graphics.unselect(self.selected))
		self.selected = self.board.cells[r][c]
		surfaces.append(self.graphics.select(self.selected))
		return surfaces


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

