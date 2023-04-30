import copy
from utils import *

class State:
    def __init__(self, board, prevMove):
        self.board = board
        self.prevMove = prevMove
    
    def is_terminal(self):
        return is_terminal_node(self.board)
        
    def actions(self):
        return get_valid_moves(self.board, self.prevMove)
    
    def result(self, action, player):
        board = copy.deepcopy(self.board)

        board.playMove(action, player)

        return State(board, action)
    
    def utility(self, player):
        curState = self.board.getState()
        if curState[0] == 'W':
            return 1 if curState[1] == player else -1
        
        return 0
    
    def evaluation(self, player):
        weight = 0.6

        small_board = get_current_small_board(self.board, self.prevMove)
        score_small_board = evaluation_small_board(small_board.board, player)

        score_big_board = get_score_big_board(self.board, player)

        return score_big_board * weight + score_small_board * (1 - weight)

    
