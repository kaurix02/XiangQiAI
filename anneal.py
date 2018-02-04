# Simulated annealing

from copy import deepcopy
from common import getValue
from random import random, choice
from math import exp


class Anneal:
	def __init__(self, pl, board, verbose=True):
		self.pl = pl
		self.board = board
		self.verbose = verbose

	def __str__(self):
		return "Anneal player, side: " + str(self.pl)

	def move(self):
		board = deepcopy(self.board)
		best = self.simulated_annealing(board)
		if self.verbose:
			print("Anneal %s moving %s to %s." % (str(self.pl), str(best[0]), str(best[1])))
		return best[0],best[1]
		# self.board.make_move(best[0], best[1])

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

	def analyze(self, board, piece, move, player=None):
		if player is None:
			player = self.pl

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

		return (pl_threat_level - op_threat_level) + (n_pl_covers - n_op_covers) + (n_pl_moves - n_op_moves)

	def get_neighbour(self, current_piece, current_move, moves, k):
		moves2 = deepcopy(moves)
		if random() > 0.5 + k / 10 and len(moves2[current_piece]) > 1:
			piece_moves = moves2[current_piece]
			piece_moves.remove(current_move)
			return current_piece, choice(piece_moves)
		else:
			new_piece = choice(list(moves2.keys()))
			new_move = choice(moves2[new_piece])
			return new_piece, new_move

	def change_probability(self, delta, k):
		return exp(-delta / k)

	def simulated_annealing(self, board):
		moves, covers = board.get_moves()
		# Choose a random piece and a move initially
		current_piece = choice(list(moves.keys()))
		current_move = choice(moves[current_piece])
		current_score = self.analyze(board, current_piece, current_move)
		best = (current_piece, current_move)
		best_score = current_score
		t = 10  # initial temperature
		t_bound = 1  # lower bound
		while t > t_bound:
			new_piece, new_move = self.get_neighbour(current_piece, current_move, moves, t)
			new_score = self.analyze(board, new_piece, new_move)
			delta = new_score if current_score == 0 else (new_score - current_score) / current_score
			if delta <= 0 or self.change_probability(delta, t) > 0.5:
				current_piece = new_piece
				current_move = new_move
				current_score = new_score
			if new_score > best_score:
				best_score = new_score
				best = (new_piece, new_move)
			t *= 0.8
		return best


flatten = lambda l: [item for sublist in l for item in sublist]
