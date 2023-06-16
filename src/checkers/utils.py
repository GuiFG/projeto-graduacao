
BLACK_PIECE = "B"
WHITE_PIECE = "C"
EMPTY_SQUARE = "---"

def is_terminal_node(board):
    player = BLACK_PIECE
    moves = find_available_moves(board, player)

    if len(moves) == 0:
        return True 
    
    opponent_moves = find_available_moves(board, opponent_player(player))
    return len(opponent_moves) == 0

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



''' EVALUATION STATE '''

def get_type_score(board, player):
    score = 0
    op_player = opponent_player(player)
    for i in range(8):
        for j in range(8):
            piece = board[i][j][0]
            if piece == player.lower():
                score += 5
            elif piece == player.upper():
                score += 17.5
            elif piece == op_player.lower():
                score -= 5
            elif piece == op_player.upper():
                score -= 17.5
    
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
                localization_score += 2
    
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
            localization_score += 0.5
    
    return localization_score

def get_layout_jump_score(board, player):
    layout_score = 0
    jump_score = 0
    for i in range(8):
        for j in range(8):
            piece = board[i][j][0]
            if piece.lower() == player.lower():
                count = count_pieces_surround(board, i, j, player)
                layout_score += (count * 0.3)
                available_jumps = get_available_jumps(board, i, j, player)
                if len(available_jumps) > 0:
                    for jump in available_jumps:
                        if jump[-1]:
                            jump_score += 8.75
                        else:
                            jump_score += 2.5

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

