from State import State
from Algorithms.HAlfaBeta import HAlfaBeta
from Algorithms.MonteCarlo import MonteCarlo
from Algorithms.RaveMcts import RaveMcts
import random

RANDOM = 0
PAB_3 = 1
PAB_4 = 2
PAB_5 = 3
PAB_6 = 4
MCTS_500 = 5
MCTS_1000 = 6
MCTS_5000 = 7
MCTS_10000 = 8 
RAVE = 9

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
        elif self.type == PAB_4:
            action = self.h_alfa_beta(state, 4)
        elif self.type == PAB_5:
            action = self.h_alfa_beta(state, 5)
        elif self.type == PAB_6:
            action = self.h_alfa_beta(state, 6)
        elif self.type == MCTS_500:
            action = self.mcts(state, 500)
        elif self.type == MCTS_1000:
            action = self.mcts(state, 1000)
        elif self.type == MCTS_5000:
            action = self.mcts(state, 5000)
        elif self.type == MCTS_10000:
            action = self.mcts(state, 10000)
        elif self.type == RAVE:
            action = self.rave_mcts(state, 100)
       
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