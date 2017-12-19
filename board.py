defboard = """
RHEAGAEHR
         
 C     C 
S S S S S
         
         
S S S S S
 C     C 
         
RHEAGAEHR
"""

class Board:
	def __init__(self, strboard = None):	#strboard for if you want to load a board from string
		if strboard == None:
			self.initboard()
		else:
			self.initboard(strboard)
		print(self.board)
	def initboard(self, strboard = defboard):
		self.board = []	#all pieces on board
		for i in range(10):
			self.board.append([])
			for j in range(9):
				self.board[i].append([])
		i = 0	#Row number
		j = 0	#column number
		pl = 0
		for piece in defboard:
			if piece == '\n':
				continue
			print("*"+piece+"*")
			if piece!=' ' and piece!='\n':
				print(piece, i, j)
				self.board[i][j]=Piece(piece,i,j, pl)

			j += 1
			if j == 9:
				j = 0
				i += 1
				if i>5:
					pl = 1
class Piece:
	def __init__(self, name,x,y,pl):
		self.name = name
		self.x = x
		self.y = y
		self.pl = pl
	def __str__(self):
		return self.name
	def __repr__(self):
		return self.name

Board()
