from State import State
from MonteCarlo import MCTS 

def move_mcts(board, player):
    state = State(board)
    mcts = MCTS(state, player)
    mcts.run(1000)
    mcts_move = mcts.next_move()

    return mcts_move 