import numpy as np
from GeneralGame import Game, Action, Agent

# Did not implement special moves (castling or en-passant)
# Also, allows Agent to move into mate.
class Chess(Game):
	white_king = "♔" #1
	white_queen = "♕" #2
	white_rook = "♖" #3
	white_bishop = "♗" #4
	white_knight = "♘" #5
	white_pawn = "♙" #6

	black_king = "♚" #7
	black_queen = "♛" #8
	black_rook = "♜" #9
	black_bishop = "♝" #10
	black_knight = "♞" #11
	black_pawn = "♟" #12

	pieces = [" ", white_king, white_queen, white_rook, white_bishop, white_knight, white_pawn,
					black_king, black_queen, black_rook, black_bishop, black_knight, black_pawn]

	def initGameState(self, args):
		# Black on top, white on bottom
		self.game_state = np.zeros((8, 8), dtype=np.int)
		self.game_state[0] = [9, 11, 10, 8, 7, 10, 11, 9]
		self.game_state[1] = [12, 12, 12, 12, 12, 12, 12, 12]
		self.game_state[6] = [6, 6, 6, 6, 6, 6, 6, 6]
		self.game_state[7] = [3, 5, 4, 2, 1, 4, 5, 3]

	def copyAndSave(self):
		self.game_history.append(self.game_state)
		self.game_state = np.array([[self.game_state[i][j] for j in range(8)] for i in range(8)])

	def isTerminalState(self):
		if not any(1 in row for row in self.game_state):
			return 2
		if not any(7 in row for row in self.game_state):
			return 1

	def takeAction(self, action):
		piece = self.game_state[action.fromRow][action.fromCol]
		self.game_state[action.toRow][action.toCol] = piece
		self.game_state[action.fromRow][action.fromCol] = 0

		# Promotion
		if self.game_state[action.toRow][action.toCol] == 6 and action.toRow == 7:
			self.game_state[action.toRow][action.toCol] = 2
		if self.game_state[action.toRow][action.toCol] == 12 and action.toRow == 0:
			self.game_state[action.toRow][action.toCol] = 8

	def printGame(self):
		print(" " + ("_ " * 8))
		for row in self.game_state:
			print("|" + "|".join(Chess.pieces[e] for e in row) + "|")
		print(" " + ("‾ " * 8))

def isWhite(p):
		return p <= 6 and p != 0
def isBlack(p):
		return p > 6

class ChessAction(Action):

	def initAction(self, args):
		self.fromRow = args['FROM_ROW']
		self.fromCol = args['FROM_COL']
		self.toRow = args['TO_ROW']
		self.toCol = args['TO_COL']
		self.player = args['PLAYER']

	def isValidAction(self, game):
		player = self.player
		fr = self.fromRow
		fc = self.fromCol
		tr = self.toRow
		tc = self.toCol
		from_cell = game.game_state[fr][fc]
		to_cell = game.game_state[tr][tc]

		# Valid space
		if fr < 0 or fr >= 8:
			return False
		if fc < 0 or fc >= 8:
			return False
		if tr < 0 or tr >= 8:
			return False
		if tc < 0 or tc >= 8:
			return False

		# Valid piece
		if from_cell < 0 or from_cell > 12:
			return False
		if to_cell < 0 or to_cell > 12:
			return False

		# Moving one of your own pieces into a space not occupied by another of your pieces
		if from_cell == 0:
			return False
		if player != 1 and player != 2:
			return False
		if player == 1 and isBlack(from_cell):
			return False
		if player == 2 and isWhite(from_cell):
			return False
		if isWhite(from_cell) and isWhite(to_cell): # Also catches not moving
			return False
		if isBlack(from_cell) and isBlack(to_cell):
			return False

		# Movements each piece can make
		if from_cell == 1 or from_cell == 7: # King
			if abs(fr - tr) <= 1 and abs(fc - tc) <= 1:
				return False
		elif from_cell == 2 or from_cell == 8: # Queen
			if fr == tr and not np.any(game.game_state[fr, min(fc, tc) + 1: max(fc, tc)]):
				return True
			if fc == tc and not np.any(game.game_state[min(fr, tr) + 1: max(fr, tr), fc]):
				return True
			row_dist = abs(fr - tr)
			col_dist = abs(fc - tc)
			if row_dist == col_dist:
				r_step = np.sign(tr - fr)
				c_step = np.sign(tc - fc)
				row = fr + r_step
				col = fc + c_step
				while row != tr and col != tc:
					if game.game_state[row][col] != 0:
						return False
					else:
						row += r_step
						col += c_step
				return True
		elif from_cell == 3 or from_cell == 9: # Rook
			if fr == tr and not np.any(game.game_state[fr, min(fc, tc) + 1: max(fc, tc)]):
				return True
			if fc == tc and not np.any(game.game_state[min(fr, tr) + 1: max(fr, tr), fc]):
				return True
		elif from_cell == 4 or from_cell == 10: # Bishop
			row_dist = abs(fr - tr)
			col_dist = abs(fc - tc)
			if row_dist == col_dist:
				r_step = np.sign(tr - fr)
				c_step = np.sign(tc - fc)
				row = fr + r_step
				col = fc + c_step
				while row != tr and col != tc:
					if game.game_state[row][col] != 0:
						return False
					else:
						row += r_step
						col += c_step
				return True
		elif from_cell == 5 or from_cell == 11: # Knight
			if abs(fr - tr) == 1 and abs(fc - tc) == 2:
				return True
			if abs(fr - tr) == 2 and abs(fc - tc) == 1:
				return True
		elif from_cell == 6 or from_cell == 12: # Pawn
			if isWhite(from_cell):
				if to_cell == 0 and fc == tc: # Move Straight
					if tr - fr == -1:
						return True
					if fr == 6 and tr - fr == -2:
						return True
				else: # Move Diagonally
					if abs(fc - tc) == 1 and tr - fr == -1 and isBlack(from_cell):
						return True
			else:
				if to_cell == 0 and fc == tc: # Move Straight
					if tr - fr == 1:
						return True
					if fr == 1 and tr - fr == 2:
						return True
				else: # Move Diagonally
					if abs(fc - tc) == 1 and tr - fr == 1 and isWhite(from_cell):
						return True

		return False

class RandomChessAgent(Agent):

	def initAgent(self, args):
		pass

	def getNextAction(self, game):
		if not isinstance(game, Chess):
			raise Exception("This agent is meant for Chess!")
		else:
			validAction = False
			action = None
			while not validAction:
				sample =  np.random.randint(8, size = 4)
				args = {'FROM_ROW': sample[0], 'FROM_COL': sample[1], 'TO_ROW': sample[2], 'TO_COL': sample[3], 'PLAYER': self.id}
				action = ChessAction(self, args)
				if action.isValidAction(game):
					validAction = True
			return action


if __name__ == "__main__":
	game = Chess(None)
	p1 = RandomChessAgent(1, None)
	p2 = RandomChessAgent(2, None)
	game.addPlayer(p1)
	game.addPlayer(p2)
	game.run(debug=True)