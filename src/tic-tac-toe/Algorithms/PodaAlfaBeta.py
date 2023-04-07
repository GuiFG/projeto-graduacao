import math 
import copy 

from utils import wins, opponent

class PodaAlfaBeta():
    def __init__(self, state, player) -> None:
        self.state = state
        self.player = player

    def search(self):
        move = None 

        max_value = -math.inf 
        for action in self.state.actions():
            new_state = copy.deepcopy(self.state)
            state_result = new_state.result(action, self.player)
            value = self.min_value(state_result)

            if value > max_value:
                max_value = value 
                move = action 

        return move 
    
    def minimax_min(self, state):
        if state.is_terminal():
            return state.utility(self.player)

        min = math.inf 
        for action in state.actions():
            new_state = copy.deepcopy(state)
            state_result = new_state.result(action, opponent(self.player))
            value = self.minimax_max(state_result)

            if value < min:
                min = value 
                
        return min


    def minimax_max(self, state):
        if state.is_terminal():
            return state.utility(self.player)
     
        max = -math.inf
        for action in state.actions():
            new_state = copy.deepcopy(state)
            state_result = new_state.result(action, self.player)
            
            value = self.min_value(state_result)

            if value > max:
                max = value

        return max