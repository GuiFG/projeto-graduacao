import numpy as np
import random
import pygame
import sys
import math

from constants import *
from utils import *
from PlayerAI import Player

from datetime import datetime
import json

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


def game(player1, player2):
	game_over = False
	turn = PLAYER #random.randint(PLAYER, OPPONENT)
	board = create_board()
	#draw_board(board)
	#pygame.display.update()

	player_win = 0
	while not game_over:

		if turn == PLAYER and not game_over:
			player = Player(board, PLAYER_PIECE, player1)
			col = player.get_action()

			if is_valid_location(board, col):
				row = get_next_open_row(board, col)
				drop_piece(board, row, col, PLAYER_PIECE)

				if winning_move(board, PLAYER_PIECE):
					#label = myfont.render("Player 1 wins!!", 1, RED)
					#screen.blit(label, (40,10))
					game_over = True
					player_win = PLAYER_PIECE

				turn += 1
				turn = turn % 2

				#print_board(board)
				draw_board(board)
		
		## Ask for Player 2 Input
		if turn == OPPONENT and not game_over:
			player = Player(board, OPPONENT_PIECE, player2)
			col = player.get_action()
			#col = random.randint(0, COLUMN_COUNT-1)
			#col = pick_best_move(board, OPPONENT_PIECE)
			#actions = get_valid_locations(board)
			#col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

			if is_valid_location(board, col):
				#pygame.time.wait(500)
				row = get_next_open_row(board, col)
				drop_piece(board, row, col, OPPONENT_PIECE)

				if winning_move(board, OPPONENT_PIECE):
					#label = myfont.render("Player 2 wins!!", 1, YELLOW)
					#screen.blit(label, (40,10))
					game_over = True

					player_win = OPPONENT_PIECE

				#print_board(board)
				draw_board(board)

				turn += 1
				turn = turn % 2

		if not game_over:
			game_over = not has_empty_cells(board)

	return player_win

def get_players():
	f = open('players.json')
	
	data = json.load(f)
	
	f.close()

	return data 

def save_metrics(metric_games):
	with open('result.json', 'w') as f:
		print(metric_games)
		json_result = json.dumps(metric_games)
		f.write(json_result)

def main(total):
	players = get_players()
	matchups = get_matchups(players)
	
	metric_games = []
	for match in matchups:
		player1 = match[0]
		player2 = match[1]

		match_players = player1['name'] + ' X ' + player2['name']
		print(match_players)

		score = { player1['name']: 0, player2['name']: 0, 'draw': 0 }
		for i in range(total):
			count = f'{i+1}/{total}'
			metrics = { 'time' : 0, 'winner': '', 'players': match_players, 'count': count }

			game_start = datetime.now()
			print(count)
			player_win = game(player1['id'], player2['id'])

			if player_win == PLAYER_PIECE:
				print(player1['name'], 'wins')
				score[player1['name']] += 1
				metrics['winner'] = player1['name']
			elif player_win == OPPONENT_PIECE:
				print(player2['name'], 'wins')
				score[player2['name']] += 1
				metrics['winner'] = player2['name']
			else:
				print('draw')
				score['draw'] += 1
				
			game_end = datetime.now() - game_start
			metrics['time'] = str(game_end)
			print(game_end)

			metric_games.append(metrics)

	save_metrics(metric_games)
		
main(5)