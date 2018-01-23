from collections import defaultdict
import os
from copy import deepcopy

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

defboard = """
RHEAGAEHR
         
 C     C 
S S S S S
         
         
S S S S S
 C     C 
         
RHEAGAEHR
"""


class Board:
	def __init__(self, strboard=None):	# strboard for if you want to load a board from string
		self.player = 0
		self.won = None  # Who won, also used to check if gameover
		if strboard is None:
			self.__initboard()
		else:
			self.__initboard(strboard)
	# self.show()

	def __initboard(self, strboard=defboard):
		self.board = []  # all pieces on board
		for i in range(10):
			self.board.append([])
			for j in range(9):
				self.board[i].append(None)
		i = 0  # Row number
		j = 0  # column number
		pl = 0  # pl0 is Player 1, pl1 is Player 2
		if strboard == defboard:
			self.check = False
			for piece in strboard:
				if piece == '\n':
					continue
				if piece != ' ':
					self.board[i][j] = Piece(piece, i, j, pl)

				j += 1
				if j == 9:
					j = 0
					i += 1
					if i > 5:
						pl = 1
		else:
			rows = list(filter(lambda row: row != "\n" and row != "", strboard.split("\n")))
			self.is_check()
			for i in range(len(rows)):
				row = rows[i]
				pieces = row.split("|")
				for j in range(len(pieces)):
					piece = pieces[j]
					if len(piece) == 2 and piece[0] in ['R', 'H', 'E', 'A', 'G', 'C', 'S']:
						self.board[i][j] = Piece(piece[0], i, j, int(piece[1]))

	def show(self):
		# clear()
		for row in self.board:
			print("|", end="")
			for piece in row:
				if piece is None:
					print("  ", end="|")
				else:
					print(piece, end="|")
			print()

	def is_unblocked(self, piece, pos):
		"""
		Returns True if the piece can move to the given position 'pos' if all the basic rules are checked EXCEPT FOR THE FOLLOWING TWO:
		(1) kings being in line of sight of each other in the next turn
		(2) an opponent's piece being able to take down the other's king in the next turn.

		This method is used for checking if any of the opponents pieces can take out the king in the next move.
		"""
		# Check precondition
		if pos not in piece.moves:
			return False
		x, y = pos[0], pos[1]  # Target position
		curr_x, curr_y = piece.x, piece.y  # Current position

		if self.board[x][y] is not None and self.board[x][y].pl == piece.pl:
			# If some piece of the same player is already on target position
			return False

		if piece.name == 'R':  # Rook/chariot
			if x - curr_x != 0:
				inc = 1 if x > curr_x else -1
				for i in range(curr_x + inc, x, inc):
					if self.board[i][y] is not None:
						return False
			elif y - curr_y != 0:
				inc = 1 if y > curr_y else -1
				for j in range(curr_y + inc, y, inc):
					if self.board[x][j] is not None:
						return False
		elif piece.name == 'C':  # Cannon
			count = 0  # Counts how many pieces are between original and target position
			is_empty = self.board[x][y] is None
			if x - curr_x != 0:
				inc = 1 if x > curr_x else -1
				for i in range(curr_x + inc, x, inc):
					if self.board[i][y] is not None:
						count += 1
						if count > 1 or (count > 0 and is_empty):
							return False
			elif y - curr_y != 0:
				inc = 1 if y > curr_y else -1
				for j in range(curr_y + inc, y, inc):
					if self.board[x][j] is not None:
						count += 1
						if count > 1 or (count > 0 and is_empty):
							return False

			if (not is_empty) and count != 1:
				return False
		elif piece.name == 'H':  # Horse/knight
			if abs(x - curr_x) == 2:
				inc = 1 if x > curr_x else -1
				if self.board[curr_x + inc][curr_y] is not None:
					return False
			elif abs(y - curr_y) == 2:
				inc = 1 if y > curr_y else -1
				if self.board[curr_x][curr_y + inc] is not None:
					return False
		elif piece.name == 'E':  # Elephant/bishop
			mid_x = curr_x + (1 if x > curr_x else -1)
			mid_y = curr_y + (1 if y > curr_y else -1)
			if self.board[mid_x][mid_y] is not None:
				return False

		# Assuming that for the soldiers, advisors and the king the moves are already correct.
		return True

	def can_move(self, piece, pos):  # piece.name gets us piece type
		"""
		Returns True if the piece can move to the given position.
		"""

		# First, check blockings, basic rules
		if not self.is_unblocked(piece, pos):
			return False

		x, y = pos[0], pos[1]  # Target position
		new_board = deepcopy(self)
		new_board.make_move(piece, x, y)

		# Find both kings
		king1_x, king1_y = None, None
		king2_x, king2_y = None, None
		for i in list(range(3)) + list(range(7, 10)):
			for j in range(3, 6):
				p = new_board.board[i][j]
				if p is not None and p.name == 'G':
					if p.pl == 0:
						king1_x = i
						king1_y = j
					else:
						king2_x = i
						king2_y = j
				if not None in [king1_x, king1_y, king2_x, king2_y]:
					break

		# Check if the kings are in line of sight
		if king1_y == king2_y:
			is_in_sight = True
			for i in range(min(king1_x, king2_x) + 1, max(king1_x, king2_x)):
				if new_board.board[i][king1_y] is not None:
					is_in_sight = False
					break
			if is_in_sight:
				return False

		# Finally, check if the opponent could take the king on the next turn
		opponent = (piece.pl + 1) % 2
		return not new_board.is_check(opponent)

	def sees_Gov(self,
				 *args):  # True if that position is in direct line of sight to opposing governor; usable for Rook/Governor move checks
		x, y, pl = None, None, None
		if len(args) == 1:  # If Piece is given
			x, y, pl = args[0].x, args[0].y, args[0].pl
		elif len(args) == 3:  # If x,y,pl is given
			x, y, pl = args[0], args[1], args[2]

		if pl == 0:
			if x not in [7, 8, 9] and y not in [3, 4, 5]:  # No possible LoS
				return False
		elif pl == 1:
			if x not in [0, 1, 2] and y not in [3, 4, 5]:  # No possible LoS
				return False
		if y in [3, 4, 5]:  # Vertical
			for i in range(y - 1, -1, -1):
				if self.board[x][i] is not None:  # Piece found
					if self.board[x][i].name == 'G' and self.board[x][i].pl != pl:  # If hostile governor
						return True
					else:  # LoS blocked
						break
			for i in range(y + 1, 9):
				if self.board[x][i] is not None:
					if self.board[x][i].name == 'G' and self.board[x][i].pl != pl:  # If hostile governor
						return True
					else:  # LoS blocked
						break
		if x in [0, 1, 2, 7, 8, 9]:  # Horizontal
			for i in range(x - 1, -1, -1):
				if self.board[i][y] is not None:
					if self.board[i][y].name == 'G' and self.board[i][y].pl != pl:  # If hostile governor
						return True
					else:  # LoS blocked
						break
		return False  # No True condition met, no LoS

	def is_check(self, opponent=None):  # returns True if the opponent could take the Governor on next turn
		if opponent is None:
			opponent = (self.player + 1) % 2
		moves = self.get_unblocked_moves(opponent)
		for move_piece in moves:
			for move in moves[move_piece]:
				if self.board[move[0]][move[1]] is not None and self.board[move[0]][move[1]].name == "G":
					self.check = True
					return True
		self.check = False
		return False

	def is_checkmate(self):  # Checks if game over
		if len(self.get_moves()) == 0:	#No moves left - either cannot move or cannot escape check
			self.won = (self.player + 1) % 2  # Declares winner
			return
		# print(len(self.get_moves()))
		p1pieces = self.get_pieces(0)
		for piece in p1pieces:
			if piece.name in ["R","C","H","S"]:
				return
		p2pieces = self.get_pieces(1)
		for piece in p2pieces:
			if piece.name in ["R","C","H","S"]:
				return
		self.won = 2	# Stalemate - neither player has offensive pieces

	def get_unblocked_moves(self, player=None):
		"""
		Returns the moves which qualify without checking the following 2 conditions:
		(1) kings being in line of sight of each other in the next turn
		(2) an opponent's piece being able to take down the other's king in the next turn.
		"""
		if player is None:
			player = self.player
		moves = {}  # Valid moves per piece
		for piece in self.get_pieces(player):
			moves[piece] = list(filter(lambda pos: self.is_unblocked(piece, pos), piece.get_all_moves()))
		return moves

	def get_protectors(self, player=None):
		if player is None:
			player = self.player

		protectors = defaultdict(set)
		opponent = (player + 1) % 2
		opponent_pieces = self.get_pieces(opponent)

		for piece in opponent_pieces:
			curr_x, curr_y = piece.x, piece.y
			for move in piece.get_all_moves():
				x, y = move[0], move[1]
				# If a player's piece is on the target position and the opponent cannot take it
				if self.board[x][y] is not None and self.board[x][y].pl == player \
						and not self.is_unblocked(piece, move):
					# The player's piece
					protected = self.board[x][y]
					if piece.name == 'R':  # Rook/chariot
						if x - curr_x != 0:
							inc = 1 if x > curr_x else -1
							for i in range(curr_x + inc, x, inc):
								if self.board[i][y] is not None:
									protectors[self.board[i][y]].add(protected)
						elif y - curr_y != 0:
							inc = 1 if y > curr_y else -1
							for j in range(curr_y + inc, y, inc):
								if self.board[x][j] is not None:
									protectors[self.board[x][j]].add(protected)
					elif piece.name == 'C':  # Cannon
						if x - curr_x != 0:
							inc = 1 if x > curr_x else -1
							for i in range(curr_x + inc, x, inc):
								if self.board[i][y] is not None:
									protectors[self.board[i][y]].add(protected)
						elif y - curr_y != 0:
							inc = 1 if y > curr_y else -1
							for j in range(curr_y + inc, y, inc):
								if self.board[x][j] is not None:
									protectors[self.board[x][j]].add(protected)
					elif piece.name == 'H':  # Horse/knight
						if abs(x - curr_x) == 2:
							inc = 1 if x > curr_x else -1
							if self.board[curr_x + inc][curr_y] is not None:
								protectors[self.board[curr_x + inc][curr_y]].add(protected)
						elif abs(y - curr_y) == 2:
							inc = 1 if y > curr_y else -1
							if self.board[curr_x][curr_y + inc] is not None:
								protectors[self.board[curr_x][curr_y + inc]].add(protected)
					elif piece.name == 'E':  # Elephant/bishop
						mid_x = curr_x + (1 if x > curr_x else -1)
						mid_y = curr_y + (1 if y > curr_y else -1)
						if self.board[mid_x][mid_y] is not None:
							protectors[self.board[mid_x][mid_y]].add(protected)

		return protectors

	def get_moves(self, player=None):  # Get all possible moves for given player
		if player is None:
			player = self.player
		moves = {}  # Valid moves per piece
		### Once all moves found, if player in check (self.check), filter out moves that do not escape from check

		for piece in self.get_pieces(player):
			valid_moves = list(filter(lambda pos: self.can_move(piece, pos), piece.get_all_moves()))
			if valid_moves != []:
				moves[piece] = valid_moves

		if len(moves) == 0:
			self.won = (self.player + 1) % 2
		covers = self.get_protectors(player)  # Which friendly pieces are 'protected' by piece
		return moves, covers

	def make_move(self, *args):  # Move piece at x1,y1 to x2,y2
		x1, y1, x2, y2 = None, None, None, None
		if type(args[0]) is tuple:
			x1, y1 = args[0][0], args[0][1]	# From
			x2, y2 = args[1][0], args[1][1]	# To
		elif len(args) == 4:
			x1, y1 = args[0], args[1]  # From
			x2, y2 = args[2], args[3]  # To
		elif len(args) == 3:
			x1, y1 = args[0].x, args[0].y  # Get from Piece
			x2, y2 = args[1], args[2]  # To
		elif len(args) == 2:
			x1, y1 = args[0].x, args[0].y  # Get from Piece
			x2, y2 = args[1]  # To
		p1 = self.board[x1][y1]
		self.board[x2][y2] = p1
		self.board[x1][y1] = None
		self.board[x2][y2].set(x2, y2)
		self.player = (self.player + 1) % 2  # Change whose turn it is
		# self.show()
		if self.check:
			print("## You are in check! ##")
		self.checkIntegrity()
		# self.is_checkmate()

	def get_pieces(self, player=None):  # Get all the pieces of this player
		if player is None:
			player = self.player
		pieces = []
		for i in range(10):
			for j in range(9):
				piece = self.board[i][j]
				if piece is not None and piece.pl == player:
					pieces.append(piece)
		return pieces
	def checkIntegrity(self):
		bad = 0
		for i in range(10):
			for j in range(9):
				if self.board[i][j] is not None:
					if self.board[i][j].x != i:
						bad += 1
					if self.board[i][j].y != j:
						bad += 1
		if bad>0:
			print("Errors: "+str(bad))

class Piece:
	def __init__(self, name, x, y, pl):
		self.name = name
		self.x = x
		self.y = y
		self.pl = pl  # Which player this belongs to

	def __str__(self):  # For printing with print command
		return self.name + str(self.pl)

	def __repr__(self):  # For if printing as part of list
		return self.name + str(self.pl)

	def __eq__(self, other):
		if self is None or other is None:
			return self is None and other is None
		return self.name == other.name and self.x == other.x and self.y == other.y and self.pl == other.pl

	def __hash__(self):
		return hash((self.name, self.x, self.y, self.pl))
	def get_all_moves(self):
		self.moves = self.__get_all_moves()
		return self.moves

	def __get_all_moves(self):
		if self.name == 'S':  # Soldier/pawn
			if self.x < 5 and self.pl == 0:  # On player's side
				return [(self.x + 1, self.y)]
			elif self.x >= 5 and self.pl == 1:  # On player's side
				return [(self.x - 1, self.y)]
			else:  # Across the river
				moves = []
				if self.pl == 0:  # Across the river
					if self.x < 9:
						moves.append((self.x + 1, self.y))
				else:
					if self.x > 0:
						moves.append((self.x - 1, self.y))
				if self.y > 0:
					moves.append((self.x, self.y - 1))
				if self.y < 8:
					moves.append((self.x, self.y + 1))
				return moves
		elif self.name == 'R' or self.name == 'C':  # Rook/Chariot, Cannon
			moves = []
			for i in range(0, self.x):
				moves.append((i, self.y))
			for i in range(self.x + 1, 10):
				moves.append((i, self.y))
			for i in range(0, self.y):
				moves.append((self.x, i))
			for i in range(self.y + 1, 9):
				moves.append((self.x, i))
			return moves
		elif self.name == 'H':  # Horse/Knight
			boxy = list(range(9))
			boxx = list(range(10))
			moves = []
			if self.x + 2 in boxx:
				if self.y + 1 in boxy:
					moves.append((self.x + 2, self.y + 1))
				if self.y - 1 in boxy:
					moves.append((self.x + 2, self.y - 1))
			if self.x + 1 in boxx:
				if self.y + 2 in boxy:
					moves.append((self.x + 1, self.y + 2))
				if self.y - 2 in boxy:
					moves.append((self.x + 1, self.y - 2))
			if self.x - 1 in boxx:
				if self.y + 2 in boxy:
					moves.append((self.x - 1, self.y + 2))
				if self.y - 2 in boxy:
					moves.append((self.x - 1, self.y - 2))
			if self.x - 2 in boxx:
				if self.y + 1 in boxy:
					moves.append((self.x - 2, self.y + 1))
				if self.y - 1 in boxy:
					moves.append((self.x - 2, self.y - 1))
			return moves
		elif self.name == 'E':  # Elephant/Bishop
			moves = []
			if self.x == 0 or self.x == 4:
				moves.append((2, self.y - 2))
				moves.append((2, self.y + 2))
			elif self.x == 5 or self.x == 9:
				moves.append((7, self.y - 2))
				moves.append((7, self.y + 2))
			elif self.y == 0:
				moves.append((self.x - 2, 2))
				moves.append((self.x + 2, 2))
			elif self.y == 8:
				moves.append((self.x - 2, 6))
				moves.append((self.x + 2, 6))
			else:  # Center column
				moves.append((self.x - 2, self.y - 2))
				moves.append((self.x + 2, self.y - 2))
				moves.append((self.x - 2, self.y + 2))
				moves.append((self.x + 2, self.y + 2))
			return moves
		elif self.name == 'A':  # Advisor
			if self.x == 0 or self.x == 2:
				return [(1, 4)]
			elif self.x == 9 or self.x == 7:
				return [(8, 4)]
			else:
				moves = [(self.x + 1, 3),
						 (self.x + 1, 5),
						 (self.x - 1, 3),
						 (self.x - 1, 5)]
				return moves
		elif self.name == 'G':  # Governator
			boxy = list(range(3, 6))
			boxx = list(range(3)) + list(range(7, 10))
			moves = []
			if self.x + 1 in boxx:
				moves.append((self.x + 1, self.y))
			if self.x - 1 in boxx:
				moves.append((self.x - 1, self.y))
			if self.y + 1 in boxy:
				moves.append((self.x, self.y + 1))
			if self.y - 1 in boxy:
				moves.append((self.x, self.y - 1))
			return moves

	def set(self, x, y):  # Move current position
		self.x = x
		self.y = y


Board()
