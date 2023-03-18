from checkers import Checkers

import time 


def is_terminal_node(board, player):
    moves = get_valid_moves(board, player)

    if len(moves) == 0:
        return True 
    
    opponent_moves = get_valid_moves(board, opponent_player(player))
    return len(opponent_moves) == 0


def opponent_player(player):
    return "C" if player == "B" else "B"

def get_valid_moves(board, player):
    if player == "B":
        return Checkers.find_player_available_moves(board, True)

    return Checkers.find_available_moves(board, True)


def make_move(board, move, player="B"):
    queen_row = get_queen_row(player)

    Checkers.make_a_move(
        board, move[0], move[1], move[2], move[3], player, queen_row)


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
