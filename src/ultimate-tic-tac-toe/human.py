from State import State
from MonteCarlo import MCTS
from MonteCarloMinimax import MCTSMinimax

from utils import *

'''
Human player class definition

author: @vaibhav.garg
date: 4th Aug'20
'''

class Human():
	
	def __init__(self, symbol):
		
		self.symbol = symbol

	def getMove(self, board, prevMove):

		print("Enter 2 space separated integers of the form: [0-8] [0-8], corresponding to a valid move ofCourse!")
		
		print('mcts')
		state = State(board, prevMove)
		
		try:
			#move = self.getMoveMcts(state)
			move = self.getMoveMctsMinimax(state)
			return move
		except:
			return self.getMove(board)
		
	
	def getMoveMcts(self, state):
		mcts = MCTS(state, self.symbol)
		print('simulating')
		mcts.run(1000)

		print('next_move')
		move = mcts.next_move() 
		
		return move 

	def getMoveMctsMinimax(self, state):
		mcts_minimax = MCTSMinimax(state, self.symbol, 2)

		print('simulating')
		mcts_minimax.run(1000)

		print('next_move')
		move = mcts_minimax.next_move() 

		return move 
