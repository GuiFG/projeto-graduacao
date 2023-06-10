from State import State
from MonteCarlo import MCTS 

MCTS_500 = 5


class Player():
    def __init__(self, board, player, type):
        self.board = board 
        self.player = player
        self.type = type

    def get_action(self):
        action = None 

        if self.type == MCTS_500:
            action = self.mcts(500)
        
        return action
    

    def mcts(self, simulations):
        state = State(self.board)
        mcts = MCTS(state, self.player)
        mcts.run(simulations)
        mcts_move = mcts.next_move()

        return mcts_move 
