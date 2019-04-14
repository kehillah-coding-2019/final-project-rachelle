
import pygame
import internalboard

class Graphics:

	def __init__(self, size, pixels):

		self.size = size
		self.pixels = pixels

		self.cell_size = int(self.pixels/(self.size+1))
		self.label_size = int(self.cell_size/3)

		self.images = self.get_images()

		self.surface = pygame.display.set_mode((self.pixels, self.pixels))
		pygame.display.set_caption('Ken Ken')


	def unselect(self, cell):
		""" redraw the cell with a white background """
		pygame.draw.rect(self.surface, (255, 255, 255), cell.rect)
		self.draw_cell(cell)

	def select(self, cell):
		""" redraw the cell with a grey background """
		pygame.draw.rect(self.surface, (215, 215, 215), cell.rect)
		self.draw_cell(cell)

	def draw_cell(self, cell):
		""" draw the cell """
		self.make_cell(cell)
		if cell.label != None:
			self.label_corner(cell)


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
				cell.rect = self.make_cell(cell)


	def get_cell_x(self, cell):
		""" return the x of a cell """
		return cell.c*self.cell_size+self.cell_size/2

	def get_cell_y(self, cell):
		""" return the y of a cell """
		return cell.r*self.cell_size+self.cell_size/2

	def make_cell(self, cell):
		""" make cell """
		return self.surface.blit(self.images[cell.graphic], (self.get_cell_x(cell), self.get_cell_y(cell)))


	def setup_corner_text(self, board):
		""" make text for a group """
		for r in range(board.dimensions):
			for c in range(board.dimensions):
				group = board.group_grid[r][c]
				if (r, c) in board.tops:
					cell = board.cells[r][c]
					if len(board.by_num[group]) != 1:
						cell.label = self.text('arial', self.label_size, str(board.group_key[group][1]) + board.group_key[group][0])
					else:
						cell.label = self.text('arial', self.label_size, str(board.group_key[group][1]))
					board.group_key[group][2] = cell.label
					self.label_corner(cell)


	def label_corner(self, cell):
		""" puts text on the board corner """
		return self.insert_text(cell.label, (cell.rect.left+self.cell_size/14, cell.rect.top+self.cell_size/14))

	def insert_text(self, text, coords):
		""" blit text on screen """
		return self.surface.blit(text, coords)

	def text(self, fontname, size, text, bold=False, italic=False):
		""" give cell operation label """
		thefont = pygame.font.SysFont(fontname, size)
		return thefont.render(text, True, (0, 0, 0))

