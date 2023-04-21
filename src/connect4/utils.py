from constants import *
import numpy as np

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
    
    return False

def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_terminal_node(board):
	return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations
            
def opponent_player(piece):
    if piece == 1:
        return 2
    return 1

def count_player(line, player):
    count = 0
    op_count = 0
    count_empty = 0

    op = opponent_player(player)
    for cell in line:
        if cell == player:
            count += 1
        elif cell == 0:
            count_empty += 1
        elif cell == op:
             op_count += 1
        
    return count, op_count, count_empty

def get_sub_board(board, row, col):
    subboard = []
    for i in range(row + 4):
        line = []
        for j in range(col + 4):
            line.append(board[i][j])
        
        subboard.append(line)
    
    return subboard