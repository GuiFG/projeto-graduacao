import copy 
from utils import *

class State:
    def __init__(self, board):
        self.board = board
    
    def is_terminal(self):
        return is_terminal_node(self.board)
        
    def actions(self):
        return get_valid_locations(self.board)
    
    def result(self, action, player):
        board = copy.deepcopy(self.board)

        row = get_next_open_row(board, action)
        drop_piece(board, row, action, player)

        return State(board)
    
    def utility(self, player):
        if winning_move(self.board, player):
            return 1
        
        return -1 if winning_move(self.board, opponent_player(player)) else 0