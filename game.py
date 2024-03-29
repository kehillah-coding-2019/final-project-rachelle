
import internalboard, graphics
import pygame

class InvalidDimensions(Exception):
	""" an error for dimensions that are too big """
	pass


class Button:
	pass

	def __init__(self, text, func, graphics, state):

		self.text = text
		self.func = func
		self.graphics = graphics

		self.states = {'up': (215, 215, 215), 'hover': (200, 200, 200), 'down': ((170, 170, 170))}
		self.set_state(state)

		self.x = 0
		self.y = 0
		self.height = 0
		self.width = 0
		self.rect = None


	def set_state(self, state):
		""" changes the state"""
		self.state = state
		self.color = self.states[self.state]

	def draw(self):
		""" draws button on screen """
		return self.graphics.draw_button(self)

	def hover(self):
		""" changes button when hovering """
		self.set_state('hover')
		return self.draw()

	def unhover(self):
		""" changes button when not hovering """
		self.set_state('up')
		return self.draw()

	def press(self):
		""" does function and changes button """
		self.set_state('down')
		return self.draw()

	def unpress(self):
		""" changes button when unpress """
		self.set_state('up')
		return self.draw()


class Game:

	def __init__(self, pixels, size):

		if size < 4 or size > 9:
			raise InvalidDimensions

		self.pixels = pixels
		self.size = size

		self.graphics = graphics.Graphics(self.size, self.pixels)
		self.board = internalboard.Board(self.size)

		self.selectedr = None
		self.selectedc = None
		self.selected_cell = None

		self.buttons = [Button('Check', self.check, self.graphics, 'up'), Button('Reveal', self.reveal, self.graphics, 'up'), Button('Solve', self.solve, self.graphics, 'up'), Button('Reset', self.reset, self.graphics, 'up'), Button('New', self.new, self.graphics, 'up')]
		self.button_width = (self.graphics.cell_size * 1.5) - self.graphics.cell_size/4
		self.button_height = self.button_width/2
		print(self.button_height)
		
		self.add_buttons()

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

		for button in self.buttons:
			button.draw()

		pygame.display.update()

	def add_buttons(self):
		""" adds buttons """
		border = self.graphics.cell_size/2
		puzzle_size = self.graphics.cell_size*self.size
		buttons_space = len(self.buttons)*self.button_height
		for i in range(len(self.buttons)):
			button = self.buttons[i]
			button.x = self.pixels-(self.graphics.cell_size/2) + (self.graphics.cell_size/10)
			button.y = border + (i*(self.button_height + (self.button_height/6)))
			button.width = self.button_width
			button.height = self.button_height
			button.rect = pygame.Rect(button.x, button.y, button.width, button.height)

	def select(self, r, c):
		""" select """
		surfaces = []
		if self.selectedr != None:
			cell = self.board.cells[self.selectedr][self.selectedc]
			cell.color = (255, 255, 255)
			surfaces.append(self.graphics.update_cell(cell))
		self.selectedr = r
		self.selectedc = c
		cell = self.board.cells[r][c]
		self.selected_cell = cell
		cell.color = (215, 215, 215)
		surfaces.append(self.graphics.update_cell(cell))
		return surfaces

	def unselect(self):
		""" unselect """
		surface = None
		if self.selectedr != None:
			cell = self.board.cells[self.selectedr][self.selectedc]
			cell.color = (255, 255, 255)
			surface = self.graphics.update_cell(cell)
		self.selectedr = None
		self.selectedc = None
		self.selected_cell = None
		return surface


	def insert_num(self, num, cell):
		""" insert a num """
		cell.inserted = num
		self.board.input[cell.r][cell.c] = num
		return self.graphics.update_cell(cell)

	def del_num(self, cell):
		""" delete a number """
		cell.inserted = 0
		self.board.input[cell.r][cell.c] = 'x'
		return self.graphics.update_cell(cell)


	def add_note(self, cell, num):
		""" add a note """
		cell.notes.append(num)
		cell.notes.sort()
		return self.graphics.update_cell(cell)

	def del_note(self, cell, num):
		""" delete a note """
		cell.notes.remove(num)
		return self.graphics.update_cell(cell)

	def clear_notes(self, cell):
		""" clear a note """
		cell.notes = []
		return self.graphics.update_cell(cell)

	def check(self):
		""" check to see if the answer is right """
		pass

	def reveal(self):
		""" reveal selected cell """
		pass

	def solve(self):
		""" show the solution """
		pass

	def reset(self):
		""" reset the puzzle """
		pass

	def new(self):
		""" start a new puzzle """
		pass

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
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
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

				# clicking
				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

					# selecting cells
					done = False
					for r in range(self.size):
						for c in range(self.size):
							if self.board.cells[r][c].rect.collidepoint(event.pos[0], event.pos[1]):
								done = True
								rects.extend(self.select(r, c))
								break

					# pressing buttons
					for button in self.buttons:
						if button.rect.collidepoint(event.pos):
							done = True
							rects.append(button.press())
							break

					if not done:
						rects.append(self.unselect())

				# insert/delete number
				if event.type == pygame.KEYDOWN and event.key in self.keys and self.keys[event.key] <= self.size:
					num = self.keys[event.key]
					if pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]:

						if num in self.selected_cell.notes:
							rects.append(self.del_note(self.selected_cell, num))
						else:
							rects.append(self.add_note(self.selected_cell, num))

					else:
						if self.selected_cell.inserted != num:
							rects.append(self.insert_num(num, self.selected_cell))
						else:
							rects.append(self.del_num(self.selected_cell))

				if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
					if self.selected_cell.inserted == 0:
						rects.append(self.clear_notes(self.selected_cell))
					else:
						rects.append(self.del_num(self.selected_cell))


				# buttons

				# button hovering
				if event.type == pygame.MOUSEMOTION and not pygame.mouse.get_pressed()[0]:
					for button in self.buttons:
						if button.rect.collidepoint(event.pos):
							rects.append(button.hover())
						else:
							rects.append(button.unhover())

				# button unpress
				if event.type == pygame.MOUSEBUTTONUP:
					for button in self.buttons:
						if button.rect.collidepoint(event.pos):
							rects.append(button.unpress())


			self.clock.tick(40)

			if rects != []:
				#print() # the only way the program will run fast
				pygame.display.update(rects)

