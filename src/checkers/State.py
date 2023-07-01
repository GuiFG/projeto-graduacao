import copy 
from utils import *
import hashlib

class State:
    def __init__(self, board, positions=[]):
        self.board = board
        self.positions = positions
    
    def is_terminal(self):
        return is_terminal_node(self.board, self.positions)
        
    def actions(self, player):
        return find_available_moves(self.board, player)
    
    def result(self, action, player):
        board = copy.deepcopy(self.board)

        make_move(board, action, player)

        update_positions(self.board, self.positions)

        return State(board, copy.deepcopy(self.positions))
    
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


    def get_state_key(self, player):
        board = flatten_board(self.board) + player

        return hashlib.sha256(board.encode()).hexdigest()

    def get_action_key(self, action):
        if action is None: 
            return '9999'
        
        return ''.join([str(a) for a in action])

    @staticmethod
    def get_action_from_key(key):
        return [int(k) for k in key]
