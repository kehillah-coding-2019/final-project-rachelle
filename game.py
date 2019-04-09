
import pygame
import internalboard

class Game:

	def __init__(self, pixels, size):

		self.pixels = pixels
		self.size = size
		self.graphic_board = []
		self.images = {}
		self.cell_size = int(self.pixels/(self.size+1))

		self.surface = pygame.display.set_mode((pixels, pixels))
		pygame.display.set_caption('KenKen')

		self.board = internalboard.Board(size)

		self.clear()
		self.make_board()

		pygame.display.flip()

		self.game_loop()


	def clear(self):
		""" clear screen """
		self.surface.fill((255, 255, 255))


	def make_board(self):
		""" make board """

		# get all names of images
		string_images = []
		for a in ['0', '1']:
			for b in ['0', '1']:
				for c in ['0', '1']:
					for d in ['0', '1']:
						string_images.append(a+b+c+d+'.png')

		# get all images in pygame
		for i in string_images:
			image = pygame.image.load(i)
			self.images[i] = pygame.transform.scale(image, (self.cell_size, self.cell_size))

		for r in range(len(self.board.cells)):
			for c in range(len(self.board.cells[r])):
				cell = self.board.cells[r][c]
				cell.surface = self.make_cell(cell)
				self.label_cell(cell)


	def make_cell(self, cell):
		""" make cell """
		return self.surface.blit(self.images[cell.graphic], (cell.c*self.cell_size+self.cell_size/2, cell.r*self.cell_size+self.cell_size/2))

	def label_cell(self, cell):
		""" give cell operation label """
		pass


	def game_loop(self):
		exit = False
		while not exit:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit = True
				if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					exit = True

			pygame.display.update()

