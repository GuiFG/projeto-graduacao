import numpy as np
import random
from datetime import datetime
import sys

from constants import *
from utils import *

from Metrics import *
from PlayerAI import Player

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
		player_win, board, game_metric = game(match_id, [player1, player2])
		game_end = datetime.now() - game_start
		match_metric['time'] = game_end.total_seconds()

		if player_win == PLAYER_PIECE:
			print(player1['name'], 'wins')
			match_metric['winner'] = player1['name']
		elif player_win == OPPONENT_PIECE:
			print(player2['name'], 'wins')
			match_metric['winner'] = player2['name']
		else:
			print('draw')

		total_empty_cells = count_empty_cells(board)
		match_metric['empty_cells'] = total_empty_cells
		print(game_end)

		save_game_metrics(game_metric, set_data_idx)
		save_matchup_metrics(match_metric, set_data_idx)


def main(config):
	total = config['game_total']
	matchup_start = config['matchup_start']
	matchup_end = config['matchup_end']
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
			
			if count > matchup_end:
				break
			
			match_total = 1 if match[0]['type'] == 'ALFA_BETA' and match[1]['type'] == 'ALFA_BETA' else total
			random.seed(seed)
			run_match(matchup_counter, match, match_total, set_data_idx)
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