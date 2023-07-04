import copy
from utils import *
import hashlib

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
        
        return 0.5
    
    def evaluation(self, player):
        score = 0 
        for row in self.board.board:
            for small_board in row: 
                score += evaluation_small_board(small_board.board, player)
        return score

    def get_state_key(self, player):
        board = ''
        for row in self.board.board:
            for small_board in row: 
                board += flatten_board(small_board.board)
        board += (self.get_action_key(self.prevMove) + str(player))

        return hashlib.sha256(board.encode()).hexdigest()
        
    def get_action_key(self, action):
        if action is None: 
            return '99'
        
        return ''.join([str(a) for a in action])

    @staticmethod
    def get_action_from_key(key):
        return [int(k) for k in key]