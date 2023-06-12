import copy 
from utils import *

class State:
    def __init__(self, board):
        self.board = board
    
    def is_terminal(self):
        return is_terminal_node(self.board)
        
    def actions(self, player):
        return find_available_moves(self.board, player)
    
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
    
    def evaluation(self, player):
        player_score = self.evaluation_by_player(player)
        op_score = self.evaluation_by_player(opponent_player(player))

        return player_score - op_score


    def evaluation_by_player(self, player):
        type_score = get_type_score(self.board, player)
        localization_score = get_localization_score(self.board, player)
        layout_score, jump_score = get_layout_jump_score(self.board, player)

        return type_score + localization_score + layout_score + jump_score 
