
import pygame
import internalboard
import math

class Graphics:

	def __init__(self, size, pixels):

		self.size = size
		self.pixels = pixels

		self.cell_size = int(self.pixels/(self.size+1))
		self.label_size = int(self.cell_size/3.8)
		self.num_size = int(self.cell_size/1.6)
		self.note_size = int(self.cell_size/7)
		self.right_border = self.cell_size

		self.font = pygame.font.get_default_font()

		self.note_font = 'helvetica.ttc'
		self.button_font = 'Arial Black copy.ttf'

		self.images = self.get_images()
		self.numbers = self.get_numText()

		self.surface = pygame.display.set_mode((self.pixels+self.right_border, self.pixels))
		pygame.display.set_caption('Ken Ken')


	def update_cell(self, cell):
		""" update the cell bg color """
		pygame.draw.rect(self.surface, cell.color, cell.rect)
		self.draw_cell(cell)
		return cell.rect

	def draw_cell(self, cell):
		""" draw the cell """
		self.make_cell(cell)
		if cell.label != None:
			self.label_corner(cell)
		if cell.inserted != 0:
			self.insert_num(cell.inserted, cell)
		elif cell.notes != []:
			self.insert_notes(cell)


	def insert_num(self, num, cell):
		""" insert a number into a cell """
		text = self.numbers['num'][num-1]
		return self.insert_text(text, ((cell.rect.width/2-text.get_rect().width/2)+cell.rect.x, (cell.rect.height/2-text.get_rect().height/2.6)+cell.rect.y))

	def coordinatify(self, num, center):
		""" take a number like 0 or -2 and make it a coordinate for a note """
		return (num*self.label_size/6)*1.5 + center

	def insert_notes(self, cell):
		""" inserts notes """

		# arrange data for formatting
		rows = [] # ex. [{1: [-2, -1] 4: [0, -1], 5: [2, -1]}, {6: [-1, 1], 8: [1, 1]}]
		for i in range(len(cell.notes)):
			if i % 3 == 0:
				rows.append({})
			rows[-1][cell.notes[i]] = []

		# get columns
		center = cell.rect.centerx
		for row in rows:
			i = -1
			for note in row:
				i += 1
				if i == 0:
					if len(row) == 1:
						row[note].append(self.coordinatify(0, center))
					elif len(row) == 2:
						row[note].append(self.coordinatify(-1, center))
					elif len(row) == 3:
						row[note].append(self.coordinatify(-2, center))
				elif i == 1:
					if len(row) == 2:
						row[note].append(self.coordinatify(1, center))
					elif len(row) == 3:
						row[note].append(self.coordinatify(0, center))
				elif i == 2:
					row[note].append(self.coordinatify(2, center))


		# get rows
		center = cell.rect.centery
		for r in range(len(rows)):
			if r == 0:
				for note in rows[r]:
					rows[r][note].append(self.coordinatify(-1*(len(rows)-1), center))
			elif r == 1:
				if len(rows) == 2:
					for note in rows[r]:
						rows[r][note].append(self.coordinatify(1, center))
				elif len(rows) == 3:
					for note in rows[r]:
						rows[r][note].append(self.coordinatify(0, center))
			elif r == 2:
				for note in rows[r]:
					rows[r][note].append(self.coordinatify(2, center))

		for row in rows:
			for note in row:
				self.insert_text(self.numbers['note'][note-1], (row[note][0], row[note][1]))


	def get_numText(self):
		""" make a dictionary of numbers """
		numbers = {'num': [], 'note': []}
		for n in range(1, self.size+1):
			numbers['num'].append(self.text(self.font, self.num_size, str(n)))
		for n in range(1, self.size+1):
			numbers['note'].append(self.text(self.note_font, self.note_size, str(n), True))
		return numbers

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
						cell.label = self.text(self.font, self.label_size, str(board.group_key[group][1]) + board.group_key[group][0])
					else:
						cell.label = self.text(self.font, self.label_size, str(board.group_key[group][1]))
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
		thefont = pygame.font.Font(fontname, size)
		if bold:
			thefont.set_bold(True)
		if italic:
			thefont.set_italic(True)
		return thefont.render(text, True, (0, 0, 0))

	def draw_button(self, button):
		""" draw the button """
		rect = pygame.draw.rect(self.surface, button.color, button.rect)
		self.insert_text(self.text(self.button_font, int(button.height/2), button.text), (button.x + button.width/20, button.y + (button.height/10)))
		return rect

