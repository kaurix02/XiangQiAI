# This class is where we pit players against each other

from board import Board  # Board itself
from human import Human  # Human player for testing
from dummy import Dummy  # Dummy player with random moves
from mvmax import MvMax  # AI player wants more mobility
from mvmax2 import MvMax2  # AI player wants more mobility weighed by piece threats
from sfocus import SFocus  # AI player wants defend/attack valuable pieces

players = [Human, Dummy, MvMax, MvMax2, SFocus]  # List of possible players to choose from


def new_game(pl1, pl2, new_board=None):
	if new_board is None:
		new_board = Board()  # Make new board
	else:
		new_board = Board(new_board)  # Make board from string
	pl1 = pl1(0, new_board)  # Turn class into object for player1
	pl2 = pl2(1, new_board)  # Turn class into object for player2
	moves = 0 # Count total number of moves
	while new_board.won is None:  # While game continues...
		print("Move %d" % moves)
		if new_board.player == 0:
			pl1.move()
			moves += 1
		else:
			pl2.move()		
		new_board.is_checkmate()
	if new_board.won == 2:
		print("Game over, stalemate!")
	else:
		print("Game over, winner: " + str(new_board.won))


# new_game(Human, Human)	#Example to do human v human game
new_game(Dummy, Dummy)  # Example to do dummy v dummy game
