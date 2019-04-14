
import internalboard, graphics
import pygame

class InvalidDimensions(Exception):
	""" an error for dimensions that are too big or small """
	pass


class Game:

	def __init__(self, pixels, size):

		if size > 9:
			raise InvalidDimensions

		self.pixels = pixels
		self.size = size

		self.graphics = graphics.Graphics(self.size, self.pixels)
		self.board = internalboard.Board(self.size)

		self.selectedr = None
		self.selectedc = None

		self.keys = {pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3, pygame.K_4: 4, pygame.K_5: 5, pygame.K_6: 6, pygame.K_7: 7, pygame.K_8: 8, pygame.K_9: 9}

		self.clock = pygame.time.Clock()

		self.set_up()
		self.game_loop()


	def set_up(self):
		""" sets up the board """
		self.graphics.clear()
		self.graphics.make_board(self.board)
		self.graphics.setup_corner_text(self.board)
		self.select(0, 0)
		pygame.display.update()


	def select(self, r, c):
		""" select """
		surfaces = []
		if self.selectedr != None:
			cell = self.board.cells[self.selectedr][self.selectedc]
			surfaces.append(self.graphics.unselect(cell))
		self.selectedr = r
		self.selectedc = c
		cell = self.board.cells[r][c]
		surfaces.append(self.graphics.select(cell))
		return surfaces

	def unselect(self):
		""" unselect """
		surface = None
		if self.selectedr != None:
			cell = self.board.cells[self.selectedr][self.selectedc]
			surface = self.graphics.unselect(cell)
		self.selectedr = None
		self.selectedc = None
		return surface


	def insert_num(self, num, cell):
		""" insert a num """
		cell.inserted = num
		self.board.input[cell.r][cell.c] = num
		return self.graphics.insert_num(num, cell)


	def game_loop(self):
		""" goes through each event and does stuff """
		exit = False
		while not exit:
			rects = []
			# event loop
			for event in pygame.event.get():

				# quit
				if event.type == pygame.QUIT:
					exit = True
				if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					exit = True

				# keyboard arrows to select
				if self.selectedr != None:
					if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
						if self.selectedc+1 < self.size:
							rects.extend(self.select(self.selectedr, self.selectedc+1))
					if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
						if self.selectedc > 0:
							rects.extend(self.select(self.selectedr, self.selectedc-1))
					if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
						if self.selectedr > 0:
							rects.extend(self.select(self.selectedr-1, self.selectedc))
					if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
						if self.selectedr+1 < self.size:
							rects.extend(self.select(self.selectedr+1, self.selectedc))

				# clicking to select
				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					done = False
					for r in range(self.size):
						for c in range(self.size):
							if self.board.cells[r][c].rect.collidepoint(event.pos[0], event.pos[1]):
								done = True
								rects.extend(self.select(r, c))
								break
					if not done:
						rects.append(self.unselect())

				# insert number
				if event.type == pygame.KEYDOWN and event.key in self.keys:
					rects.append(self.insert_num(self.keys[event.key], self.board.cells[self.selectedr][self.selectedc]))

			self.clock.tick(40)
			if rects != []:
				print() # the only way the program will run fast
				pygame.display.update(rects)

