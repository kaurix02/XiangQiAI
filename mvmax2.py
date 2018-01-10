# Movement maxxer model. Plays whichever move either wins or creates the most possible moves for next move (frees up pieces). Also checks for piece values

from random import random
from copy import deepcopy
from common import getValue


class MvMax2:
	def __init__(self, pl, board, verbose=True):
		self.pl = pl
		self.board = board
		self.verbose = verbose
		print(self)

	def __str__(self):
		return "MoveMaxxer player, side: " + str(self.pl) + ", smart"

	def move(self):
		moves, c = self.board.get_moves(self.pl)
		tmoves, tc = len(moves), c
		best = (None, None, -9999)
		for p in moves:
			for m in moves[p]:
				deval = self.analyze(p, m, tmoves, tc)
				if deval > best[2]:  # If evaluation beats current best move
					best = (p, m, deval)  # New best move saved!
				elif deval == best[2]:
					if random() > 0.5:
						best = (p, m, deval)
		if self.verbose:
			print("MoveMaxxer " + str(self.pl) + " moving " + str(best[0]) + " to " + str(best[1]) + ".")
		self.board.make_move(best[0], best[1])

	def analyze(self, piece, move, movesNow, cov):  # Analyzes move, return evaluation based on gained moves
		board2 = deepcopy(self.board)
		covNow = self.getCovers(self.board, cov)  # Score protected pieces
		thrNow = self.getThreats(board2)  # Score threats to own pieces
		board2.make_move(piece, move)
		movesLater, cov2 = board2.get_moves(self.pl)
		movesLater = len(movesLater)
		covLater = self.getCovers(board2, cov2)  # Score protected pieces
		thrLater = self.getThreats(board2)  # Score threats to own pieces
		if board2.won:  # if move would win the game
			return 9999  # return over 9000
		else:
			score = movesLater - movesNow  # Add gained moves
			score += (covLater - covNow) * 2  # Add gained friendly covers *2
			score += (thrNow - thrLater) * 2  # Smaller scalar to account for threat value
			return score  # return heuristic score for move

	def getThreats(self, board):
		opMoves, _ = board.get_moves((self.pl + 1) % 2)  # Get potential moves by opponent
		count = 0
		for p in opMoves:
			for m in opMoves[p]:
				if board.board[m[0]][m[1]] != None and board.board[m[0]][
					m[1]].pl == self.pl:  # If enemy piece can move to take friendly piece
					tp = board.board[m[0]][m[1]]
					count += getValue(tp)
		return count

	def getCovers(self, board, covers):
		count = 0
		for p in covers:
			for m in covers:
				tp = board.board[m.x][m.y]
				count += getValue(tp)
		return count
