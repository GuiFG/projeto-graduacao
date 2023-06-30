from datetime import datetime
import sys

from bigBoard import BigBoard
from copy import *

from PlayerAI import *
from Metrics import *


def evaluate_state(board):
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
			game_metric = get_game_metrics(id, round)
			prevMove, time = execute_move(board, p, symbol, prevMove)

			game_metric['player'] = player['name']
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
		

def run_match(matchup_counter, match, total, set_data_idx):
	player1 = match[0]
	player2 = match[1]

	match_name = player1['name'] + '_X_' + player2['name']
	for i in range(total):
		count_matchs = f'{i+1}/{total}'
		match_id = matchup_counter + match_name + "_" + str((i + 1))
		print('matchup ' + matchup_counter + " | " + match_name + " | " + f'match {count_matchs}' + " | " + match_id)

		match_metric = get_match_metrics(match_id, player1, player2, count_matchs)
		
		game_start = datetime.now()
		winner, game_metric = game(match_id, [player1, player2])
		game_end = datetime.now() - game_start
		print(game_end)

		match_metric['time'] = game_end.total_seconds()
		match_metric['winner'] = winner

		save_game_metrics(game_metric, set_data_idx)
		save_matchup_metrics(match_metric, set_data_idx)

def main(config):
	total = config['game_total']
	matchup_start = config['matchup_start']
	seed = config['seed']
	set_data_idx = config['set_data_idx']
	tournament = config['tournament']

	players = get_players(set_data_idx)
	matchups = get_matchups(players, tournament)

	start_tournement = datetime.now()
	try:
		count = 0
		for match in matchups:
			matchup_counter = f'{count+1}/{len(matchups)}'
			count += 1
			if count < matchup_start:
				continue

			random.seed(seed)
			run_match(matchup_counter, match, total, set_data_idx)
			print()
		
		time_elapsed = datetime.now() - start_tournement
		print(time_elapsed)
	except Exception as error:
		print("Ocorreu um erro durante o torneio: ", error)
		exc_type, _, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)

		print(datetime.now() - start_tournement)

if __name__ == "__main__":
	config = get_json('config.json')
	main(config)
