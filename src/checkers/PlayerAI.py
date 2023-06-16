from State import State
from Algorithms.Random import Random
from Algorithms.HAlfaBeta import HAlfaBeta
from Algorithms.MonteCarlo import MCTS 
from Algorithms.RaveMcts import RaveMcts

RANDOM = 0
PAB_3 = 1
PAB_4 = 2 
PAB_5 = 3
PAB_6 = 4
MCTS_500 = 5
RAVE = 6

class Player():
    def __init__(self, board, player, type):
        self.board = board 
        self.player = player
        self.type = type

    def get_action(self):
        action = None

        if self.type == 0:
            action = self.random()
        elif self.type == PAB_3:
            action = self.h_alfa_beta(3)
        elif self.type == PAB_4:
            action = self.h_alfa_beta(4)
        elif self.type == PAB_5:
            action = self.h_alfa_beta(5)
        elif self.type == PAB_6:
            action = self.h_alfa_beta(6)
        elif self.type == MCTS_500:
            action = self.mcts(500)
        elif self.type == RAVE:
            action = self.rave_mcts(500)
        
        return action
    
    def random(self):
        move = Random.get_move(self.board, self.player)

        return move

    def h_alfa_beta(self, depth):
        state = State(self.board)

        h_alfa_beta = HAlfaBeta(state, self.player, depth)

        action = h_alfa_beta.search()

        return action

    def mcts(self, simulations):
        state = State(self.board)
        mcts = MCTS(state, self.player)
        mcts.run(simulations)
        mcts_move = mcts.next_move()

        return mcts_move
    
    def rave_mcts(self, simulations):
        state = State(self.board)
        rave_mcts = RaveMcts(state, self.player)
        rave_mcts.run(simulations)
        move = rave_mcts.next_move()

        return move 
