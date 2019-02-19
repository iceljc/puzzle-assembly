
from queue import PriorityQueue
from colored import fg, bg, attr
import numpy as np



# define puzzle piece
class Piece:
  def __init__(self, pid, color, unit_list):
  	self.id = pid
  	self.color = color
  	self.unit_list = unit_list
  	self.unit_count = len(unit_list)
  	self.unit_xsize = max(p[0] for p in self.unit_list) + 1
  	self.unit_ysize = max(p[1] for p in self.unit_list) + 1
  
  """
  		adjust the local coordinates of the puzzle piece
  """
  def zeroup(self):
    xmin = min(p[0] for p in self.unit_list)
    ymin = min(p[1] for p in self.unit_list)
    if min([xmin, ymin, 0]) != 0:
      if xmin < ymin:
        self.unit_list = [[t[0] - xmin, t[1]] for t in self.unit_list]
      else:
        self.unit_list = [[t[0], t[1] - ymin] for t in self.unit_list]

  """
  		rotate 90 degrees clockwise
  """
  def rotate90(self):
    for i, item in enumerate(self.unit_list):
      x = item[0]
      y = item[1]
      self.unit_list[i][0] = y
      self.unit_list[i][1] = -1 * x
    self.zeroup()
  
  """
  		rotate 90 degrees counter-clockwise
  """
  def counterRotate90(self):
    for i, item in enumerate(self.unit_list):
      x = item[0]
      y = item[1]
      self.unit_list[i][0] = -1 * y
      self.unit_list[i][1] = x
    self.zeroup()

  """
  		rotate a puzzle piece several turns
  """
  def rotate(self, turns):
    if turns > 0:
      for i in range(turns):
        self.rotate90()
    elif turns < 0:
      turns = turns * -1
      for i in range(turns):
        self.counterRotate90()
    else:
      self
    return self



# define board
class Board:

	def __init__(self, board=None, board_size=None, moves=0):

		if board is None:
			self.board = np.ones((7,7), dtype=int)
			# [[1 for i in range(7)] for j in range(7)]
			self.board_size = 7
		else:
			self.board = board
			self.board_size = board_size
		self.hole = Piece(0, 'black', [[0,0]])
		self.moves = moves
		# self.previous = previous
		# self.placed_puzzle = [] 

	def isGoal(self):
		"""
			check if the current board is the goal.
		"""
		for i in range(self.board_size):
			for j in range(self.board_size):
				if not isinstance(self.board[i][j], tuple):
					return False
		return True

	def placePiece(self, piece, location):
		"""
			place a puzzle piece at a given location.
		"""
		if self.withinBoard(piece, location) and self.isFit(piece, location):
			for unit in piece.unit_list:
				self.board[location[0]+unit[0]][location[1]+unit[1]] = (piece.id, piece.color)
			# self.placed_puzzle.append(piece.id)

	
	def removePiece(self, piece):
		"""
			remove a puzzle piece at a given location.
		"""
		for x in range(self.board_size):
			for y in range(self.board_size):
				if self.board[x][y] == (piece.id, piece.color):
					self.board[x][y] = 1


	def isFit(self, piece, location):
		"""
			check if the piece can be placed on the board without overlapping.
		"""
		for unit in piece.unit_list:
			if self.board[location[0]+unit[0]][location[1]+unit[1]] != 1:
				return False
		return True

	def withinBoundary(self, x, y):
  		return x >= 0 and x < self.board_size and y >=0 and y < self.board_size

	def withinBoard(self, piece, location):
		"""
			check if the piece is placed within the board boundary.
		"""
		for unit in piece.unit_list:
			if not self.withinBoundary(location[0]+unit[0],location[1]+unit[1]):
				return False
		return True
	


	def clone(self):
		"""
			returns copy of the current board
		"""
		return Board(self.board.copy(), self.board_size, self.moves+1)


	def neighbours(self, pieces):
		return


	def queue_entry(self, count):
		return (self.moves, count, self)

	def __eq__(self, other):
		"""
            check if self == other
        """
		if other is None:
			return False
		else:
			return self.board == other.board

	# def get_previous_states(self):
	# 	"""
 #            return a list of previous states by going up the state space tree
 #        """
	# 	states = [self]
	# 	prev = self.previous

	# 	while prev is not None:
	# 		states.append(prev)
	# 		prev = prev.previous

	# 	# states.reverse()
		
	# 	return states

	


def dfs_solver(board, pieces, piece_id):
	if board.isGoal():
		return True
	piece = pieces[piece_id - 1]
	xb = piece.unit_xsize
	yb = piece.unit_ysize
	for x in range(board.board_size - xb + 1):
		for y in range(board.board_size - yb + 1):
			loc = [x, y]
			r = 0
			while r < 4:
				if board.withinBoard(piece, loc) and board.isFit(piece, loc):
					board.placePiece(piece, loc)
					if dfs_solver(board, pieces, piece_id + 1):
						return True
					else:
						# cannot place next piece, so remove the current one and try other configuration
						board.removePiece(piece)
						piece.rotate90()
						r += 1
				else:
					piece.rotate90()
					r += 1
					
	return False



def plot_board(board):
	for line in board:
		for item in line:
			if isinstance(item, tuple):
				(block, color) = item
				print('%s%s%i%s' % (fg(color), bg(color), block, attr('reset')), end='')
			else:
				print('%s%s %s' % (fg('white'), bg('white'), attr('reset')), end='')
		print(' ')



if __name__ == '__main__':

	##########################################################
	"""
			test case on a 4x4 board with 4 pieces.
	"""

	if 1:
		pieces = [Piece(1, 'green', [[0,1], [1,1], [1,0]]),
			Piece(2, 'red', [[0,0], [0,1], [1,1], [2,1]]),
			Piece(3, 'blue', [[0,1], [0,2], [1,0], [1,1]]),
			Piece(4, 'gold_1', [[0,1], [1,0], [1,1], [1,2]])
			]

		board = [[1 for i in range(4)] for j in range(4)]
		board_size = 4
		hole_pos = [3,0]
		# initialize a board
		init_board = Board(board=board, board_size=board_size)
		# set a hole on the board
		init_board.placePiece(init_board.hole, hole_pos)

		dfs_solver(init_board, pieces, 1)
		if init_board.isGoal():
			print("solution found !")
		else:
			print("no solution ...")

		plot_board(init_board.board)
	

	##########################################################

	"""
			test case on a 7x7 board with 9 pieces.
	"""

	if 0:
		# initialize a board
		init_board = Board()

		# hole location
		Holes = [[0,0], [0,3], [1,0], [1,4], [1,5], [3,2], [3,3], [4,1], [4,4], [4,6], [5,3], [6,0], [6,4], [6,5]]

		pieces = [
				Piece(1, 'green', [[0,1], [0,2], [1,0], [1,1], [1,2], [2,1], [2,2], [2,3]]),
				Piece(2, 'red', [[0,0], [0,1], [1,0], [1,1], [2,0], [2,1], [1,2]]),
				Piece(3, 'purple_1a', [[0,0], [1,0], [1,1], [2,0], [2,1], [2,2]]),
				Piece(4, 'orange_red_1', [[0,1], [1,0], [1,1], [2,0], [2,1], [3,1]]),
				Piece(5, 'gold_1', [[0,0], [0,1], [1,1], [1,2], [2,2]]),
				Piece(6, 'blue', [[0,0], [0,1], [0,2], [0,3],[1,2]]),
				Piece(7, 'dark_cyan', [[0,0], [1,0], [2,0], [3,0], [4,0]]),
				Piece(8, 'magenta', [[0,1], [1,0], [1,1], [1,2]]),
				Piece(9, 'dark_orange', [[0,0], [1,0]])
			]

		# set a hole on the board
		init_board.placePiece(init_board.hole, Holes[11])

		dfs_solver(init_board, pieces, 1)
		if init_board.isGoal():
			print("solution found !")
		else:
			print("no solution ...")

		plot_board(init_board.board)


	







