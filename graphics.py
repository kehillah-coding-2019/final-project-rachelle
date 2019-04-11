
import pygame
import internalboard

class Graphics:

	def __init__(self, size, pixels):

		self.size = size
		self.pixels = pixels

		self.cell_size = int(self.pixels/(self.size+1))
		self.images = self.get_images()

		self.surface = pygame.display.set_mode((self.pixels, self.pixels))
		pygame.display.set_caption('Ken Ken')


	def get_images(self):
		""" make a dictionary of images with their names and their scaled versions on python """

		# get all names of images
		string_images = []
		for a in ['0', '1']:
			for b in ['0', '1']:
				for c in ['0', '1']:
					for d in ['0', '1']:
						string_images.append(a+b+c+d+'.png')

		# get all images in pygame
		images = {}
		for i in string_images:
			image = pygame.image.load(i)
			images[i] = pygame.transform.scale(image, (self.cell_size, self.cell_size))
		return images


	def clear(self):
		""" clear screen """
		self.surface.fill((255, 255, 255))


	def make_board(self, board):
		""" make board """
		for r in range(len(board.cells)):
			for c in range(len(board.cells[r])):
				cell = board.cells[r][c]
				cell.surface = self.make_cell(cell)


	def get_cell_x(self, cell):
		""" return the x of a cell """
		return cell.c*self.cell_size+self.cell_size/2

	def get_cell_y(self, cell):
		""" return the y of a cell """
		return cell.r*self.cell_size+self.cell_size/2

	def make_cell(self, cell):
		""" make cell """
		return self.surface.blit(self.images[cell.graphic], (self.get_cell_x(cell), self.get_cell_y(cell)))


	def label_cell(self, cell):
		""" give cell operation label """
		# return pygame.font.Font.render(' '.join(self.board.group_key[cell.r][cell.c]))

