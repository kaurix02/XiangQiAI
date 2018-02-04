# Three-staged heuristic that uses MoveMaxxer2 for initial start to get pieces out, then settles for SingleFocus to attack opponent pieces, followed by an aggressive move-minimizer against the opponent to checkmate. TriTac - TRIple TACtics, one strategy.
# If a move is evaluated near-best, uses random to decide whether to make that move instead. Creates unpredictability.

from random import random
from copy import deepcopy
from common import getValue
from sfocus import SFocus


class TriTac:
	def __init__(self, pl, board, verbose=True):
		self.pl = pl
		self.board = board
		self.verbose = verbose

	def __str__(self):
		return "TriTac player, side: " + str(self.pl)

	def move(self):
		moves, c = self.board.get_moves(self.pl)
		tmoves, tc = len(moves), c
		best = (None, None, -9999)
		op_pcs = len(self.board.get_pieces((self.pl+1)%2))
		pcs = len(self.board.get_pieces(self.pl)) + op_pcs  # 14+14
		if pcs > 20:  # After fewer than 8 pieces have been taken in total
			for p in moves:
				for m in moves[p]:
					deval = self.analyze(p, m, tmoves, tc)
					if deval > best[2]:  # If evaluation beats current best move
						if random() > 0.05:  # Small chance of ignoring
							best = (p, m, deval)  # New best move saved!
					elif deval == best[2]:
						if random() > 0.5:
							best = (p, m, deval)
					elif best[2] - deval < 1:  # If a move is almost as good
						if random() > 0.7:
							best = (p, m, deval)
		elif op_pcs < 6:
			best = self.minMoves(moves, c)
		else:  # When there are still many pieces at play
			model = SFocus(self.pl, self.board, False)
			best = model.move()
		if self.verbose:
			print("TriTac making move: " + str(best))
		if best[0] is None:
			print("Bug somewhere...")
			choice = int(len(moves) * random())
			my_piece = list(moves.keys())[choice]  # Choose piece to move
			my_move = moves[my_piece][int(len(moves[my_piece]) * random())]
			best = (my_piece, my_move)
		return best[0],best[1]
		# self.board.make_move(best[0], best[1])

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

	def getThreats(self, board, opMoves = None):
		if opMoves is None:
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

	def minMoves(self, moves, cov):
		opMoves = len(self.board.get_moves((self.pl + 1) % 2))  # How many possible moves opponent has
		covNow = self.getCovers(self.board, cov)  # How well are friendly pieces covered
		best = (None, None, opMoves, covNow)
		for p in moves:
			for m in moves[p]:
				res = self.getOpMoves(p, m)
				if best[0] is None:  # Make sure we have 'a' turn to make
					best = res
					continue
				elif res[2] == 0:  # Checkmate.
					return res
				elif res[2] < best[2]:
					if best[3] == 0 or best[4] == 0:	# Cannot divide
						if res[3]>0:
							best = res
					else:
						if random() * (res[3] / best[3]) * ((res[4]/best[4])**2) > 0.450 :  # Make a judgment call according to possible loss in defense
							best = res
		return best[0], best[1]

	def getOpMoves(self, piece, move):
		board2 = deepcopy(self.board)
		board2.make_move(piece, move)
		opMoves,_ = board2.get_moves((self.pl + 1) % 2)
		thr = self.getThreats(board2,opMoves)
		opMoves = len(opMoves)
		_, c = board2.get_moves(self.pl)
		covLater = self.getCovers(board2, c)
		return (piece, move, opMoves, covLater, thr)
