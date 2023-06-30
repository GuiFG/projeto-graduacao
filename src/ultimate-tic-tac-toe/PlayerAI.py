from State import State
from Algorithms.HAlfaBeta import HAlfaBeta
from Algorithms.MonteCarlo import MonteCarlo
from Algorithms.RaveMcts import RaveMcts
import random

RANDOM = 0
PAB_3 = 1
PAB_6 = 2
MCTS_1000 = 3
MCTS_10000 = 4
RAVE_1000 = 5
RAVE_10000 = 6
QLEARN_1 = 7
QLEARN_2 = 8

class Player():
    def __init__(self, type, player):
        self.type = type 
        self.player = player

    def get_action(self, board, prevMove):
        action = None 

        state = State(board, prevMove)

        if self.type == RANDOM:
            return self.random(board, prevMove)
        elif self.type == PAB_3:
            action = self.h_alfa_beta(state, 3)
        elif self.type == PAB_6:
            action = self.h_alfa_beta(state, 6)
        elif self.type == MCTS_1000:
            action = self.mcts(state, 1000)
        elif self.type == MCTS_10000:
            action = self.mcts(state, 10000)
        elif self.type == RAVE_1000:
            action = self.rave_mcts(state, 1000)
        elif self.type == RAVE_10000:
            action = self.rave_mcts(state, 10000)
       
        return action

    def random(self, board, prevMove):
        nextMoves, _ = board.getValidMoves(prevMove)

        return random.choice(nextMoves)
    
    def h_alfa_beta(self, state, depth):
        h_alfa_beta = HAlfaBeta(state, self.player, depth)

        action = h_alfa_beta.search()

        return action
        
    def mcts(self, state, simulations):
        mcts = MonteCarlo(state, self.player)
        mcts.run(simulations)
        action = mcts.next_move()

        return action
    
    def rave_mcts(self, state, simulations):
        rave_mcts = RaveMcts(state, self.player)
        rave_mcts.run(simulations)
        action = rave_mcts.next_move()

        return action