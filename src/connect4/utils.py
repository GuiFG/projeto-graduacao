from constants import *
import numpy as np
import itertools

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
	return winning_move(board, PLAYER_PIECE) or winning_move(board, OPPONENT_PIECE) or len(get_valid_locations(board)) == 0

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
    for i in range(row, row + 4):
        line = []
        for j in range(col, col + 4):
            line.append(board[i][j])
        
        subboard.append(line)
    
    return subboard

def evaluate_window(window, piece):
	score = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = OPPONENT_PIECE

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4

	return score

def score_position(board, piece):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	## Score Horizontal
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score Vertical
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score posiive sloped diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score

def get_matchups(players):
    combinations = list(itertools.combinations(players, 2))

    matchups = []
    for comb in combinations:
        player1 = comb[0]
        player2 = comb[1]

        if player1['type'] == player2['type']:
            continue 

        matchups.append(comb)
        revert = (comb[1], comb[0])
        matchups.append(revert)
    
    return matchups

def has_empty_cells(board):
    for i in range(6):
        for j in range(7):
            if board[i][j] == 0:
                return True 
    
    return False 