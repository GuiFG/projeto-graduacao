from State import State
from Algorithms.Minimax import Minimax
from Algorithms.PodaAlfaBeta import PodaAlfaBeta
from Algorithms.MonteCarlo import MCTS
from Algorithms.MonteCarloMinimax import MCTSMinimax


class Player():
    def minimax(board, player):
        state = State(board)
        minimax = Minimax(state, player)
        action = minimax.search()
        
        return action 
    
    def alfa_beta(board, player):
        state = State(board)
        alfa_beta = PodaAlfaBeta(state, player)
        action = alfa_beta.search()

        return action
        
    def mcts(board, player):
        state = State(board)
        mcts = MCTS(state, player)
        mcts.run(1000)
        action = mcts.next_move()

        return action

    def mcts_minimax(board, player):
        state = State(board)
        mcts_minimax = MCTSMinimax(state, player, 2)
        mcts_minimax.run(1000)
        action = mcts_minimax.next_move()

        return action 