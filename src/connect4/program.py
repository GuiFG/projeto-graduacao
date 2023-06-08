import numpy as np
import random
import pygame
import sys
import math

from constants import *
from utils import *
from PlayerAI import Player

from datetime import datetime
from Metrics import *

def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def print_board(board):
	print(np.flip(board, 0))

def game(id, player1, player2):
	game_over = False
	turn = PLAYER
	board = create_board()
	
	metric_game = []
	player_win = 0
	round = 1
	while not game_over:
		if turn == PLAYER and not game_over:
			metric = get_metrics_game(id)
			metric['player'] = player1['name']
			metric['round'] = round
			total_empty_cells = count_empty_cells(board)
			metric['empty_cells'] = total_empty_cells

			player = Player(board, PLAYER_PIECE, player1['id'])

			start = datetime.now()
			col = player.get_action()
			end = datetime.now() - start
			metric['time'] = end.total_seconds()

			metric_game.append(metric)

			if is_valid_location(board, col):
				row = get_next_open_row(board, col)
				drop_piece(board, row, col, PLAYER_PIECE)

				if winning_move(board, PLAYER_PIECE):
					game_over = True
					player_win = PLAYER_PIECE

				turn += 1
				turn = turn % 2

				# print_board(board)
		
		## Ask for Player 2 Input
		if turn == OPPONENT and not game_over:
			metric = get_metrics_game(id)
			metric['player'] = player2['name']
			metric['round'] = round
			total_empty_cells = count_empty_cells(board)
			metric['empty_cells'] = total_empty_cells

			player = Player(board, OPPONENT_PIECE, player2['id'])

			start = datetime.now()
			col = player.get_action()
			end = datetime.now() - start
			metric['time'] = end.total_seconds()

			metric_game.append(metric)
			
			
			if is_valid_location(board, col):
				row = get_next_open_row(board, col)
				drop_piece(board, row, col, OPPONENT_PIECE)

				if winning_move(board, OPPONENT_PIECE):
					game_over = True
					player_win = OPPONENT_PIECE

				# print_board(board)

				turn += 1
				turn = turn % 2

		if not game_over:
			game_over = not has_empty_cells(board)
		
		round += 1

	return player_win, board, metric_game

def main():
	total = 1
	players = get_players()
	matchups = get_matchups(players)
	
	metrics_matchup = []
	metrics_game = []
	counter = 0
	start_tournement = datetime.now()
	for match in matchups:
		random.seed(42)
		player1 = match[0]
		player2 = match[1]

		match_players = player1['name'] + ' X ' + player2['name']
		print(match_players)		
		for i in range(total):
			count = f'{i+1}/{total}'
			metrics = { 'id' : counter + 1, 'time' : 0, 'winner': '', 'player1': player1['name'], 'player2': player2['name'], 'count': count, 'empty_cells' : 0 }

			game_start = datetime.now()
			player_win, board, metric_game = game(counter + 1, player1, player2)
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

	time_elapsed = datetime.now() - start_tournement
	print(time_elapsed)
	
	save_metrics_game(metrics_game)
	save_metrics_matchup(metrics_matchup)
		
if __name__ == "__main__":
	main()