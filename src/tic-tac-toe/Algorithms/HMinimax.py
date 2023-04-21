import math 
import copy 

from utils import opponent

class HMinimax():
    def __init__(self, state, player, depth):
        self.state = state
        self.player = player
        self.depth = depth

    def search(self):
        move = None 

        max_value = -math.inf 
        for action in self.state.actions():
            new_state = copy.deepcopy(self.state)
            state_result = new_state.result(action, self.player)
            value = self.minimax_min(state_result, self.depth-1)

            if value > max_value:
                max_value = value 
                move = action 

        return move 
    
    def minimax_min(self, state, depth):
        if state.is_terminal():
            return state.utility(self.player)
        
        if depth == 0:
            return state.evaluation(self.player)

        min = math.inf 
        for action in state.actions():
            new_state = copy.deepcopy(state)
            state_result = new_state.result(action, opponent(self.player))
            value = self.minimax_max(state_result, depth - 1)

            if value < min:
                min = value 
                
        return min


    def minimax_max(self, state, depth):
        if state.is_terminal():
            return state.utility(self.player)
        
        if depth == 0:
            return state.evaluation(self.player)
     
        max = -math.inf
        for action in state.actions():
            new_state = copy.deepcopy(state)
            state_result = new_state.result(action, self.player)
            
            value = self.minimax_min(state_result, depth - 1)

            if value > max:
                max = value

        return max
    