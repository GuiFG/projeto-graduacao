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

def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, OPPONENT_PIECE):
				return (None, 100000000000000)
			elif winning_move(board, PLAYER_PIECE):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, OPPONENT_PIECE))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, OPPONENT_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, PLAYER_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

def pick_best_move(board, piece):

	valid_locations = get_valid_locations(board)
	best_score = -10000
	best_col = random.choice(valid_locations)
	for col in valid_locations:
		row = get_next_open_row(board, col)
		temp_board = board.copy()
		drop_piece(temp_board, row, col, piece)
		score = score_position(temp_board, piece)
		if score > best_score:
			best_score = score
			best_col = col

	return best_col

def draw_board(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			if board[r][c] == PLAYER_PIECE:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == OPPONENT_PIECE:
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()


pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)

myfont = pygame.font.SysFont("monospace", 75)


def game(id, player1, player2):
	game_over = False
	turn = PLAYER
	board = create_board()
	
	metric_game = []
	player_win = 0
	round = 1
	while not game_over:
		if turn == PLAYER and not game_over:
			metric = get_metrics_game(id, round)
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

				draw_board(board)
		
		## Ask for Player 2 Input
		if turn == OPPONENT and not game_over:
			metric = get_metrics_game(id, round)
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

				draw_board(board)

				turn += 1
				turn = turn % 2

		if not game_over:
			game_over = not has_empty_cells(board)
		
		round += 1

	return player_win, board, metric_game

def main(args):
	total = int(args[0])
	set_player_idx = int(args[1])

	players = get_players(set_player_idx)
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
	
	save_metrics_game(metrics_game, set_player_idx)
	save_metrics_matchup(metrics_matchup, set_player_idx)
		

if __name__ == "__main__":
	main(sys.argv[1:])