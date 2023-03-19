import math 
import copy 


class Minimax():
    def __init__(self, state) -> None:
        self.state = state
        self.player = state.player

    def search(self):
        value, move = self.max_value(self.state)

        return move 
        
    def max_value(self, state):
        if state.is_terminal():
            return state.utility(self.player), None
        
        max = -math.inf
        max_move = 0

        actions = state.actions()
        for action in actions:
            new_state = copy.deepcopy(state)
            state_result = new_state.result(action)
            
            value, move = self.min_value(state_result)
            if value > max:
                max = value
                max_move = action 

        return max, max_move 
        
    def min_value(self, state):
        if state.is_terminal():
            return state.utility(self.player), None  

        min = math.inf 
        min_move = 0 

        actions = state.actions()
        for action in actions:
            new_state = copy.deepcopy(state)
            state_result = new_state.result(action)
            value, move = self.max_value(state_result)
            if value < min:
                min = value 
                min_move = action 

        return min, min_move 

    