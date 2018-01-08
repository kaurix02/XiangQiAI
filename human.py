class Human:
	def __init__(self, pl, board):
		self.pl = pl
		self.board = board
		print(self)
	def __str__(self):
		return "Human player, side: "+str(self.pl)
	def move(self):
		print("Available moves:")
		moves,_ = self.board.get_moves(self.pl)
		for i in moves:
			print(i, moves[i])
		self.mymove = input("Your move: ")
		while not self.check_move(self.mymove,moves):
			self.mymove = input("This move is not possible. Your move: ")
		print("Making move "+str(self.mymove)+".")
		self.board.make_move(self.mymove[0],self.mymove[1])
	def check_move(self, move, moves):
		move = move.strip().split()
		can_do = False
		if len(move) == 3:
			for p in moves:
				if str(p)==move[0]:
					if (int(move[1]),int(move[2])) in moves[p]:
						self.mymove = (p,(int(move[1]),int(move[2])))
						return True
		if len(move) == 4:
			for p in moves:
				if p.x==int(move[0]) and p.y == int(move[1]):
					if (int(move[2]),int(move[3])) in moves[p]:
						return True
		return False
