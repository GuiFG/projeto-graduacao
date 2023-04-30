from State import State
from Algorithms.MonteCarlo import MCTS
from Algorithms.HAlfaBeta import HAlfaBeta

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
			move = self.h_alfa_beta(state, 4)
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
	
	def h_alfa_beta(self, state, depth):
		h_alfa_beta = HAlfaBeta(state, self.symbol, depth)

		action = h_alfa_beta.search()

		return action
		