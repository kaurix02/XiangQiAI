# This class is where we pit players against each other

from board import Board
from human import Human
from dummy import Dummy
from mvmax import MvMax
from mvmax2 import MvMax2

players = [Human, Dummy, MvMax, MvMax2]	#List of possible players to choose from

def newgame(pl1, pl2, newboard=None):
	if newboard==None:
		newboard = Board()	#Make new board
	else:
		newboard = Board(newboard)	#Make board from string
	pl1 = pl1(0, newboard)	#Turn class into object for player1
	pl2 = pl2(1, newboard)	#Turn class into object for player2
	while newboard.won == None:	#While game continues...
		if newboard.player == 0:
			pl1.move()
		else:
			pl2.move()
	print("Game over, winner: "+str(newboard.won))

#newgame(Human, Human)	#Example to do human v human game
newgame(Dummy, Dummy)	#Example to do dummy v dummy game
