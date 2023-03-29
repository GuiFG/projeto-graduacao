import math 
import copy 

from utils import wins, opponent

class HMinimax():
    def __init__(self, state, depth) -> None:
        self.state = state
        self.player = state.player
        self.depth = depth 

    def search(self):
        value, move = self.max_value(self.state, 0)

        if value == None:
            return None 

        return move 
        
    def max_value(self, state, depth):
        if state.is_terminal():
            return state.utility(self.player), None
        
        if depth == self.depth:
            return None, None 
        
        max = -math.inf
        max_move = 0

        actions = state.actions()
        for action in actions:
            new_state = copy.deepcopy(state)
            state_result = new_state.result(action)
            
            value, move = self.min_value(state_result, depth)

            if value == None:
                return None, None 

            if value > max:
                max = value
                max_move = action 


        return max, max_move 
        
    def min_value(self, state, depth):
        if state.is_terminal():
            return state.utility(self.player), None  

        min = math.inf 
        min_move = 0 

        actions = state.actions()
        for action in actions:
            new_state = copy.deepcopy(state)
            state_result = new_state.result(action)
            value, move = self.max_value(state_result, depth + 1)

            if value == None:
                return None, None 

            if value < min:
                min = value 
                min_move = action 

        return min, min_move 

    def evaluation_state(self, state):
        if wins(state.grid, self.player):
            return 1 
        
        if wins(state.grid, opponent(self.player)):
            return -1 
        
        return 1
    