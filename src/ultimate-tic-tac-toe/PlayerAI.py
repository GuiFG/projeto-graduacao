from State import State
from Algorithms.HAlfaBeta import HAlfaBeta
from Algorithms.MonteCarlo import MCTS


class Player():
    def h_alfa_beta(self, depth):
        state = State(self.board)
        h_alfa_beta = HAlfaBeta(state, self.player, depth)

        action = h_alfa_beta.search()

        return action

    def mcts(board, player):
        state = State(board)
        mcts = MCTS(state, player)
        mcts.run(1000)
        action = mcts.next_move()

        return action
