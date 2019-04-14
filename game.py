
import internalboard, graphics
import pygame

class Game:

	def __init__(self, pixels, size):

		self.pixels = pixels
		self.size = size

		self.graphics = graphics.Graphics(self.size, self.pixels)
		self.board = internalboard.Board(self.size)

		self.selectedr = None
		self.selectedc = None

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
		if self.selectedr != None:
			cell = self.board.cells[self.selectedr][self.selectedc]
			surfaces.append(self.graphics.unselect(cell))
		self.selectedr = r
		self.selectedc = c
		cell = self.board.cells[r][c]
		surfaces.append(self.graphics.select(cell))
		return surfaces


	def game_loop(self):
		""" goes through each event and does stuff """
		exit = False
		while not exit:
			for event in pygame.event.get():

				# quit
				if event.type == pygame.QUIT:
					exit = True
				if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					exit = True

				# keyboard arrows
				if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
					if self.selectedc+1 < self.size:
						self.select(self.selectedr, self.selectedc+1)
				if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
					if self.selectedc > 0:
						self.select(self.selectedr, self.selectedc-1)
				if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
					if self.selectedr > 0:
						self.select(self.selectedr-1, self.selectedc)
				if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
					if self.selectedr+1 < self.size:
						self.select(self.selectedr+1, self.selectedc)

			pygame.display.update()

