import os
from datetime import datetime
import time

from colorama import Fore, Style
from bigBoard import BigBoard
from copy import *

from PlayerAI import *
from Metrics import *

matchup_metrics = []
game_metrics = []
game_counter = 0


def evaluate_state(board):
	board.print()
	curState = board.getState()
	if curState[0] == 'W':
		return curState[1]
	elif curState[0] == 'D':
		return 'D'
	
def execute_move(board, player, symbol, prevMove):
	start_action = datetime.now()
	move = player.get_action(deepcopy(board), prevMove)
	end_action = datetime.now() - start_action
	
	board.playMove(move, symbol)
	
	return move, end_action.total_seconds()

def game(id, players):
	board = BigBoard()

	symbols = ['X', 'O']

	round = 1
	game_metrics = []
	result = None 
	prevMove = None
	game_over = False 
	winner_idx = 0
	while not game_over:
		for idx in range(len(players)):
			player = players[idx]
			symbol = symbols[idx]
			
			p = Player(player['id'], symbol)
			game_metric = get_game_metrics(id, player['name'], round)
			print(f"It is P{idx+1}'s turn now.")
			prevMove, time = execute_move(board, p, symbol, prevMove)
			print(f"Move played by p{idx+1}:", prevMove)

			game_metric['time'] = time 
			game_metrics.append(game_metric)

			result = evaluate_state(board)
			if result:
				winner_idx = idx + 1
				game_over = True
				break
		
		round += 1
	
	winner = players[winner_idx-1]['name'] if winner_idx != 0 else 'draw'

	print(winner + ' won!' if winner_idx != 0 else winner)

	return winner, game_metrics
		

def run_match(match, total):
	player1 = match[0]
	player2 = match[1]

	global game_counter

	print(player1['name'] + ' X ' + player2['name'])
	for i in range(total):
		time.sleep(2)
		match_metrics = get_match_metrics(game_counter + 1, player1, player2, f'{i+1}/{total}')
		game_start = datetime.now()
		winner, game_metric = game(game_counter, [player1, player2])
		game_end = datetime.now() - game_start
		print(game_end)

		match_metrics['time'] = game_end.total_seconds()
		match_metrics['winner'] = winner

		game_metrics.extend(game_metric)
		matchup_metrics.append(match_metrics)
		game_counter += 1

def main(config):
	total = config['game_total']
	seed = config['seed']
	set_data_idx = config['set_data_idx']

	print(Fore.RED + "Ultimate TicTacToe")
	print(Style.RESET_ALL)

	players = get_players(set_data_idx)
	matchups = get_matchups(players)

	start_tournement = datetime.now()
	count = 0
	for match in matchups:
		random.seed(seed)
		run_match(match, total)

		if count + 1 != len(matchups):
			time.sleep(5)
			os.system('cls' if os.name == 'nt' else 'clear')
		count += 1
	
	time_elapsed = datetime.now() - start_tournement
	print(time_elapsed)

	save_game_metrics(game_metrics, set_data_idx)
	save_matchup_metrics(matchup_metrics, set_data_idx)

if __name__ == "__main__":
	config = get_json('config.json')
	main(config)
