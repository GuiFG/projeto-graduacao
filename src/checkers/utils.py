def is_terminal_node(board):
    player = "B"
    moves = get_valid_moves(board, player)

    if len(moves) == 0:
        return True 
    
    opponent_moves = get_valid_moves(board, opponent_player(player))
    return len(opponent_moves) == 0


def opponent_player(player):
    return "C" if player == "B" else "B"

def check_player_moves(board, old_i, old_j, new_i, new_j):
    if new_i > 7 or new_i < 0:
        return False
    if new_j > 7 or new_j < 0:
        return False
    if board[old_i][old_j] == "---":
        return False
    if board[new_i][new_j] != "---":
        return False
    if board[old_i][old_j][0] == "c" or board[old_i][old_j][0] == "C":
        return False
    if board[new_i][new_j] == "---":
        return True

def check_player_jumps(board, old_i, old_j, via_i, via_j, new_i, new_j):
    if new_i > 7 or new_i < 0:
        return False
    if new_j > 7 or new_j < 0:
        return False
    if board[via_i][via_j] == "---":
        return False
    if board[via_i][via_j][0] == "B" or board[via_i][via_j][0] == "b":
        return False
    if board[new_i][new_j] != "---":
        return False
    if board[old_i][old_j] == "---":
        return False
    if board[old_i][old_j][0] == "c" or board[old_i][old_j][0] == "C":
        return False
    return True


def find_player_available_moves(board, mandatory_jumping):
    available_moves = []
    available_jumps = []
    for m in range(8):
        for n in range(8):
            if board[m][n][0] == "b":
                if check_player_moves(board, m, n, m - 1, n - 1):
                    available_moves.append([m, n, m - 1, n - 1])
                if check_player_moves(board, m, n, m - 1, n + 1):
                    available_moves.append([m, n, m - 1, n + 1])
                if check_player_jumps(board, m, n, m - 1, n - 1, m - 2, n - 2):
                    available_jumps.append([m, n, m - 2, n - 2])
                if check_player_jumps(board, m, n, m - 1, n + 1, m - 2, n + 2):
                    available_jumps.append([m, n, m - 2, n + 2])
            elif board[m][n][0] == "B":
                if check_player_moves(board, m, n, m - 1, n - 1):
                    available_moves.append([m, n, m - 1, n - 1])
                if check_player_moves(board, m, n, m - 1, n + 1):
                    available_moves.append([m, n, m - 1, n + 1])
                if check_player_jumps(board, m, n, m - 1, n - 1, m - 2, n - 2):
                    available_jumps.append([m, n, m - 2, n - 2])
                if check_player_jumps(board, m, n, m - 1, n + 1, m - 2, n + 2):
                    available_jumps.append([m, n, m - 2, n + 2])
                if check_player_moves(board, m, n, m + 1, n - 1):
                    available_moves.append([m, n, m + 1, n - 1])
                if check_player_jumps(board, m, n, m + 1, n - 1, m + 2, n - 2):
                    available_jumps.append([m, n, m + 2, n - 2])
                if check_player_moves(board, m, n, m + 1, n + 1):
                    available_moves.append([m, n, m + 1, n + 1])
                if check_player_jumps(board, m, n, m + 1, n + 1, m + 2, n + 2):
                    available_jumps.append([m, n, m + 2, n + 2])
    if mandatory_jumping is False:
        available_jumps.extend(available_moves)
        return available_jumps
    elif mandatory_jumping is True:
        if len(available_jumps) == 0:
            return available_moves
        else:
            return available_jumps
        
def check_moves(board, old_i, old_j, new_i, new_j):
    if new_i > 7 or new_i < 0:
        return False
    if new_j > 7 or new_j < 0:
        return False
    if board[old_i][old_j] == "---":
        return False
    if board[new_i][new_j] != "---":
        return False
    if board[old_i][old_j][0] == "b" or board[old_i][old_j][0] == "B":
        return False
    if board[new_i][new_j] == "---":
        return True

def check_jumps(board, old_i, old_j, via_i, via_j, new_i, new_j):
    if new_i > 7 or new_i < 0:
        return False
    if new_j > 7 or new_j < 0:
        return False
    if board[via_i][via_j] == "---":
        return False
    if board[via_i][via_j][0] == "C" or board[via_i][via_j][0] == "c":
        return False
    if board[new_i][new_j] != "---":
        return False
    if board[old_i][old_j] == "---":
        return False
    if board[old_i][old_j][0] == "b" or board[old_i][old_j][0] == "B":
        return False
    return True



def find_available_moves(board, mandatory_jumping):
    available_moves = []
    available_jumps = []
    for m in range(8):
        for n in range(8):
            if board[m][n][0] == "c":
                if check_moves(board, m, n, m + 1, n + 1):
                    available_moves.append([m, n, m + 1, n + 1])
                if check_moves(board, m, n, m + 1, n - 1):
                    available_moves.append([m, n, m + 1, n - 1])
                if check_jumps(board, m, n, m + 1, n - 1, m + 2, n - 2):
                    available_jumps.append([m, n, m + 2, n - 2])
                if check_jumps(board, m, n, m + 1, n + 1, m + 2, n + 2):
                    available_jumps.append([m, n, m + 2, n + 2])
            elif board[m][n][0] == "C":
                if check_moves(board, m, n, m + 1, n + 1):
                    available_moves.append([m, n, m + 1, n + 1])
                if check_moves(board, m, n, m + 1, n - 1):
                    available_moves.append([m, n, m + 1, n - 1])
                if check_moves(board, m, n, m - 1, n - 1):
                    available_moves.append([m, n, m - 1, n - 1])
                if check_moves(board, m, n, m - 1, n + 1):
                    available_moves.append([m, n, m - 1, n + 1])
                if check_jumps(board, m, n, m + 1, n - 1, m + 2, n - 2):
                    available_jumps.append([m, n, m + 2, n - 2])
                if check_jumps(board, m, n, m - 1, n - 1, m - 2, n - 2):
                    available_jumps.append([m, n, m - 2, n - 2])
                if check_jumps(board, m, n, m - 1, n + 1, m - 2, n + 2):
                    available_jumps.append([m, n, m - 2, n + 2])
                if check_jumps(board, m, n, m + 1, n + 1, m + 2, n + 2):
                    available_jumps.append([m, n, m + 2, n + 2])
    if mandatory_jumping is False:
        available_jumps.extend(available_moves)
        return available_jumps
    elif mandatory_jumping is True:
        if len(available_jumps) == 0:
            return available_moves
        else:
            return available_jumps

def get_valid_moves(board, player):
    if player == "B":
        return find_player_available_moves(board, True)

    return find_available_moves(board, True)


def make_a_move(board, old_i, old_j, new_i, new_j, big_letter, queen_row):
    letter = board[old_i][old_j][0]
    i_difference = old_i - new_i
    j_difference = old_j - new_j
    if i_difference == -2 and j_difference == 2:
        board[old_i + 1][old_j - 1] = "---"

    elif i_difference == 2 and j_difference == 2:
        board[old_i - 1][old_j - 1] = "---"

    elif i_difference == 2 and j_difference == -2:
        board[old_i - 1][old_j + 1] = "---"

    elif i_difference == -2 and j_difference == -2:
        board[old_i + 1][old_j + 1] = "---"

    if new_i == queen_row:
        letter = big_letter
    board[old_i][old_j] = "---"
    board[new_i][new_j] = letter + str(new_i) + str(new_j)


def make_move(board, move, player="B"):
    queen_row = get_queen_row(player)

    make_a_move(board, move[0], move[1], move[2], move[3], player, queen_row)


def get_queen_row(player):
    return 7 if player == "C" else 0


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
