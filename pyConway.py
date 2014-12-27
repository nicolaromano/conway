import sys, pygame, random, time
from math import sin

pygame.init()

class Conway:
	"""A simple class for generating a Conway's game of life cellular automaton """
	
	def __init__(self, numsquares=30, winsize=600, border=60):
		"""" Init the class members, set up the pygame window and zero the board """
		self.winsize = winsize # Size of the window
		self.numsquares = numsquares # Number of squares for the cells to live within
		self.border = border # Border from the edge of the window to the grid
		# Create the pygame window
		self.window = pygame.display.set_mode([self.winsize, self.winsize])
		self.squaresize = (self.winsize-self.border*2)/self.numsquares
		self.board = [[0 for col in range(self.numsquares)] for row in range(self.numsquares)]

	def initBoard(self, percent=0.1):
		"""" Randomly fills the board with cells. Percent is the percent of the board occupied by cells """
		self.board = [[0 if random.random()>percent else 1 for col in range(self.numsquares)] for row in range(self.numsquares)]

	def drawGrid(self):
		""" Draws the current state of the grid """
		self.window.fill(0)
		for x in range (self.border, self.winsize-self.border+1, self.squaresize):
			pygame.draw.line(self.window, (50, 50, 50), (x, self.border), (x, self.winsize-self.border))

		for y in range (self.border, self.winsize-self.border+1, self.squaresize):
			pygame.draw.line(self.window, (50, 50, 50), (self.border, y), (self.winsize-self.border, y))
		
		for x in range(self.numsquares):
			for y in range(self.numsquares):
				if self.board[x][y] == 1:
					r = pygame.Rect(self.border+x*self.squaresize, self.border+y*self.squaresize, self.squaresize, self.squaresize)
					pygame.draw.rect(self.window, (255, 0, 0), r)
	
		pygame.display.flip()
	
	def nextStep(self):
		""" Advances one time point
		See Conway's game of life rules here: http://en.wikipedia.org/wiki/Conway%27s_Game_of_Life#Rules
		Essentially, we only need to know who lives/is born in the new generation, the rest dies/stays dead
		by default (newBoard is initialized to 0)
		"""
		
		newBoard = [[0 for col in range(self.numsquares)] for row in range(self.numsquares)]

		for x in range(self.numsquares):
			for y in range(self.numsquares):
				neighCount = self.countNeighbours(x,y)
				
				# Alive cell with 2 or 3 neighbours, stays alive or
				# Dead cell with exactly 3 neighbours, born by reproduction
				if ((self.board[x][y] == 1 and (neighCount == 2 or neighCount == 3)) or (self.board[x][y] == 0 and neighCount == 3)):
					newBoard[x][y] = 1
		self.board = newBoard
		
	def countNeighbours(self, x, y):
		res = 0
		# Upper row
		if (y > 0):
			res = res + self.board[x][y-1]
			if (x > 0):
				res = res + self.board[x-1][y-1]
			if (x < (self.numsquares-1)):
				res = res + self.board[x+1][y-1]
		# Cell's row
		if (x > 0):
			res = res + self.board[x-1][y]
		if (x < (self.numsquares-1)):
			res = res + self.board[x+1][y]
		# Lower row
		if (y < (self.numsquares-1)):
			res = res + self.board[x][y+1]
			if (x > 0):
				res = res + self.board[x-1][y+1]
			if (x < (self.numsquares-1)):
				res = res + self.board[x+1][y+1]
		return res

conway = Conway(120)
conway.initBoard(0.1)

while True: 
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit(0)
	conway.drawGrid()
	time.sleep(.1)
	conway.nextStep()
	pygame.time.Clock().tick(60)
