defboard = """
RHEAGAEHR
         
 C     C 
S S S S S
         
         
S S S S S
 C     C 
         
RHEAGAEHR
"""
import os
clear = lambda: os.system('cls' if os.name=='nt' else 'clear')


class Board:
	def __init__(self, strboard = None):	#strboard for if you want to load a board from string
		self.player = 0
		self.won = None	#Who won, also used to check if gameover
		if strboard == None:
			self.__initboard()
		else:
			self.__initboard(strboard)
		self.show()
	def __initboard(self, strboard = defboard):
		self.board = []	#all pieces on board
		for i in range(10):
			self.board.append([])
			for j in range(9):
				self.board[i].append(None)
		i = 0	#Row number
		j = 0	#column number
		pl = 0	#pl0 is Player 1, pl1 is Player 2
		for piece in defboard:
			if piece == '\n':
				continue
			if piece!=' ' and piece!='\n':
				self.board[i][j]=Piece(piece,i,j, pl)

			j += 1
			if j == 9:
				j = 0
				i += 1
				if i>5:
					pl = 1
	def show(self):
		clear()
		for row in self.board:
			print("|", end="")
			for piece in row:
				if piece==None:
					print("  ", end="|")
				else:
					print(piece, end="|")
			print()
	def canmove(self, piece, pos):	#piece.name gets us piece type
		x,y = pos[0],pos[1]	#Target position
		### TODO
		pass
	def seesGov(self, *args):	#True if that position is in direct line of sight to opposing governor; usable for Rook/Governor move checks
		if len(args)==1:	#If Piece is given
			x,y,pl = args[0].x, args[0].y, args[0].pl
		elif len(args)==3:	#If x,y,pl is given
			x,y = args[0], args[1], args[2]
		if pl == 0:
			if x not in [7,8,9] and y not in [3,4,5]:	#No possible LoS
				return False
		elif pl == 1:
			if x not in [0,1,2] and y not in [3,4,5]:	#No possible LoS
				return False
		if y in [3,4,5]:	#Vertical
			for i in range(y-1,-1,-1):
				if self.board[x,i]!=None:	#Piece found
					if self.board[x,i].name='G' and self.board[x,i].pl != pl:	#If hostile governor
						return True
					else:	#LoS blocked
						break
			for i in range(y+1,9):
				if self.board[x,i]!=None:
					if self.board[x,i].name='G' and self.board[x,i].pl != pl:	#If hostile governor
						return True
					else:	#LoS blocked
						break
		if x in [0,1,2,7,8,9]:	#Horizontal
			for i in range(x-1,-1,-1):
				if self.board[i,y]!=None:
					if self.board[i,y].name=='G' and self.board[i,y].pl != pl:	#If hostile governor
						return True
					else:	#LoS blocked
						break
		return False	#No True condition met, no LoS
	def ischeck(self):	#returns True if the opponent could take Governor on next turn
		moves = self.getmoves((self.player+1)%2)
		for movepiece in moves:
			for move in moves[movepiece]:
				if self.board[move[0]],[move[1]]!=None and self.board[move[0]],[move[1]].name=="G":
					self.check=True
		self.check=False
	def ischeckmate(self):	#Checks if game over
		if self.check and len(getmoves(self.player))==0:
			self.won = (self.player+1)%2	#Declares winner
		
	def getmoves(self, player):	#Get all possible moves for given player.
		moves = {}	#Valid moves per piece
		covers = {}	#Which friendly pieces are 'protected' by piece
		### TODO
		### Once all moves found, if player in check (self.check), filter out moves that do not escape from check
		return moves, covers
	def makemove(self, *args):	#Move piece at x1,y1 to x2,y2
		if len(args)==4:
			x1,y1 = args[0], args[1]	#From
			x2,y2 = args[2], args[3]	#To
		elif len(args)==3:
			x1,y1 = args[0].x, args[0].y	#Get From from Piece
			x2,y2 = args[1], args[2]	#To
		self.board[x1][y1], self.board[x2][y2] = None, self.board[x1][y1]
		self.board[x2][y2].set(x2,y2)
		self.player = (self.player+1)%2	#Change whose turn it is
		self.show()
		if self.check:
			print("## You are in check! ##")
		self.ischeckmate()
class Piece:
	def __init__(self, name,x,y,pl):
		self.name = name
		self.x = x
		self.y = y
		self.pl = pl	#Which player this belongs to
	def __str__(self):	#For printing with print command
		return self.name+str(self.pl)
	def __repr__(self):	#For if printing as part of list
		return self.name+str(self.pl)
	def getmoves(self):
		if self.name=='S':	#Soldier/pawn
			if self.x<=5 and self.pl==0:	#On player's side
				return [(self.x+1, self.y)]
			elif self.x>5 and self.pl==1:	#On player's side
				return [(self.x-1, self.y)]
			else:	#Across the river
				moves=[]
				if self.pl==0:	#Across the river
					if self.x<9:
						moves.append((self.x+1,self.y))
				else:
					if self.x>0:
						moves.append((self.x-1,self.y))
				if self.y>0:
					moves.append((self.x,self.y-1))
				if self.y<8:
					moves.append((self.x,self.y+1))
				return moves
		elif self.name=='R' or self.name=='C':	#Rook/Chariot, Cannon
			moves=[]
			for i in range(0,self.x):
				moves.append((i,self.y))
			for i in range(self.x+1,10):
				moves.append((i,self.y))
			for i in range(0,self.y):
				moves.append((self.x,i))
			for i in range(self.y+1,9):
				moves.append((self.x,i))
			return moves
		elif self.name=='H':	#Horse/Knight
			boxy=list(range(9))
			boxx=list(range(10))
			moves=[]
			if self.x+2 in boxx:
				if self.y+1 in boxy:
					moves.append((self.x+2,self.y+1))
				if self.y-1 in boxy:
					moves.append((self.x+2,self.y-1))
			if self.x+1 in boxx:
				if self.y+2 in boxy:
					moves.append((self.x+1,self.y+2))
				if self.y-2 in boxy:
					moves.append((self.x+1,self.y-2))
			if self.x-1 in boxx:
				if self.y+2 in boxy:
					moves.append((self.x-1,self.y+2))
				if self.y-2 in boxy:
					moves.append((self.x-1,self.y-2))
			if self.x-2 in boxx:
				if self.y+1 in boxy:
					moves.append((self.x-2,self.y+1))
				if self.y-1 in boxy:
					moves.append((self.x-2,self.y-1))
			return moves
		elif self.name=='E':	#Elephant/Bishop
			moves=[]
			if self.x==0 or self.x==4:
				moves.append((2,self.y-2))
				moves.append((2,self.y+2))
			elif self.x==5 or self.x==9:
				moves.append((8,self.y-2))
				moves.append((8,self.y+2))
			elif self.y==0:
				moves.append((self.x-2,2))
				moves.append((self.x+2,2))
			elif self.y==8:
				moves.append((self.x-2,6))
				moves.append((self.x+2,6))
			else:	#Center column
				moves.append((self.x-2,self.y-2))
				moves.append((self.x+2,self.y-2))
				moves.append((self.x-2,self.y+2))
				moves.append((self.x+2,self.y+2))
			return moves
		elif self.name=='A':	#Advisor
			if self.x==0 or self.x==2:
				return [(1,4)]
			elif self.x==9 or self.x==7:
				return [(8,4)]
			else:
				moves=[]
				moves.append((self.x+1,3))
				moves.append((self.x+1,5))
				moves.append((self.x-1,3))
				moves.append((self.x-1,5))
				return moves
		elif self.name=='G':	#Governator
			boxy=list(range(3,6))
			boxx=list(range(3))+list(range(7,10))
			moves=[]
			if self.x+1 in boxx:
				moves.append((self.x+1,self.y))
			if self.x-1 in boxx:
				moves.append((self.x-1,self.y))
			if self.y+1 in boxy:
				moves.append((self.x,self.y+1))
			if self.y-1 in boxy:
				moves.append((self.x,self.y-1))
			return moves
	def set(self, x, y):	#Move current position
		self.x = x
		self.y = y

Board()
