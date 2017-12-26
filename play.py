# This class is where we pit players against each other

from board import Board	#Board itself
from human import Human	#Human player for testing
from dummy import Dummy	#Dummy player with random moves
from mvmax import MvMax	#AI player wants more mobility
from mvmax2 import MvMax2	#AI player wants more mobility weighed by piece threats
from sfocus import SFocus	#AI player wants defend/attack valuable pieces

players = [Human, Dummy, MvMax, MvMax2, SFocus]	#List of possible players to choose from

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
