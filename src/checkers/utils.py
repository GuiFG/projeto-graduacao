
BLACK_PIECE = "B"
WHITE_PIECE = "C"
EMPTY_SQUARE = "---"

MAX_POSITION_REPEAT = 3

def is_terminal_node(board, positions):
    player = BLACK_PIECE
    moves = find_available_moves(board, player)
    
    if len(moves) == 0:
        return True
    
    opponent_moves = find_available_moves(board, opponent_player(player))
    if len(opponent_moves) == 0:
        return True 
    
    return check_draw(positions)

def opponent_player(player):
    return WHITE_PIECE if player == BLACK_PIECE else BLACK_PIECE
        
def check_moves(board, previous_move, move, player_piece):
    old_i = previous_move[0]
    old_j = previous_move[1]
    new_i = move[0]
    new_j = move[1]
    
    if new_i > 7 or new_i < 0:
        return False
    if new_j > 7 or new_j < 0:
        return False
    if board[old_i][old_j] == EMPTY_SQUARE:
        return False
    if board[new_i][new_j] != EMPTY_SQUARE:
        return False
    if board[old_i][old_j][0] == opponent_player(player_piece).lower() or board[old_i][old_j][0] == opponent_player(player_piece).upper():
        return False
    
    return True

def check_jumps(board, previous_move, via_move, move, player_piece):
    old_i = previous_move[0]
    old_j = previous_move[1]
    via_i = via_move[0]
    via_j = via_move[1]
    new_i = move[0]
    new_j = move[1]


    if new_i > 7 or new_i < 0:
        return False
    if new_j > 7 or new_j < 0:
        return False
    if board[via_i][via_j] == EMPTY_SQUARE:
        return False
    if board[via_i][via_j][0] == player_piece or board[via_i][via_j][0] == player_piece.upper():
        return False
    if board[new_i][new_j] != EMPTY_SQUARE:
        return False
    if board[old_i][old_j] == EMPTY_SQUARE:
        return False
    if board[old_i][old_j][0] == opponent_player(player_piece).lower() or board[old_i][old_j][0] == opponent_player(player_piece):
        return False
    
    return True

def find_black_available_moves(board, mandatory_jumping):
        available_moves = []
        available_jumps = []
        for m in range(8):
            for n in range(8):
                previous_move = [m, n]
                if board[m][n][0] == BLACK_PIECE.lower():
                    if check_moves(board, previous_move, [m - 1, n - 1], BLACK_PIECE):
                        available_moves.append([m, n, m - 1, n - 1])
                    if check_moves(board, previous_move, [m - 1, n + 1], BLACK_PIECE):
                        available_moves.append([m, n, m - 1, n + 1])

                    if check_jumps(board, previous_move, [m - 1, n - 1], [m - 2, n - 2], BLACK_PIECE):
                        available_jumps.append([m, n, m - 2, n - 2])
                    if check_jumps(board, previous_move, [m - 1, n + 1], [m - 2, n + 2], BLACK_PIECE):
                        available_jumps.append([m, n, m - 2, n + 2])

                elif board[m][n][0] == BLACK_PIECE.upper():
                    if check_moves(board, previous_move, [m - 1, n - 1], BLACK_PIECE):
                        available_moves.append([m, n, m - 1, n - 1])
                    if check_moves(board, previous_move, [m - 1, n + 1], BLACK_PIECE):
                        available_moves.append([m, n, m - 1, n + 1])
                    if check_moves(board, previous_move, [m + 1, n - 1], BLACK_PIECE):
                        available_moves.append([m, n, m + 1, n - 1])
                    if check_moves(board, previous_move, [m + 1, n + 1], BLACK_PIECE):
                        available_moves.append([m, n, m + 1, n + 1])

                    if check_jumps(board, previous_move, [m - 1, n - 1], [m - 2, n - 2], BLACK_PIECE):
                        available_jumps.append([m, n, m - 2, n - 2])
                    if check_jumps(board, previous_move, [m - 1, n + 1], [m - 2, n + 2], BLACK_PIECE):
                        available_jumps.append([m, n, m - 2, n + 2])
                    if check_jumps(board, previous_move, [m + 1, n - 1], [m + 2, n - 2], BLACK_PIECE):
                        available_jumps.append([m, n, m + 2, n - 2])
                    if check_jumps(board, previous_move, [m + 1, n + 1], [m + 2, n + 2], BLACK_PIECE):
                        available_jumps.append([m, n, m + 2, n + 2])

        if mandatory_jumping is False:
            available_jumps.extend(available_moves)
            return available_jumps
        elif mandatory_jumping is True:
            if len(available_jumps) == 0:
                return available_moves
            else:
                return available_jumps

def find_white_available_moves(board, mandatory_jumping = True):
    available_moves = []
    available_jumps = []
    for m in range(8):
        for n in range(8):
            previous_move = [m, n]
            if board[m][n][0] == WHITE_PIECE.lower():
                if check_moves(board, previous_move, [m+1, n+1], WHITE_PIECE):
                    available_moves.append([m, n, m + 1, n + 1])
                if check_moves(board, previous_move, [m + 1, n - 1], WHITE_PIECE):
                    available_moves.append([m, n, m + 1, n - 1])

                if check_jumps(board, previous_move, [m + 1, n - 1], [m + 2, n - 2], WHITE_PIECE):
                    available_jumps.append([m, n, m + 2, n - 2])
                if check_jumps(board, previous_move, [m + 1, n + 1], [m + 2, n + 2], WHITE_PIECE):
                    available_jumps.append([m, n, m + 2, n + 2])

            elif board[m][n][0] == WHITE_PIECE.upper():
                if check_moves(board, previous_move, [m + 1, n + 1], WHITE_PIECE):
                    available_moves.append([m, n, m + 1, n + 1])
                if check_moves(board, previous_move, [m + 1, n - 1], WHITE_PIECE):
                    available_moves.append([m, n, m + 1, n - 1])
                if check_moves(board, previous_move, [m - 1, n - 1], WHITE_PIECE):
                    available_moves.append([m, n, m - 1, n - 1])
                if check_moves(board, previous_move, [m - 1, n + 1], WHITE_PIECE):
                    available_moves.append([m, n, m - 1, n + 1])

                if check_jumps(board, previous_move, [m + 1, n - 1], [m + 2, n - 2], WHITE_PIECE):
                    available_jumps.append([m, n, m + 2, n - 2])
                if check_jumps(board, previous_move, [m - 1, n - 1], [m - 2, n - 2], WHITE_PIECE):
                    available_jumps.append([m, n, m - 2, n - 2])
                if check_jumps(board, previous_move, [m - 1, n + 1], [m - 2, n + 2], WHITE_PIECE):
                    available_jumps.append([m, n, m - 2, n + 2])
                if check_jumps(board, previous_move, [m + 1, n + 1], [m + 2, n + 2], WHITE_PIECE):
                    available_jumps.append([m, n, m + 2, n + 2])
    
    if mandatory_jumping is False:
        available_jumps.extend(available_moves)
        return available_jumps
    elif mandatory_jumping is True:
        if len(available_jumps) == 0:
            return available_moves
        else:
            return available_jumps

def find_available_moves(board, player_piece, mandatory_jumping = True):
    return find_black_available_moves(board, mandatory_jumping) if player_piece.lower() == BLACK_PIECE.lower() else find_white_available_moves(board, mandatory_jumping)
    
def make_a_move(board, old_i, old_j, new_i, new_j, big_letter, queen_row):
    letter = board[old_i][old_j][0]
    i_difference = old_i - new_i
    j_difference = old_j - new_j

    capture = False

    if i_difference == -2 and j_difference == 2:
        board[old_i + 1][old_j - 1] = EMPTY_SQUARE
        capture = True
    elif i_difference == 2 and j_difference == 2:
        board[old_i - 1][old_j - 1] = EMPTY_SQUARE
        capture = True
    elif i_difference == 2 and j_difference == -2:
        board[old_i - 1][old_j + 1] = EMPTY_SQUARE
        capture = True
    elif i_difference == -2 and j_difference == -2:
        board[old_i + 1][old_j + 1] = EMPTY_SQUARE
        capture = True

    if new_i == queen_row:
        letter = big_letter
    board[old_i][old_j] = "---"
    board[new_i][new_j] = letter + str(new_i) + str(new_j)

    return capture

def make_move(board, move, player=BLACK_PIECE):
    queen_row = get_queen_row(player)

    return make_a_move(board, move[0], move[1], move[2], move[3], player.upper(), queen_row)

def get_queen_row(player):
    return 7 if player.lower() == WHITE_PIECE.lower() else 0

def print_board(board):
    i = 0
    print()
    for row in board:
        print(i, end="  |")
        i += 1
        for elem in row:
            print(elem, end=" ")
        print()
    print()
    for j in range(8):
        if j == 0:
            j = "     0"
        print(j, end="   ")
    print("\n")

def count_pieces_by_player(matrix, player):
    count_pieces = 0
    for m in range(8):
        for n in range(8):
            if matrix[m][n][0].lower() == player.lower():
                count_pieces += 1
    
    return count_pieces


def count_pieces(matrix):
    black_pieces = 0
    white_pieces = 0

    for m in range(8):
        for n in range(8):
            if matrix[m][n][0] == BLACK_PIECE.upper() or matrix[m][n][0] == BLACK_PIECE.lower():
                black_pieces += 1
            elif matrix[m][n][0] == WHITE_PIECE.upper() or matrix[m][n][0] == WHITE_PIECE.lower():
                white_pieces += 1

    return black_pieces, white_pieces

def player_most_pieces(black_pieces, white_pieces):
        if black_pieces > white_pieces:
            return BLACK_PIECE
        elif white_pieces > black_pieces:
            return WHITE_PIECE
        else:
            return EMPTY_SQUARE

def check_winner(matrix, black_pieces, white_pieces, mandatory_jumping=True):
        if black_pieces == 0 or white_pieces == 0:
            return player_most_pieces(black_pieces, white_pieces)

        available_moves = find_available_moves(
            matrix, BLACK_PIECE, mandatory_jumping)
        if len(available_moves) == 0:
            return player_most_pieces(black_pieces, white_pieces)

        available_moves = find_available_moves(
            matrix, WHITE_PIECE, mandatory_jumping)
        if len(available_moves) == 0:
            return player_most_pieces(black_pieces, white_pieces)

        return None

def convert_matrix_to_state(matrix):
    matrix_state = ''
    for i in range(8):
        for j in range(8):
            matrix_state += matrix[i][j]
    
    return matrix_state

def update_positions(matrix, positions):
    matrix_state = convert_matrix_to_state(matrix)

    total_positions = MAX_POSITION_REPEAT * 2
    if len(positions) > total_positions:
        positions.pop(0)

    positions.append(matrix_state)

def check_draw(positions):
    counter = dict((p, positions.count(p)) for p in positions)

    for value in counter.values():
        if value > MAX_POSITION_REPEAT:
            return True

    return False

''' EVALUATION STATE '''

def get_type_score(board, player):
    score = 0
    for i in range(8):
        for j in range(8):
            piece = board[i][j][0]
            if piece == player.lower():
                score += 5
            elif piece == player.upper():
                score += 20
    
    return score

def get_localization_score(board, player):
    localization_score = 0

    op_player = opponent_player(player)
    min_idx, max_idx = get_index_region_by_player(op_player)

    # pieces in the opponent area
    for i in range(min_idx, max_idx + 1):
        for j in range(8):
            piece = board[i][j][0]
            if piece.lower() == player.lower():
                localization_score += 3
    
    # pieces on the side 
    cols = [0, 7]
    for col in cols:
        for i in range(8):
            piece = board[i][col][0]
            if piece.lower() == player.lower():
                localization_score += 2

    # pieces on bottom
    bottom_line_idx = get_bottom_idx_by_player(player)
    for j in range(8):
        piece = board[bottom_line_idx][j][0]
        if piece.lower() == player.lower():
            localization_score += 1
    
    return localization_score

def get_layout_jump_score(board, player):
    layout_score = 0
    jump_score = 0
    for i in range(8):
        for j in range(8):
            piece = board[i][j][0]
            if piece.lower() == player.lower():
                count = count_pieces_surround(board, i, j, player)
                layout_score += count

                available_jumps = get_available_jumps(board, i, j, player)
                if len(available_jumps) > 0:
                    for jump in available_jumps:
                        if jump[-1]:
                            jump_score += 7
                        else:
                            jump_score += 3

    return layout_score, jump_score 

def count_pieces_surround(board, line, col, player):
    count = 0
    offsets = [(-1, -1), (-1, 1), (1, 1), (1, -1)]

    for offset in offsets:
        exist = exist_piece(board, line + offset[0], col + offset[1], player)
        if exist:
            count += 1
    
    return count       

def exist_piece(board, line, col, player):
    if line > 7 or line < 0 or col < 0 or col > 7:
        return False

    return board[line][col].lower() == player.lower()

def get_index_region_by_player(player):
    return (0, 3) if player.lower() == WHITE_PIECE.lower() else (4, 7)

def get_bottom_idx_by_player(player):
    return 7 if player.lower() == BLACK_PIECE.lower() else 0

def get_available_jumps(board, m, n, player):
    available_jumps = []
    
    previous_move = [m, n]
    if player.lower() == WHITE_PIECE.lower():
        if player.islower():
            if check_jumps(board, previous_move, [m + 1, n - 1], [m + 2, n - 2], WHITE_PIECE):
                available_jumps.append([m + 2, n - 2, is_queen(board, m+1, n-1)])
            if check_jumps(board, previous_move, [m + 1, n + 1], [m + 2, n + 2], WHITE_PIECE):
                available_jumps.append([m + 2, n + 2, is_queen(board, m+1, n+1)])
        else:
            if check_jumps(board, previous_move, [m + 1, n - 1], [m + 2, n - 2], WHITE_PIECE):
                available_jumps.append([m + 2, n - 2, is_queen(board, m+1, n-1)])
            if check_jumps(board, previous_move, [m - 1, n - 1], [m - 2, n - 2], WHITE_PIECE):
                available_jumps.append([m - 2, n - 2, is_queen(board, m-1, n-1)])
            if check_jumps(board, previous_move, [m - 1, n + 1], [m - 2, n + 2], WHITE_PIECE):
                available_jumps.append([m - 2, n + 2, is_queen(board, m-1, n+1)])
            if check_jumps(board, previous_move, [m + 1, n + 1], [m + 2, n + 2], WHITE_PIECE):
                available_jumps.append([m + 2, n + 2, is_queen(board, m+1, n+1)])
    else:
        if player.islower():
            if check_jumps(board, previous_move, [m - 1, n - 1], [m - 2, n - 2], BLACK_PIECE):
                available_jumps.append([m - 2, n - 2, is_queen(board, m-1, n-1)])
            if check_jumps(board, previous_move, [m - 1, n + 1], [m - 2, n + 2], BLACK_PIECE):
                available_jumps.append([m - 2, n + 2, is_queen(board, m-1, n+1)])
        else:
            if check_jumps(board, previous_move, [m - 1, n - 1], [m - 2, n - 2], BLACK_PIECE):
                available_jumps.append([m - 2, n - 2, is_queen(board, m-1, n-1)])
            if check_jumps(board, previous_move, [m - 1, n + 1], [m - 2, n + 2], BLACK_PIECE):
                available_jumps.append([m - 2, n + 2, is_queen(board, m-1, n+1)])
            if check_jumps(board, previous_move, [m + 1, n - 1], [m + 2, n - 2], BLACK_PIECE):
                available_jumps.append([m + 2, n - 2, is_queen(board, m+1, n-1)])
            if check_jumps(board, previous_move, [m + 1, n + 1], [m + 2, n + 2], BLACK_PIECE):
                available_jumps.append([m + 2, n + 2, is_queen(board, m+1, n+1)])

    return available_jumps

def is_queen(board, m, n):
    piece = board[m][n]
    if piece.lower() == WHITE_PIECE.lower():
        return piece == WHITE_PIECE.upper()
    
    return piece == BLACK_PIECE.upper()

def flatten_board(board):
    flattened = [cell for row in board for cell in row]
    return ''.join(flattened) 

def get_start_game():
    matrix = [[], [], [], [], [], [], [], []]
    for row in matrix:
        for i in range(8):
            row.append(EMPTY_SQUARE)
    
    position_black(matrix)
    position_white(matrix)
    
    return matrix

def print_board(matrix):
    i = 0
    print()
    for row in matrix:
        print(i, end="  |")
        i += 1
        for elem in row:
            print(elem, end=" ")
        print()
    print()
    for j in range(8):
        if j == 0:
            j = "     0"
        print(j, end="   ")
    print("\n")

def position_white(matrix):
    for i in range(3):
        for j in range(8):
            if (i + j) % 2 == 1:
                matrix[i][j] = (WHITE_PIECE.lower() + str(i) + str(j))

def position_black(matrix):
    for i in range(5, 8, 1):
        for j in range(8):
            if (i + j) % 2 == 1:
                matrix[i][j] = (BLACK_PIECE.lower() + str(i) + str(j))