
import pygame, game, internalboard
pygame.init()
pygame.font.init()

kgame = game.Game(750, 6)

pygame.font.quit()


# Structure
""" 

Game
instance variables
- pixels
- size
methods
- call setting up board
- game loop

Display
instance variables
- cell_size
- surface
- images
methods
- set up
- refresh cell
- make cell
- update text
- clear


Board
- all board information in lists

Cell
instance variables
- row
- column
- number
- group
- graphic
- inserted
- notes
- surface
- x-coord
- y-coord
methods
- make a cell

"""