from montecarlo import *

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
		state = State(board, opponent_player(self.symbol), prevMove)
		mcts = MonteCarloTreeSearch(state)
		print('simulating')
		mcts.run(1000)
		try:
			print('next_move')
			move = mcts.next_move() #list(map(int, input().split()))
			print('move')
			return move
		except:
			return self.getMove(board)