
import pygame
from random import randint, choice

def sub(l):
	""" subtract first of l by second """
	if len(l) == 2:
		return abs(l[0] - l[1])

def mult(l):
	""" multiply numbers together """
	product = 1
	for item in l:
		product *= item
	return product

def div(l):
	""" divide n1 by n2 """
	if len(l) == 2:
		if l[0] >= l[1]:
			if l[0] % l[1] == 0:
				return int(l[0]/l[1])
		else:
			if l[1] % l[0] == 0:
				return int(l[1]/l[0])

class Cell:

	def __init__(self, coords, number, group, graphic):
		""" example: Cell((1, 3), 4, 2, '1100') """

		self.r = coords[0]
		self.c = coords[1]
		self.number = number
		self.group = group
		self.graphic = graphic

		self.inserted = 0
		self.notes = []

		self.color = (255, 255, 255)
		self.rect = None
		self.label = None


class Board:

	def __init__(self, dimensions, operations=[(sum, '+'), (sub, '-'), (mult, 'x'), (div, '÷')]):
		""" example: Board(9) """

		self.dimensions = dimensions

		self.number_grid = numGrid(self.dimensions)
		func = groupGrid(self.number_grid)
		self.group_grid = func[0]
		self.by_num = func[1]
		self.in_group = func[2]
		self.group_key = groupKey(self.by_num, operations)

		self.tops = []
		for l in self.in_group:
			self.tops.append(l[0])

		self.cells = []
		for r in range(dimensions):
			self.cells.append([])
			for c in range(dimensions):
				self.cells[r].append(Cell((r, c), self.number_grid[r][c], self.group_grid[r][c], get_graphic(r, c, self.group_grid)))

		self.input = []
		for row in range(self.dimensions):
			self.input.append([])
			for column in range(self.dimensions):
				self.input[row].append('x')



def numGrid(dimensions):
	""" return a grid with no number repeating in each column or row """

	number_grid = []
	for i in range(dimensions):
		number_grid.append([])

	for r in range(dimensions):

		exit = False
		while not exit:

			possibilities = list(range(1, dimensions+1))
			exclude = []

			for column in range(dimensions):

				possibilities.extend(exclude)

				exclude = []
				for row in number_grid[:r]:
					if row[column] in possibilities:
						exclude.append(row[column])
						possibilities.remove(row[column])
				
				if len(possibilities) != 0:
					number_grid[r].append(possibilities.pop(randint(0, len(possibilities)-1)))
					if len(number_grid[r]) == dimensions:
						exit = True
				else:
					number_grid[r] = []
					break

	return number_grid


def getOptions(r, c, group_grid):
	""" return the surrounding cell coordinates that are available """

	options = []

	if r > 0:
		if group_grid[r-1][c] == 'x':
			options.append((r-1, c))
	if r < len(group_grid)-1:
		if group_grid[r+1][c] == 'x':
			options.append((r+1, c))
	if c > 0:
		if group_grid[r][c-1] == 'x':
			options.append((r, c-1))
	if c < len(group_grid)-1:
		if group_grid[r][c+1] == 'x':
			options.append((r, c+1))

	return options


def groupGrid(number_grid):
	""" return a grid of groups """

	dimensions = len(number_grid)

	group_grid = []
	for i in range(dimensions):
		group_grid.append([])
		for j in range(dimensions):
			group_grid[i].append('x')

	by_num = []
	in_group = []
	num = -1
	for r in range(dimensions):
		for c in range(dimensions):
			
			if group_grid[r][c] == 'x':

				num += 1
				in_group.append([])
				by_num.append([])
				R = r
				C = c

				for i in range(4):
					group_grid[R][C] = num
					in_group[num].append((R, C))
					by_num[num].append(number_grid[R][C])
					#options = getOptions(R, C, group_grid)
					options = []
					for coords in in_group[num]:
						options.extend(getOptions(coords[0], coords[1], group_grid))
					if [] != options:
						coords = choice(options)
						R = coords[0]
						C = coords[1]
						if i == 1:
							if randint(0, 1) == 0:
								break
						elif i == 2:
							if randint(0, 15) != 0:
								break
					else:
						break

	return group_grid, by_num, in_group


def groupKey(by_num, operations):
	""" figure out arithmetic solutions """

	gk = []

	for group in by_num:
		key = None
		while key == None:
			op = choice(operations)
			key = op[0](group)
		gk.append([op[1], key, None])

	return gk


def get_graphic(r, c, group_grid):
	""" get the graphic code for a cell """
	
	code = ''

	if r > 0 and group_grid[r-1][c] == group_grid[r][c]:
		code += '0'
	else:
		code += '1'
	if c < len(group_grid)-1 and group_grid[r][c+1] == group_grid[r][c]:
		code += '0'
	else:
		code += '1'
	if r < len(group_grid)-1 and group_grid[r+1][c] == group_grid[r][c]:
		code += '0'
	else:
		code += '1'
	if c > 0 and group_grid[r][c-1] == group_grid[r][c]:
		code += '0'
	else:
		code += '1'

	return code + '.png'


