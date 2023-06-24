import copy 
from utils import *

class State:
    def __init__(self, board, positions=[]):
        self.board = board
        self.positions = positions
    
    def is_terminal(self):
        return is_terminal_node(self.board)
        
    def actions(self, player):
        return find_available_moves(self.board, player)
    
    def result(self, action, player):
        board = copy.deepcopy(self.board)

        make_move(board, action, player)

        update_positions(self.board, self.positions)

        return State(board, self.positions)
    
    def utility(self, player):
        black_pieces, white_pieces = count_pieces(self.board)
        winner = check_winner(self.board, black_pieces, white_pieces)
        
        if winner is None:
            return 0
        
        if winner.lower() == player.lower():
            return 1
        
        return -1 * count_pieces_by_player(self.board, opponent_player(player))
    
    def evaluation(self, player):
        player_score = self.evaluation_by_player(player)
        op_score = self.evaluation_by_player(opponent_player(player))

        return player_score - op_score
    
    def evaluation_by_player(self, player):
        type_score = get_type_score(self.board, player)
        localization_score = get_localization_score(self.board, player)
        layout_score, jump_score = get_layout_jump_score(self.board, player)

        return type_score + localization_score + layout_score + jump_score 
