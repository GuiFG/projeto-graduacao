import math 
import copy 

from utils import opponent

class PodaAlfaBeta():
    def __init__(self, state, player):
        self.state = state
        self.player = player

    def search(self):
        move = None 

        max_value = -math.inf 
        for action in self.state.actions():
            new_state = copy.deepcopy(self.state)
            state_result = new_state.result(action, self.player)
            value = self.alfa_beta_min(state_result, max_value, math.inf)

            if value > max_value:
                max_value = value 
                move = action 

        return move 
    
    def alfa_beta_min(self, state, alfa, beta):
        if state.is_terminal():
            return state.utility(self.player)

        min_value = math.inf 
        for action in state.actions():
            new_state = copy.deepcopy(state)
            state_result = new_state.result(action, opponent(self.player))
            value = self.alfa_beta_max(state_result, alfa, beta)

            if value < min_value:
                min_value = value 

            if min_value <= alfa:
                return min_value 
            
            if min_value < beta: 
                beta = min_value 
            
                
        return min_value


    def alfa_beta_max(self, state, alfa, beta):
        if state.is_terminal():
            return state.utility(self.player)
     
        max_value = -math.inf
        for action in state.actions():
            new_state = copy.deepcopy(state)
            state_result = new_state.result(action, self.player)
            
            value = self.alfa_beta_min(state_result, alfa, beta)

            if value > max_value:
                max_value = value

            if max_value >= beta: 
                return max_value 

            if max_value > alfa:
                alfa = max_value 

        return max_value