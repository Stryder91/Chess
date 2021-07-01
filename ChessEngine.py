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
		self.whiteToMove = True
		self.moveLog = []
	
	def makeMove(self, move):
		self.board[move.startRow][move.startCol] = "--"
		self.board[move.endRow][move.endCol] = move.pieceMoved
		self.moveLog.append(move) #log pour revenir en arrière ou afficher historique
		self.whiteToMove = not self.whiteToMove # joué, donc on change de joueur

	def undoMove(self):
		if len(self.moveLog) != 0:
			move = self.moveLog.pop() # On remove puis on récupère le move grâce à pop
			self.board[move.startRow][move.startCol] = move.pieceMoved
			self.board[move.endRow][move.endCol] = move.pieceCaptured
			self.whiteToMove = not self.whiteToMove # On reswitch back le tour du joueur
		
	"""
	All moves considering checks
	"""
	def getValidMoves(self):
		return self.getAllPossibleMoves()

	"""
	Ici, on considère qu'on pion peut bouger même si il met en échec son propre roi.
	"""
	def getAllPossibleMoves(self):
		moves = [Move((6,4), (4,4), self.board)]

		for r in range(len(self.board)):
			for c in range(len(self.board[r])):
				turn = self.board[r][c][0]
				if (turn == 'w' and self.whiteToMove) and (turn == 'b' and not self.whiteToMove):
					piece = self.board[r][c][1]
					if piece == 'p':
						self.getPawnMoves(r, c, moves)
					elif piece == 'R':
						self.getRookMoves(r, c, moves)
					elif piece == 'R':
						self.getRookMoves(r, c, moves)
					elif piece == 'R':
						self.getRookMoves(r, c, moves)
					elif piece == 'R':
						self.getRookMoves(r, c, moves)
		return moves
	def getPawnMoves(self, r, c, moves):
		pass

	def getRookMoves(self, r, c, moves):
		pass



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