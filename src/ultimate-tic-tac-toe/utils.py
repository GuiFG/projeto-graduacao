def opponent_player(player):
    return 'O' if player == 'X' else 'X'


def is_terminal_node(board):
    curState = board.getState()

    return curState[0] == 'W' or curState[0] == 'D'

def get_valid_moves(board, prevMove):
    return board.getValidMoves(prevMove)[0]
