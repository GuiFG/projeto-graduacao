from State import State
from Algorithms.MonteCarlo import MCTS 
from Algorithms.Random import Random

RANDOM = 0
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
        elif self.type == MCTS_500:
            action = self.mcts(500)
        
        return action
    
    def random(self):
        move = Random.get_move(self.board, self.player)

        return move

    def mcts(self, simulations):
        state = State(self.board)
        mcts = MCTS(state, self.player)
        mcts.run(simulations)
        mcts_move = mcts.next_move()

        return mcts_move 
