# Movement maxxer model. Plays whichever move either wins or creates the most possible moves for next move (frees up pieces).

from random import random
from copy import deepcopy

class MvMax:
	def __init__(self, pl, board):
		self.pl = pl
		self.board = board
		print(self)
	def __str__(self):
		return "MoveMaxxer player, side: "+str(self.pl)
	def move(self):
		moves,c = self.board.getmoves(self.pl)
		tmoves, tc = len(moves), len(c)
		best = (None, None, -9999)
		for p in moves:
			for m in moves[p]:
				deval = self.analyze(p,m,tmoves, tc)
				if deval > best[2]:	#If evaluation beats current best move
					best = (p,m,deval)	#New best move saved!
		print("MoveMaxxer "+str(pl)+" moving "+str(best[0])+" to "+str(best[1])+".")
		self.board.makemove(best[0],best[1])

	def analyze(self, piece, move, movesNow, covNow):	#Analyzes move, return evaluation based on gained moves
		board2 = deepcopy(self.board)
		thrNow = self.threats(board2)
		board2.makemove(piece, move)
		movesLater, covLater = len(board2.getmoves(self.pl))
		thrLater = self.threats(board2)
		if board2.won:	#if move would win the game
			return 9999	#return over 9000
		else:
			score = movesLater - movesNow	#Add gained moves
			score += (covLater - covNow)*2	#Add gained friendly covers *2
			score += (thrNow - thrLater)*3	#Remove gained threats *3
			return score	#return heuristic score for move
	def threats(self, board):
		opMoves,_ = board.getmoves((self.pl+1)%2)	#Get potential moves by opponent
		count = 0
		for p in opMoves:
			for m in opMoves[p]:
				if board[m[0]][m[1]]!=None and board[m[0]][m[1]].pl==self.pl:	#If enemy piece can move to take friendly piece
					count += 1	#Without piece values
		return count