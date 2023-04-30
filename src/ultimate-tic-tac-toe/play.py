'''

File running the main game loop

Author: @vaibhav.garg
Date: 4th Aug'20
'''

from colorama import Fore, Style
from bigBoard import BigBoard
from mcts import MCTS
from human import Human
from copy import *


def evaluate_state(board):
	board.print()
	curState = board.getState()
	if curState[0] == 'W':
		return curState[1]
	elif curState[0] == 'D':
		return 'D'


def game(p1, p2):
	board = BigBoard()

	p1_symbol = 'X'
	p2_symbol = 'O'

	result = None 
	prevMove = None
	while True:
		# P1 turn
		print("It is P1's turn now.")
		move = p1.getMove(deepcopy(board), prevMove)
		board.playMove(move, p1_symbol)
		print("Move played by p1:", move)

		prevMove = move
		result = evaluate_state(board)
		if result:
			break
		
		# P2 turn
		print("It is P2's turn now.")
		move = p2.getMove(deepcopy(board), prevMove)
		board.playMove(move, p2_symbol)
		print("Move played by p2:", move)

		prevMove = move
		result = evaluate_state(board)
		if result:
			break
	
	if result == p1_symbol:
		print('P1 won!')
	elif result == p2_symbol:
		print('P2 won!')
	else:
		print('Draw!')
		


def main():
	print(Fore.RED + "Ultimate TicTacToe")
	print(Style.RESET_ALL)

	p1 = MCTS('X', compTime=0.1) 
	p2 = Human('O')	

	game(p1, p2)
	
	
main()