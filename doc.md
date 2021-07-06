def getValidMoves(self):
		# 1 Générer tous les moves possibles
		moves = self.getAllPossibleMoves()
		# 2 pour chaque move, faire le move
		for i in range(len(moves) -1, -1, -1): # when removing from a list go 
			self.makeMove(moves[i])

			# 3 pour chaque move ennemi, regarde s'ils attaquent le roi
			# 4 S'ils attaquent le roi, ce n'est pas un move valide
			# En faisant le makeMove, on vient de switch le tour
			# mais pourtant on a besoin du move avec la vue du blanc
			self.whiteToMove = not self.whiteToMove 
			if self.inCheck():
				moves.remove(moves[i])
			self.whiteToMove = not self.whiteToMove # Puis on remet pour les noirs
			self.undoMove()

		if len(moves) == 0: #Donc plus aucun move possible

			if self.inCheck():
				self.checkMate = True
			else:
				self.staleMate = True
		else:
			self.checkMate = False
			self.staleMate = False
		return moves		
			
		# return self.getAllPossibleMoves()