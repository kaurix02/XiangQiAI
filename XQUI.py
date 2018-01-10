import tkinter as tk
from play import players
from board import Board

class XiangQi():
	def __init__(self, pl2, master=None):
		self.master = master
		self.board = Board()
		self.pl2 = players[pl2](1, self.board)  # Turn class into object for player2
		self.background_image = tk.PhotoImage("images/board.gif")	#Use board as bgd
		self.background_label = tk.Label(self.master, image=self.background_image)
		self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
		self.getImages()	#Dict of images
		self.moves = 0
		self.play()
	def getImages(self):	#Helper method that adds an image reference to each piece
		self.im = {}
		for p in self.board.get_pieces(0):
			self.im[str(p)] = tk.PhotoImage(file="images/"+p.name+"0.gif")
		for p in self.board.get_pieces(1):
			self.im[str(p)] = tk.PhotoImage(file="images/"+p.name+"1.gif")
	def play(self):
		if self.board.won is None:  # While game continues...
			if self.board.player == 0:
				self.moves += 1
				print("Player turn")
				self.avail_moves,_ = self.board.get_moves()
				self.draw()
			else:
				pl2.move()		
			self.board.is_checkmate()
			if self.moves > 300:
				print("### Game too long! ###")
				self.board.won = 2
		else:
			self.draw()
			if self.board.won == 2:
				print("Game over, stalemate!")
			else:
				print("Game over, winner: " + str(self.board.won))
	def draw(self):
		for i in range(10):	#Row
			for j in range(9):	#Column
				if self.board.board[i][j] is None:	#Empty
					tk.Button(self.master, command=lambda: self.moveTo(i,j), width=5, height=5, image=None).grid(row=9-i,column=j)
				elif self.board.board[i][j].pl == self.board.player:	#Friendly
					tk.Button(self.master, command=lambda: self.moveFrom(self.board.board[i][j]), image=self.im[str(self.board.board[i][j])]).grid(row=9-i,column=j)
				else:	#Hostile
					tk.Button(self.master, command=lambda: self.moveTo(i,j), image=self.im[str(self.board.board[i][j])]).grid(row=9-i,column=j)
		self.m_fr = None
	def moveFrom(self, piece):
		print("Moving with "+str(piece)
		self.m_fr = piece
	def moveTo(self, x, y):
		if self.m_fr is None:	#No piece selected, do nothing.
			return
		if self.m_fr in self.avail_moves:
			if (x,y) in self.avail_moves[self.m_fr]:
				print("YAY")
				self.board.make_move(self.m_fr,x,y)
				self.play()
			else:
				print(x,y)
		print(self.m_fr)
r=tk.Tk()
app = XiangQi(1,r)
#r.master.title("XiangQi")
r.mainloop()
