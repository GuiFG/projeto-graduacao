from State import State
from MonteCarlo import MCTS 
from MonteCarloMinimax import MCTSMinimax

def move_mcts(board, player):
    state = State(board)
    mcts = MCTS(state, player)
    mcts.run(1000)
    mcts_move = mcts.next_move()

    return mcts_move 

def move_mcts_minimax(board, player):
    state = State(board)
    mcts_minimax = MCTSMinimax(state, player, 2)
    mcts_minimax.run(1000)

    move = mcts_minimax.next_move()

    return move 