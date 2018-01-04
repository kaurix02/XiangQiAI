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
			print(i)
		mymove = input("Your move: ").trim().split()
		while mymove not in moves:
			mymove = input("This move is not possible. Your move: ").trim().split()
		print("Making move "+str(mymove)+".")
		self.board.makemove(mymove[0:2],mymove[2:])
