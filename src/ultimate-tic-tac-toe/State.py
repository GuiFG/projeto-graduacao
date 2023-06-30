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
        score = 0 
        for line in self.board.board:
            for small_board in line: 
                score += evaluation_small_board(small_board.board, player)
        
        return score
