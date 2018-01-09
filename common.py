# common constants for different models to use

#General piece values (SR is Soldier who has crossed river), according to wiki:
values = {"S":1.0, "SR":2.0, "A":2.0, "E":2.0, "H":4.0, "C":4.5, "R":9, "G":100}
def getValue(piece):	#Return piece value
	if piece.name == "S":	#Check if my Soldier has crossed river
		if piece.pl==0 and piece.x>4:
			return values["SR"]
		elif piece.pl==1 and piece.x<5:
			return values["SR"]
	return values[piece.name]
