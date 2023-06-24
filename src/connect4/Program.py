import numpy as np
import random
from datetime import datetime

from constants import *
from utils import *

from Metrics import *
from PlayerAI import Player

metrics_matchup = []
metrics_game = []
counter = 0

def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def print_board(board):
	print(np.flip(board, 0))

def play_player(board, player_id, player_piece):
	player = Player(board, player_piece, player_id)

	start = datetime.now()
	col = player.get_action()
	end = datetime.now() - start
	time = end.total_seconds()

	if is_valid_location(board, col):
		row = get_next_open_row(board, col)
		drop_piece(board, row, col, player_piece)
	
	return time 

def game(id, players):
	game_over = False
	turn = PLAYER
	board = create_board()
	
	metric_game = []
	player_win = 0
	round = 1
	while not game_over:
		metric = get_game_metrics(id, round)

		for idx_player in range(len(players)):
			player = players[idx_player]
			player_piece = PLAYER_PIECE if turn == PLAYER else OPPONENT_PIECE

			metric['player'] = player['name']
			metric['empty_cells'] = count_empty_cells(board)
			metric['time'] = play_player(board, player['id'], player_piece)
			metric_game.append(metric)

			if winning_move(board, player_piece):
				player_win = player_piece
				game_over = True
				break 
			
			turn += 1
			turn = turn % 2

		if not game_over:
			game_over = not has_empty_cells(board)
		
		round += 1

	return player_win, board, metric_game

def run_match(match, total):
	player1 = match[0]
	player2 = match[1]

	global counter
	print(player1['name'] + ' X ' + player2['name'])
	for i in range(total):
		count_matchs = f'{i+1}/{total}'
		print(f'match {count_matchs}')
		metrics = get_match_metrics(counter + 1, player1, player2, count_matchs)

		game_start = datetime.now()
		player_win, board, metric_game = game(counter + 1, [player1, player2])
		game_end = datetime.now() - game_start
		metrics['time'] = game_end.total_seconds()

		if player_win == PLAYER_PIECE:
			print(player1['name'], 'wins')
			metrics['winner'] = player1['name']
		elif player_win == OPPONENT_PIECE:
			print(player2['name'], 'wins')
			metrics['winner'] = player2['name']
		else:
			print('draw')

		total_empty_cells = count_empty_cells(board)
		metrics['empty_cells'] = total_empty_cells

		print(game_end)
		metrics_matchup.append(metrics)
		metrics_game.extend(metric_game)
		counter += 1

def main(config):
	total = config['game_total']
	seed = config['seed']
	set_data_idx = config['set_data_idx']
	tournament = config['tournament']

	players = get_players(set_data_idx)
	matchups = get_matchups(players, tournament)

	start_tournement = datetime.now()
	count = 0
	for match in matchups:
		print(f'matchup {count+1}/{len(matchups)}')
		random.seed(seed)
		run_match(match, total)
		print()

		count += 1
		
	time_elapsed = datetime.now() - start_tournement
	print(time_elapsed)
	
	save_game_metrics(metrics_game, set_data_idx)
	save_matchup_metrics(metrics_matchup, set_data_idx)
		
if __name__ == "__main__":
	config = get_json('config.json')
	main(config)