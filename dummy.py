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
		moves = self.board.getmoves(self.pl)
		choice = len(moves)*random()
		mymove = moves[choice]
		print("Dummy "+str(pl)+" moving "+str(mymove)+".")
		self.board.makemove(mymove[0:2],mymove[2:])
