"""
Responsible for storing information about the current state of game
Responsible for determining valid moves at current state
Also keep a move log
"""

class GameState():
	def __init__(self):
		# Numpy serait plus rapide, mais bon
		self.board = [
			["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
			["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
			["--", "--", "--", "--", "--", "--", "--", "--"],
			["--", "--", "--", "--", "--", "--", "--", "--"],
			["--", "--", "--", "--", "--", "--", "--", "--"],
			["--", "--", "--", "--", "--", "--", "--", "--"],
			["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
			["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
		]
		# Map lettre et la fonction pour mouvoir cette pièce
		self.moveFunctions = {
			'p': self.getPawnMoves, 
			'R': self.getRookMoves,
			'N': self.getKnightMoves,
			'B': self.getBishopMoves,
			'Q': self.getQueenMoves,
			'K': self.getKingMoves
		}
		self.whiteToMove = True
		self.moveLog = []

		self.whiteKingLocation = (7,4)
		self.blackKingLocation = (0,4)

		# Old version - simple algo
		# self.checkMate = False
		# self.staleMate = False

		self.inCheck = False
		# Les pins sont des pièces qui ne peuvent pas bouger car elles protègent le roi
		self.pins = []
		self.checks = []
	
	def makeMove(self, move):
		self.board[move.endRow][move.endCol] = move.pieceMoved
		self.board[move.startRow][move.startCol] = "--"
		self.moveLog.append(move) #log pour revenir en arrière ou afficher historique
		self.whiteToMove = not self.whiteToMove # joué, donc on change de joueur

		# on update l'enregistrement du king locations
		if move.pieceMoved == "wK":
			self.whiteKingLocation = (move.endRow, move.endCol)

		elif move.pieceMoved == "bK":
			self.blackKingLocation = (move.endRow, move.endCol)

	def undoMove(self):
		if len(self.moveLog) != 0:
			move = self.moveLog.pop() # On remove puis on récupère le move grâce à pop
			self.board[move.startRow][move.startCol] = move.pieceMoved
			self.board[move.endRow][move.endCol] = move.pieceCaptured
			self.whiteToMove = not self.whiteToMove # On reswitch back le tour du joueur
			# on update king locations
			if move.pieceMoved == "wK":
				self.whiteKingLocation = (move.startRow, move.startCol)

			elif move.pieceMoved == "bK":
				self.blackKingLocation = (move.startRow, move.startCol)
			
	"""
	All moves considering checks
	"""
	### Old version is in doc
	def getValidMoves(self):
		moves = []
		self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
		if self.whiteToMove:
			kingRow = self.whiteKingLocation[0]
			kingCol = self.whiteKingLocation[1]
		else:
			kingRow = self.blackKingLocation[0]
			kingCol = self.blackKingLocation[1]
		if self.inCheck:
			if len(self.checks) == 1: #only 1 check, either block check or move king
				moves = self.getAllPossibleMoves()
				# to block a check you must move a piece into one of the square between enemy piece and king
				check = self.checks[0]
				checkRow = check[0]
				checkCol = check[1]
				pieceChecking = self.board[checkRow][checkCol]
				validSquares = [] # squares that pieces can move to
				# if knight, must capture knight or move king, other pieces can be blocked

				if pieceChecking[1] == 'N':
					validSquares = [(checkRow, checkCol)]
				else:
					pass

	def checkForPinsAndChecks(self):
		pins = [] # squares where the allied pinned piece is and direction pinned from
		checks = []
		inCheck = False

		if self.whiteToMove:
			enemyColor = "b"
			allyColor = "w"
			startRow = self.whiteKingLocation[0]
			startCol = self.whiteKingLocation[1]
		else:
			enemyColor = "w"
			allyColor = "b"
			startRow = self.blackKingLocation[0]
			startCol = self.blackKingLocation[1]
		# check outward from king pins and checks, keep track of pins 
		directions = ((-1,0), (0,-1), (1,0), (0,1), (-1,-1), (-1,1), (1, -1), (1,1))
		for j in range(len(directions)):
			d = directions[j]
			possiblePin = () # reset possible pins
			for i in range(1,8):
				endRow = startRow + d[0] * i
				endCol = startCol + d[1] * i
			
	"""
	Determine si l'ennemi met en échec le roi 	
	"""
	def inCheck(self):
		if self.whiteToMove:
			return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
		else:
			return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])	
	
	def squareUnderAttack(self, r, c):
		self.whiteToMove = not self.whiteToMove
		oppMoves = self.getAllPossibleMoves()

		self.whiteToMove = not self.whiteToMove 
		for move in oppMoves:
			if move.endRow == r and move.endCol == c:
				return True
		return False

	"""
	Ici, on considère qu'on pion peut bouger même si il met en échec son propre roi.
	"""
	def getAllPossibleMoves(self):
		moves = []

		for r in range(len(self.board)):
			for c in range(len(self.board[r])):
				turn = self.board[r][c][0]
				if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
					piece = self.board[r][c][1]
					self.moveFunctions[piece](r, c, moves) # appel le bon 
		return moves

	def getPawnMoves(self, r, c, moves):
		# - Les noirs et les blancs movent différemment (ce sont les seuls) et 
		# - ne peuvent pas revenir en arrière
		# - Les captures sont sur la diagonale
		if self.whiteToMove:
			if self.board[r-1][c] == "--": # il avance
				moves.append(Move((r, c), (r-1, c), self.board))
				if r == 6 and self.board[r-2][c] == "--": # Depuis case de départ pion peut avancer de 2
					moves.append(Move((r, c), (r-2, c), self.board))
			# Pour éviter les débordements sur des colonnes inexistantes
			# par la gauche du board
			if c-1 >= 0: 
				if self.board[r-1][c-1][0] == 'b': # Il y a un ennemi à prendre
					moves.append(Move((r,c), (r-1, c-1), self.board))
			# Par la droite cette fois
			if c+1 <= 7:
				if self.board[r-1][c+1][0] == 'b': # Il y a un ennemi à prendre
					moves.append(Move((r,c), (r-1, c+1), self.board))

		else:
			if self.board[r+1][c] == "--": # il avance
				moves.append(Move((r, c), (r+1, c), self.board))
				if r == 1 and self.board[r+2][c] == "--": # Depuis case de départ pion peut avancer de 2
					moves.append(Move((r, c), (r+2, c), self.board))
			# Débordement par la gauche du board
			if c-1 >= 0: 
				if self.board[r+1][c-1][0] == 'w': # Il y a un ennemi à prendre
					moves.append(Move((r,c), (r+1, c-1), self.board))
			# Par la droite cette fois
			if c+1 <= 7:
				if self.board[r+1][c+1][0] == 'w': # Il y a un ennemi à prendre
					moves.append(Move((r,c), (r+1, c+1), self.board))



	def getRookMoves(self, r, c, moves):
		directions = ((-1,0), (0,-1), (1,0), (0,1)) # Up, left, down, right
		enemyColor = "b" if self.whiteToMove else "w"

		for d in directions:
			for i in range(1,8):
				# Le 0 dans direction est important, puisque ça permet de ne pas se déplacer
				endRow = r + d[0] * i
				endCol = c + d[1] * i
				if 0 <= endRow < 8 and 0 <= endCol < 8:
					endPiece = self.board[endRow][endCol] 
					if endPiece == "--":
						moves.append(Move((r, c), (endRow, endCol), self.board))
					elif endPiece[0] == enemyColor:
						moves.append(Move((r,c), (endRow, endCol), self.board))
						break # Le break permet de ne pas jump l'ennemi
					else:  # pièce amie
						break
				else: # off the board
					break
	
	def getKnightMoves(self, r, c, moves):
		knightMoves = ((-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1))
		allyColor = "w" if self.whiteToMove else "b"
		# On va créer les 8 moves possibles dans endPiece
		# puis soustraire les moves sur les ally
		# Pas de for i in range(1,8) puisque les seuls move possibles sont listés dans knightMoves
		for m in knightMoves: 
			endRow = r + m[0]
			endCol = c + m[1]
			if 0 <= endRow < 8 and 0 <= endCol < 8:
				endPiece = self.board[endRow][endCol]
				if endPiece[0] != allyColor: # On passe par ally car de toute façon, que ce soit -- ou ennemi ça ne change rien : le cheval peut y aller.
					moves.append(Move((r, c), (endRow, endCol), self.board))
					
	def getBishopMoves(self, r, c, moves):
		directions = ((-1,-1), (-1,1), (1,-1), (1,1)) # On les change simultanément de 1 - 1 => ce qui permet d'aller en diagonale
		enemyColor = "b" if self.whiteToMove else "w"

		for d in directions:
			for i in range(1,8): # le fou ne peut faire que 7 cases 
				endRow = r + d[0] * i
				endCol = c + d[1] * i
				if 0 <= endRow < 8 and 0 <= endCol < 8: # Pour être sur qu'il reste sur le board
					endPiece = self.board[endRow][endCol] 
					if endPiece == "--":
						moves.append(Move((r, c), (endRow, endCol), self.board))	
					elif endPiece[0] == enemyColor: 
						moves.append(Move((r, c), (endRow, endCol), self.board))
						break
					else:  # pièce amie
						break
				else:
					break

	def getQueenMoves(self, r, c, moves):
		self.getRookMoves(r, c, moves)
		self.getBishopMoves(r, c, moves)

	def getKingMoves(self, r, c, moves):
		kingMoves = ((-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1))
		allyColor = "w" if self.whiteToMove else "b"
		for i in range(8):
			endRow = r + kingMoves[i][0]
			endCol = c + kingMoves[i][1]
			if 0 <= endRow < 8 and 0 <= endCol < 8: # Pour être sur qu'il reste sur le board
				endPiece = self.board[endRow][endCol] 
				if endPiece[0] != allyColor:
					moves.append(Move((r, c), (endRow, endCol), self.board))

class Move():
	# maps keys to values - En Chess, on ne parle pas de [0][0] 
	# mais plutôt de A8 par (coordonnées comme bataille navale)
	# La notation est indépendante du move en soi
	ranksToRows = {
		"1": 7, "2": 6, "3": 5, "4": 4,
		"5": 3, "6": 2, "7": 1, "8":0
	}
	rowsToRanks = {v: k for k, v in ranksToRows.items()}

	filesToCols = {
		"a": 0, "b": 1, "c": 2, "d": 3,
		"e": 4, "f": 5, "g": 6, "h": 7
	}
	colsToFiles = {v: k for k, v in filesToCols.items()}

	def __init__(self, startSq, endSq, board):
		# On décompose le premier click et le deuxième du tuple playerClicks()
		self.startRow = startSq[0]
		self.startCol = startSq[1]
		self.endRow = endSq[0]
		self.endCol = endSq[1]
		self.pieceMoved = board[self.startRow][self.startCol]
		self.pieceCaptured = board[self.endRow][self.endCol]
		self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol
		print(self.moveID)
	"""
	Overriding the equals method
	"""
	def __eq__(self, other):
		if isinstance(other, Move):
			return self.moveID == other.moveID
		return False

	def getChessNotation(self):
		return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

	def getRankFile(self, r, c):
		return self.colsToFiles[c] + self.rowsToRanks[r]