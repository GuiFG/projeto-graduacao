from State import State
from Algorithms.Minimax import Minimax
from Algorithms.PodaAlfaBeta import PodaAlfaBeta
from Algorithms.MonteCarlo import MonteCarlo
from Algorithms.MonteCarloMinimax import MCTSMinimax
from Algorithms.HMinimax import HMinimax
from Algorithms.HAlfaBeta import HAlfaBeta
from constants import *


class Player():
    def __init__(self, board, player, type):
        self.board = board
        self.player = player
        self.type = type

    def get_action(self):
        action = None 
        if self.type == MINIMAX:
            action = self.minimax()
        elif self.type == HMINIMAX:
            action = self.hminimax()
        elif self.type == ALFA_BETA:
            action = self.alfa_beta()
        elif self.type == HALFA_BETA:
            action = self.h_alfa_beta()
        elif self.type == MCTS:
            action = self.mcts()
        elif self.type == MCTS_MINIMAX:
            action = self.mcts_minimax()
        
        return action
             

    def minimax(self):
        state = State(self.board)
        minimax = Minimax(state, self.player)
        action = minimax.search()
        
        return action 
    
    def alfa_beta(self):
        state = State(self.board)
        alfa_beta = PodaAlfaBeta(state, self.player)
        action = alfa_beta.search()

        return action
    
    def hminimax(self):
        state = State(self.board)
        hminimax = HMinimax(state, self.player, 4)
        
        action = hminimax.search()

        return action 
    
    def h_alfa_beta(self):
        state = State(self.board)
        h_alfa_beta = HAlfaBeta(state, self.player, 5)

        action = h_alfa_beta.search()

        return action
        
    def mcts(self):
        state = State(self.board)
        mcts = MonteCarlo(state, self.player)
        mcts.run(1000)
        action = mcts.next_move()

        return action

    def mcts_minimax(self):
        state = State(self.board)
        mcts_minimax = MCTSMinimax(state, self.player, 2)
        mcts_minimax.run(1000)
        action = mcts_minimax.next_move()

        return action 