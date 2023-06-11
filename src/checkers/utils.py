
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
    if board[old_i][old_j][0] == player_piece or board[old_i][old_j][0] == player_piece.upper():
        return False
    if board[new_i][new_j] == EMPTY_SQUARE:
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

                elif board[m][n][0] == BLACK_PIECE:
                    if check_moves(board, previous_move, [m - 1, n - 1], BLACK_PIECE):
                        available_moves.append([m, n, m - 1, n - 1])
                    if check_moves(board, previous_move, [m - 1, n + 1], BLACK_PIECE):
                        available_moves.append([m, n, m - 1, n + 1])

                    if check_jumps(board, previous_move, [m - 1, n - 1], [m - 2, n - 2], BLACK_PIECE):
                        available_jumps.append([m, n, m - 2, n - 2])
                    if check_jumps(board, previous_move, [m - 1, n + 1], [m - 2, n + 2], BLACK_PIECE):
                        available_jumps.append([m, n, m - 2, n + 2])
                    if check_moves(board, previous_move, [m + 1, n - 1], BLACK_PIECE):
                        available_moves.append([m, n, m + 1, n - 1])
                    if check_jumps(board, previous_move, [m + 1, n - 1], [m + 2, n - 2], BLACK_PIECE):
                        available_jumps.append([m, n, m + 2, n - 2])
                    if check_moves(board, previous_move, [m + 1, n + 1], BLACK_PIECE):
                        available_moves.append([m, n, m + 1, n + 1])
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

            elif board[m][n][0] == WHITE_PIECE:
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
    return find_black_available_moves(board, mandatory_jumping) if player_piece == BLACK_PIECE else find_white_available_moves(board, mandatory_jumping)
    

def make_a_move(board, old_i, old_j, new_i, new_j, big_letter, queen_row):
    letter = board[old_i][old_j][0]
    i_difference = old_i - new_i
    j_difference = old_j - new_j
    if i_difference == -2 and j_difference == 2:
        board[old_i + 1][old_j - 1] = EMPTY_SQUARE

    elif i_difference == 2 and j_difference == 2:
        board[old_i - 1][old_j - 1] = EMPTY_SQUARE

    elif i_difference == 2 and j_difference == -2:
        board[old_i - 1][old_j + 1] = EMPTY_SQUARE

    elif i_difference == -2 and j_difference == -2:
        board[old_i + 1][old_j + 1] = EMPTY_SQUARE

    if new_i == queen_row:
        letter = big_letter
    board[old_i][old_j] = "---"
    board[new_i][new_j] = letter + str(new_i) + str(new_j)

def make_move(board, move, player=BLACK_PIECE):
    queen_row = get_queen_row(player)

    make_a_move(board, move[0], move[1], move[2], move[3], player, queen_row)


def get_queen_row(player):
    return 7 if player == WHITE_PIECE else 0


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
