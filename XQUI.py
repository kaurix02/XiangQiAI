import tkinter as tk
from tkinter import messagebox
from play import players
from board import Board

class XiangQi():
	def __init__(self, pl2, master=None):
		self.master = master
		self.board = Board()
		self.pl2 = players[pl2](1, self.board)  # Turn class into object for player2
		self.background_image = tk.PhotoImage(file="images/board.gif")	#Use board as bgd
		# self.background_label = tk.Label(self.master, image=self.background_image, width=580, height=640)
		self.canvas = tk.Canvas(self.master, width=580, height=640)
		self.canvas.pack()
		# self.background_label.place(x=0, y=0, width=580, height=640)
		self.getImages()	#Dict of images
		self.moves = 0
		self.m_fr = None
		self.play()
	def getImages(self):	#Helper method that adds an image reference to each piece
		self.im = {}
		self.im["FF"] = tk.PhotoImage(file="images/FF.gif")	#Free tile
		for p in self.board.get_pieces(0):
			self.im[str(p)] = tk.PhotoImage(file="images/"+p.name+"0.gif")
		for p in self.board.get_pieces(1):
			self.im[str(p)] = tk.PhotoImage(file="images/"+p.name+"1.gif")
	def play(self):
		self.board.is_checkmate()
		if self.board.won is None:  # While game continues...
			if self.board.player == 0:
				self.moves += 1
				print("Player turn")
				self.draw()

				if self.moves > 300:
					print("### Game too long! ###")
					self.board.won = 2
			else:
				self.pl2.move()
				self.play()
		else:
			self.draw()
			if self.board.won == 2:
				messagebox.showinfo("Game over", "stalemate!")
				print("Game over, stalemate!")
				self.master.destroy()
			else:
				if self.board.won == 0:
					messagebox.showinfo("Game over", "you win!")
				else:
					messagebox.showinfo("Game over", "you lose :(")
				print("Game over, winner: " + str(self.board.won))
				self.master.destroy()
	def draw(self):
		self.canvas.delete("all")
		self.canvas.update_idletasks()
		self.canvas.create_image(0,0,image=self.background_image,anchor='nw')
		self.avail_moves,_ = self.board.get_moves()
		for i in range(10):	#Row
			for j in range(9):	#Column
				if self.board.board[i][j] is None:	#Empty
					t = self.canvas.create_image(50+j*60,590-i*60, image=self.im["FF"])
					self.canvas.tag_bind(t,"<Button-1>",lambda x:self.click(x)) #self.moveTo(i,j))
					#tk.Button(self.master, command=lambda: self.moveTo(i,j), width=5, height=5, image=None, bd=0).grid(row=9-i,column=j)
				elif self.board.board[i][j].pl == self.board.player:	#Friendly
					#tk.Button(self.master, command=lambda: self.moveFrom(self.board.board[i][j]), image=self.im[str(self.board.board[i][j])], bd=0).grid(row=9-i,column=j)
					t = self.canvas.create_image(50+j*60,590-i*60,image=self.im[str(self.board.board[i][j])])
					self.canvas.tag_bind(t,"<Button-1>",lambda x:self.click(x))
				else:	#Hostile
					#tk.Button(self.master, command=lambda: self.moveTo(i,j), image=self.im[str(self.board.board[i][j])], bd=0).grid(row=9-i,column=j)
					t = self.canvas.create_image(50+j*60,590-i*60,image=self.im[str(self.board.board[i][j])])
					self.canvas.tag_bind(t,"<Button-1>",lambda x:self.click(x))
	def click(self, event):
		b,a= int((event.x-20)/60), int((event.y-20)/60)
		a = 9-a
		print(a,b)
		if self.board.board[a][b] is None:
			self.moveTo(a,b)
		elif self.board.board[a][b].pl == self.board.player:
			self.moveFrom(self.board.board[a][b])
		else:
			self.moveTo(a,b)
	def moveFrom(self, piece):
		print("Moving with "+str(piece))
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
				print("Bad move: ",x,y)
r=tk.Tk()
app = XiangQi(1,r)
#r.master.title("XiangQi")
r.mainloop()
