# Three-staged heuristic that uses MoveMaxxer2 for initial start to get pieces out, then settles for SingleFocus to attack opponent pieces, followed by an aggressive move-minimizer against the opponent to checkmate. TriTac - TRIple TACtics, one strategy.
# If a move is evaluated near-best, uses random to decide whether to make that move instead. Creates unpredictability.

from random import random
from copy import deepcopy
from common import getValue

class TriTac:
	def __init__(self, pl, board, verbose=True):
		self.pl = pl
		self.board = board
		self.verbose = verbose
		print(self)
	def __str__(self):
		return "TriTac player, side: "+str(self.pl)
	def move(self):
		moves,c = self.board.get_moves(self.pl)
		tmoves, tc = len(moves), c
		best = (None, None, -9999)
		pcs = len(self.board.get_pieces(0))+len(self.board.get_pieces(1))	#14+14
		if pcs > 20:	#After fewer than 8 pieces have been taken in total
			for p in moves:
				for m in moves[p]:
					deval = self.analyze(p,m,tmoves, tc)
					if deval > best[2]:	#If evaluation beats current best move
						if random() > 0.05:	#Small chance of ignoring
							best = (p,m,deval)	#New best move saved!
					elif deval == best[2]:
						if random() > 0.5:
							best = (p,m,deval)
					elif best[2]-deval < 1:	# If a move is almost as good
						if random() > 0.7:
							best = (p,m,deval)
		elif pcs > 16:	#When there are still many pieces at play
			maxPr = (None, -9999)	#Check most priority
			opPr = (None, -9999)	#Check most priority for opponent
			for i in self.board.board:	#Rows
				for j in i:	#Pieces
					if j == None:	#If no piece is there, ignore
						continue
					pr = self.getPriority(j)
					if j.pl == self.pl:
						if pr > maxPr[1]:
							maxPr = (j,pr)
					else:
						if -pr > opPr[1]:
							if random() > 0.1:	#Small chance of ignoring
								opPr = (j,-pr)
			best = (None, None, -9999)

			if maxPr[1]>2:	#If something valuable is under threat, do something defensive
				for p in moves:
					for m in moves[p]:
						deval = self.doDef(p,m,maxPr)
						if best[0] is None:
							best = (p,m,deval)
						elif deval > best[2]:
							best = (p,m,deval)
			#if self.verbose:
			#	print("TriTac best defensive move: "+str(best))

			if opPr[1]>2:	#If something valuable can be taken, take!
				p, m, deval = self.doAtt(opPr, moves, c)
				if best[0] is None:
					best = (p,m,deval)
				elif deval > best[2]:
					best = (p,m,deval)
			if best[0] is None:	#No good moves available
				choice = int(len(moves) * random())
				my_piece = list(moves.keys())[choice]  # Choose piece to move
				my_move = moves[my_piece][int(len(moves[my_piece]) * random())]
				best = (my_piece,my_move)
			#if self.verbose:
			#	print("TriTac best defensive/offensive move: "+str(best))
		else:	#Once half the board has been cleared
			best = self.minMoves(moves, c)
		if self.verbose:
			print("TriTac making move: "+str(best))
		if best[0] is None:
			print("Bug somewhere...")
			choice = int(len(moves) * random())
			my_piece = list(moves.keys())[choice]  # Choose piece to move
			my_move = moves[my_piece][int(len(moves[my_piece]) * random())]
			best = (my_piece,my_move)
		self.board.make_move(best[0],best[1])

	def analyze(self, piece, move, movesNow, cov):	#Analyzes move, return evaluation based on gained moves
		board2 = deepcopy(self.board)
		covNow = self.getCovers(self.board, cov)	#Score protected pieces
		thrNow = self.getThreats(board2)	#Score threats to own pieces
		board2.make_move(piece, move)
		movesLater, cov2 = board2.get_moves(self.pl)
		movesLater = len(movesLater)
		covLater = self.getCovers(board2, cov2)	#Score protected pieces
		thrLater = self.getThreats(board2)	#Score threats to own pieces
		if board2.won:	#if move would win the game
			return 9999	#return over 9000
		else:
			score = movesLater - movesNow	#Add gained moves
			score += (covLater - covNow)*2	#Add gained friendly covers *2
			score += (thrNow - thrLater)*2	#Smaller scalar to account for threat value
			return score	#return heuristic score for move
	def getThreats(self, board):
		opMoves,_ = board.get_moves((self.pl+1)%2)	#Get potential moves by opponent
		count = 0
		for p in opMoves:
			for m in opMoves[p]:
				if board.board[m[0]][m[1]]!=None and board.board[m[0]][m[1]].pl==self.pl:	#If enemy piece can move to take friendly piece
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
	def getPriority(self, piece, board = None):
		if board == None:
			board = self.board
		threats = 0	#Count threats to this piece
		covers = 0	#Count how many friendlies protect this piece
		_, cov = board.get_moves(piece.pl)
		opMoves,_ = board.get_moves((piece.pl+1)%2)
		for p in opMoves:
			for m in opMoves[p]:
				if m[0]==piece.x and m[1]==piece.y:	#If enemy piece threatens this piece
					threats += 1
		for p in cov:
			for cp in cov[p]:
				if cp == piece:	#If friendly piece covers this piece
					covers += 1
		return (threats-covers)*getValue(piece)	#returns threat level weighed by piece value
	def doDef(self, piece, move, maxPr):
		score = 0
		board2 = deepcopy(self.board)	#Copy board
		board2.make_move(piece, move)
		maxPr2 = (None, -9999)	#Check most priority after move
		for i in board2.board:	#Rows
			for j in i:	#Pieces
				if j == None:	#If no piece is there, ignore
					continue
				if j.pl == self.pl:
					pr = self.getPriority(j,board2)
					if pr > maxPr2[1]:
						maxPr2 = (j,pr)
		if maxPr2[1]<maxPr[1]:	#MaxPriority has fallen
			score = maxPr2[1]-maxPr[1]
		return score
	def doAtt(self, maxPr, moves, cov):	#Chooses which piece to use to take enemy piece
		mFinal = (maxPr[0].x, maxPr[0].y)
		score = (None, -9999)
		pieces = []
		for p in moves:
			for m in moves[p]:
				if m == mFinal:
					pieces.append(p)
		for p in pieces:
			sc = getValue(maxPr[0])	#Initialize on piece value
			sc -= getValue(p)	#Prefer using pieces with low value
			sc -= len(cov.get(p,[]))	#Prefer using pieces that do not defend others
			if sc > score[1]:
				score = (p, sc)
		res = (score[0], mFinal, score[1]+14)	#Add value to show the benefit of a good offense!
		print("Best offensive move: "+str(res))
		return res
	def minMoves(self, moves, cov):
		opMoves = len(self.board.get_moves((self.player+1)%2))	#How many possible moves opponent has
		covNow = self.getCovers(self.board, cov)	#How well are friendly pieces covered
		best = (None, None, opMoves, covNow)
		for p in moves:
			for m in moves[p]:
				res = self.getOpMoves(p,m)
				if best[0] is None:	#Make sure we have 'a' turn to make
					best = res
					continue
				elif res[2]==0:	#Checkmate.
					return res
				elif res[2]<best[2]:
					if random()*(res[3]/best[3])>0.4:	#Make a judgment call according to possible loss in defense
						best = res
		return best
	def getOpMoves(self, piece, move):
		board2 = deepcopy(self.board)
		board2.make_move(piece, move)
		opMoves = len(board2.get_moves((self.pl+1)%2))
		_, c = board2.get_moves(self.pl)
		covLater = self.getCovers(board2,c)
		return (piece, move, opMoves, covLater)
