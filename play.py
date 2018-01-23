# This class is where we pit players against each other

import numpy as np
from board import Board  # Board itself
from human import Human  # Human player for testing
from dummy import Dummy  # Dummy player with random moves
from mvmax import MvMax  # AI player wants more mobility
from mvmax2 import MvMax2  # AI player wants more mobility weighed by piece threats
from sfocus import SFocus  # AI player wants defend/attack valuable pieces
from tritac import TriTac  # AI player wants mobility, defend/attack and checkmate
from alpha_beta import AlphaBeta
from anneal import Anneal

players = [Human, Dummy, MvMax, MvMax2, SFocus, TriTac, AlphaBeta, Anneal]  # List of possible players to choose from


def new_game(pl1, pl2, new_board=None, verbose=True):
	if new_board is None:
		new_board = Board()  # Make new board
	else:
		new_board = Board(new_board)  # Make board from string
	pl1 = pl1(0, new_board, verbose)  # Turn class into object for player1
	pl2 = pl2(1, new_board, verbose)  # Turn class into object for player2
	moves = 0  # Count total number of moves
	while new_board.won is None:  # While game continues...
		if verbose:
			print("Move %d" % moves)
			new_board.show()
		if new_board.player == 0:
			pl1.move()
			moves += 1
		else:
			pl2.move()
		if new_board.check:
			print("### You are in check! ###")
		new_board.is_checkmate()
		if moves > 300:
			print("### Game too long! ###")
			new_board.won = 2
	if verbose:
		new_board.show()  # Show final state of game
		if new_board.won == 2:
			print("Game over, stalemate!")
		else:
			print("Game over, winner: " + str(new_board.won))
	return new_board.won, moves


def run_test_sm(p1, p2, n=10):
	res = {0: [0, 0], 1: [0, 0], 2: [0, 0]}
	for i in range(n):  # Do n games
		r, m = new_game(p1, p2, verbose=False)
		res[r][0] += 1  # Count victory
		res[r][1] += m  # Count moves taken
	for i in range(3):
		if res[i][0] > 0:
			res[i][1] = res[i][1] / res[i][0]  # Average moves per game per result
	return res


def run_test_med(pl, pls, n=10):
	for i in range(len(pls)):
		print(run_test_sm(pl, pls[i], n))


def run_test_bg(pls, n=10):
	dim = len(pls)
	wins = np.zeros((dim, dim))  # Initialize matrices for number of each result
	wins_m = np.zeros((dim, dim))  # Initialize matrices for average length of game
	losses = np.zeros((dim, dim))
	losses_m = np.zeros((dim, dim))
	ties = np.zeros((dim, dim))
	ties_m = np.zeros((dim, dim))
	for i in range(dim):  # For each player1
		for j in range(dim):  # For each player2
			result = run_test_sm(pls[i], pls[j], n)  # Run test n times, get results
			wins[i][j] = result[0][0]
			wins_m[i][j] = result[0][1]
			losses[i][j] = result[1][0]
			losses_m[i][j] = result[1][1]
			ties[i][j] = result[2][0]
			ties_m[i][j] = result[2][1]
			print(result)  # Show result because if bug later, could get first results.
	np.savetxt("results/wins.csv", wins, delimiter=",")  # Save results
	np.savetxt("results/wins_m.csv", wins_m, delimiter=",")
	np.savetxt("results/losses.csv", losses, delimiter=",")
	np.savetxt("results/losses_m.csv", losses_m, delimiter=",")
	np.savetxt("results/ties.csv", ties, delimiter=",")
	np.savetxt("results/ties_m.csv", ties_m, delimiter=",")

# new_game(Human, Human)	# Example to do human v human game
# new_game(Dummy, Dummy)	# Example to do dummy v dummy game
# run_test_bg(players[1:])
# run_test_med(TriTac, players[1:])
# print(run_test_sm(TriTac, Dummy,10))
# print(new_game(AlphaBeta, Dummy))
# new_game(Dummy, TriTac)
