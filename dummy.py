#Dummy is a baseline model, takes all possible moves he can make and chooses one completely randomly.

from random import random

class Dummy:
	def __init__(self, pl, board):
		self.pl = pl
		self.board = board
		print(self)
	def __str__(self):
		return "Dummy player, side: "+str(self.pl)
	def move(self):
		moves,_ = self.board.getmoves(self.pl)
		choice = len(moves)*random()
		mypiece = list(moves.keys())[choice]	#Choose piece to move
		mymove = moves[mypiece][len(moves[mypiece])*random()]
		print("Dummy "+str(pl)+" moving "+str(mypiece)+" to "+str(mymove)+".")
		self.board.makemove(mypiece,mymove)
