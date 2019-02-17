from colored import fg, bg, attr
import numpy as np

#make blank 7x7 block
A = [[1,1,1,1,1,1,1],
[1,1,1,1,1,1,1],
[1,1,1,1,1,1,1],
[1,1,1,1,1,1,1],
[1,1,1,1,1,1,1],
[1,1,1,1,1,1,1],
[1,1,1,1,1,1,1]]

#numbered the same as in the assignment
H = [[0,0], [0,3], [1,0], [1,4], [1,5], [3,2], [3,3], [4,1], [4,4], [4,6], [5,3], [6,0], [6,4], [6,5]]

# https://pypi.org/project/colored/ for color list
# unit list start at 0,0 top left. use coords as if the piece were encapsulated by a rectangle with that coordinate system.
class Piece:
  def __init__(self, color, unit_list):
    self.color = color
    self.unit_list = unit_list
    self.unit_count = len(unit_list)
  
  def zeroup(self):
    xmin = min(x[0] for x in self.unit_list)
    ymin = min(x[1] for x in self.unit_list)
    if min([xmin, ymin, 0]) != 0:      
      if xmin < ymin:
        self.unit_list = [[t[0] - xmin, t[1]] for t in self.unit_list]
      else:
        self.unit_list = [[t[0], t[1] - ymin] for t in self.unit_list]

  #rotate 90 degrees counterclockwise
  def rotate90(self):
    for i, item in enumerate(self.unit_list):
      x = item[0]
      y = item[1]
      self.unit_list[i][0] = y
      self.unit_list[i][1] = -1 * x
    self.zeroup()
  
  #rotate 90 degrees clockwise
  def antirotate90(self):
    for i, item in enumerate(self.unit_list):
      x = item[0]
      y = item[1]
      self.unit_list[i][0] = -1 * y
      self.unit_list[i][1] = x
    self.zeroup()

  def rotate(self, turns):
    if turns > 0:
      for i in range(turns):
        self.rotate90()
    elif turns < 0:
      turns = turns * -1
      for i in range(turns):
        self.antirotate90()
    else:
      self
    return self



hole = Piece('black',[[0,0]])
pieces = [
  Piece('red', [[0,0], [0,1], [1,0], [1,1], [2,0], [2,1], [1,2]]),
  Piece('gold_1', [[0,0], [0,1], [1,1], [1,2], [2,2]]),
  Piece('green', [[0,1], [0,2], [1,0], [1,1], [1,2], [2,1], [2,2], [2,3]]),
  Piece('dark_cyan', [[0,0], [1,0], [2,0], [3,0], [4,0]]),
  Piece('dark_orange', [[0,0], [1,0]]),
  Piece('orange_red_1', [[0,1], [1,0], [1,1], [2,0], [2,1], [3,1]]),
  Piece('purple_1a', [[0,0], [1,0], [1,1], [2,0], [2,1], [2,2]]),
  Piece('magenta', [[0,1], [1,0], [1,1], [1,2]]),
  Piece('blue', [[0,0], [0,1], [0,2], [0,3],[1,2]])
]  

def isFit(board, piece, location):
  for unit in piece.unit_list:
    if board[location[0]+unit[0]][location[1]+unit[1]] != 1:
      return False
  return True

def withinBoundary(x,y):
  return x >= 0 and x < 7 and y >=0 and y < 7

def withinBoard(board, piece, location):
  for unit in piece.unit_list:
      if not withinBoundary(location[0]+unit[0],location[1]+unit[1]):
        return False
  return True

def placePiece(board, piece, location):
  if withinBoard(board, piece, location) and isFit(board, piece, location):
      for unit in piece.unit_list:
        board[location[0]+unit[0]][location[1]+unit[1]] = (piece.unit_count, piece.color)
  return board

def printBoard(A):
  for line in A:
    for item in line:
      if isinstance(item, tuple):
        (block, color) = item
        print('%s%s%i%s' % (fg(color), bg(color), block, attr('reset')), end='')
      else:
        print('%s%s %s' % (fg('white'), bg('white'), attr('reset')), end='')
    print(' ')

# how to use it
# hole
A = placePiece(A, hole, H[1])
#red 3x3
A = placePiece(A, pieces[0].rotate(0), [1,0])
printBoard(A)
print(' ')

#yellow 3x3
A = placePiece(A, pieces[1].rotate(0), [1,3])
printBoard(A)
print(' ')
# green 3x4
A = placePiece(A, pieces[2].rotate(-1), [3,0])
printBoard(A)
print(' ')

#teal 1x5
A = placePiece(A, pieces[3].rotate(1), [6,2])
printBoard(A)
print(' ')
# #orange 1x2
A = placePiece(A, pieces[4].rotate(1), [5,4])
printBoard(A)
print(' ')
# #red 2x4 
A = placePiece(A, pieces[5].rotate(2), [2,3])
printBoard(A)
print(' ')
# #purple 3x3
A = placePiece(A, pieces[6].rotate(2), [0,4])
printBoard(A)
print(' ')
# #purple 2x3 
A = placePiece(A, pieces[7].rotate(-1), [3,5])
printBoard(A)
print(' ')
# #blue 2x4
A = placePiece(A, pieces[8].rotate(0), [0,0])
#print to terminal
printBoard(A)
