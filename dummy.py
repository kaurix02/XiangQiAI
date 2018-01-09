# Dummy is a baseline model, takes all possible moves he can make and chooses one completely randomly.

from random import random


class Dummy:
	def __init__(self, pl, board, verbose=True):
		self.pl = pl
		self.board = board
		self.verbose = verbose
		print(self)

	def __str__(self):
		return "Dummy player, side: " + str(self.pl)

	def move(self):
		#self.board.show()
		moves, _ = self.board.get_moves(self.pl)
		if len(moves) == 0 and self.board.check:
			print("Player %d lost!" % self.pl)
			return
		choice = int(len(moves) * random())
		my_piece = list(moves.keys())[choice]  # Choose piece to move
		my_move = moves[my_piece][int(len(moves[my_piece]) * random())]
		if self.verbose:
			print("Dummy " + str(self.pl) + " moving " + str(my_piece) + " to " + str(my_move) + ".")
		self.board.make_move(my_piece, my_move)
