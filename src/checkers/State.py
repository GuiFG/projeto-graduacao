import copy 
from utils import *

class State:
    def __init__(self, board):
        self.board = board
    
    def is_terminal(self):
        return is_terminal_node(self.board)
        
    def actions(self, player):
        return get_valid_moves(self.board, player)
    
    def result(self, action, player):
        board = copy.deepcopy(self.board)

        make_move(board, action, player)

        return State(board)
    
    def utility(self, player):
        opponent_moves = self.actions(opponent_player(player))
        moves = self.actions(player)

        if len(opponent_moves) == 0 and len(moves) == 0:
            return 0

        if len(opponent_moves) == 0:
            return 1
        
        return -1
        
        