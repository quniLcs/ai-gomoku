# from logger import Logger


class AlphaBetaAgent:
	max_depth = 5
	# logger = Logger()

	def search(self, board):
		_, action = self.max_value(board, -float('inf'), float('inf'), 0)
		return action

	def max_value(self, board, alpha, beta, depth):
		if depth >= self.max_depth:
			utility = board.get_utility()
			action = None
		else:
			utility = -float('inf')
			action = None
			for x, y in board.get_actions(1):
				original_score1, original_score2 = board.make_move(x, y, 1)
				new_utility, _ = self.min_value(board, alpha, beta, depth + 1)
				board.take_back(1, original_score1, original_score2)
				if new_utility > utility:
					utility = new_utility
					action = (x, y)
				if utility >= beta:
					return utility, action
				if utility > alpha:
					alpha = utility
		return utility, action

	def min_value(self, board, alpha, beta, depth):
		if depth >= self.max_depth:
			utility = board.get_utility()
			action = None
		else:
			utility = float('inf')
			action = None
			for x, y in board.get_actions(2):
				original_score1, original_score2 = board.make_move(x, y, 2)
				new_utility, _ = self.max_value(board, alpha, beta, depth + 1)
				board.take_back(2, original_score1, original_score2)
				if new_utility < utility:
					utility = new_utility
					action = (x, y)
				if utility <= alpha:
					return utility, action
				if utility < beta:
					beta = utility
		return utility, action
