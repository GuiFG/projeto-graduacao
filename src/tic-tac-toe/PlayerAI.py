from State import State
from Algorithms.MonteCarlo import MCTS
from Algorithms.MonteCarloMinimax import MCTSMinimax
from Algorithms.Minimax import Minimax

class Player():
    def minimax(board, player):
        state = State(board)
        minimax = Minimax(state, player)

        action = minimax.search()

        return action 

    def mcts(board, player):
        state = State(board)
        mcts = MCTS(state, player)
        mcts.run(2000)
        action = mcts.next_move()

        return action

    def mcts_minimax(board, player):
        state = State(board)
        mcts_minimax = MCTSMinimax(state, player, 2)
        mcts_minimax.run(1000)
        action = mcts_minimax.next_move()

        return action 

