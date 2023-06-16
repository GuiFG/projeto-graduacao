from State import State
from Algorithms.HAlfaBeta import HAlfaBeta
from Algorithms.MonteCarlo import MCTS 
from Algorithms.Random import Random

RANDOM = 0
PAB_3 = 1
PAB_4 = 2
MCTS_500 = 5

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
        elif self.type == MCTS_500:
            action = self.mcts(500)
        
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
