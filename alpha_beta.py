# Alpha-beta pruning algorithm
from copy import deepcopy
from common import getValue
from random import random, choice


class AlphaBeta:
	def __init__(self, pl, board, verbose=True):
		self.pl = pl
		self.board = board
		self.verbose = verbose

	def __str__(self):
		return "AlphaBeta player, side: " + str(self.pl)

	def move(self):
		board = deepcopy(self.board)
		best = self.alpha_beta(board, None, None, 2, -9999, 9999, self.pl, True)[1]
		print("AlphaBeta %s moving %s to %s." % (str(self.pl), str(best[0]), str(best[1])))
		self.board.make_move(best[0], best[1])


	def get_threats(self, player, board, op_moves, pl_covers):
		count = 0
		score = 0
		for p in op_moves:
			for m in op_moves[p]:
				piece = board.board[m[0]][m[1]]
				if piece is not None and piece.pl == player:
					# If enemy piece can move to take friendly piece
					count += 1  # Without piece values
					add_score = 1 if piece in pl_covers else 0  # If it protects some piece, give it additional value
					score += getValue(piece) + add_score
		return count, score


	# Returns the heuristic for a certain move of a player considering the current situation
	def analyze(self, board, piece, move, player):
		board_after = deepcopy(board)
		board_after.make_move(piece, move)
		opponent = (player + 1) % 2
		pl_moves, pl_covers = board_after.get_moves(player)
		op_moves, op_covers = board_after.get_moves(opponent)

		# 0. Check if game is won after move
		if board_after.won:
			return 9999

		# 1. Space/number of moves for the opponent
		n_op_moves = sum([len(moves) for moves in op_moves.values()])

		# 2. Space/number of moves for the player
		n_pl_moves = sum([len(moves) for moves in pl_moves.values()])

		# 3. Get threat level by opponent after move
		op_threat_count, op_threat_level = self.get_threats(player, board_after, op_moves, pl_covers)

		# 4. Get threat level to opponent after move
		pl_threat_count, pl_threat_level = self.get_threats(opponent, board_after, pl_moves, op_covers)

		# 5. Get number of player's covered pieces after move
		n_pl_covers = len(set(flatten(pl_covers.values())))

		# 6. Get the number of opponent's covered pieces after move
		n_op_covers = len(set(flatten(op_covers.values())))

		return (pl_threat_level - op_threat_level) + (n_pl_covers - n_op_covers) + (n_pl_moves - n_op_moves), (piece, move)


	def alpha_beta(self, board, piece, move, depth, alpha, beta, player, is_maximising_pl):
		if depth == 0:
			return self.analyze(board, piece, move, player)

		moves, _ = board.get_moves(player)
		opponent = (player + 1) % 2

		# Just in case, select a random move as the best one first
		random_piece = choice(list(moves.keys()))
		random_move = choice(moves[random_piece])
		best = (random_piece, random_move)

		if is_maximising_pl:  # We want to maximise the score
			h = -9999
			for p in moves:
				for m in moves[p]:
					score, p_m = self.alpha_beta(board, p, m, depth - 1, alpha, beta, opponent, False)
					if h < score or (h == score and random() > 0.5):
						h = score
						best = p_m

					alpha = max(alpha, h)
					if beta <= alpha:
						break
			return h, best
		else:  # We want to minimize the score
			h = 9999
			for p in moves:
				for m in moves[p]:
					score, p_m = self.alpha_beta(board, p, m, depth - 1, alpha, beta, opponent, True)
					if h > score or (h == score and random() > 0.5):
						h = score
						best = p_m

					beta = min(beta, h)
					if beta <= alpha:
						break
			return h, best


flatten = lambda l: [item for sublist in l for item in sublist]