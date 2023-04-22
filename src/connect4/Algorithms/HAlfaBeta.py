import math 
import copy 

from utils import opponent_player

class HAlfaBeta():
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
            value = self.alfa_beta_min(state_result, max_value, math.inf, self.depth-1)

            if value > max_value:
                max_value = value 
                move = action 

        return move 
    
    def alfa_beta_min(self, state, alfa, beta, depth):
        if state.is_terminal() or depth == 0:
            return state.evaluation(self.player)

        min_value = math.inf 
        for action in state.actions():
            new_state = copy.deepcopy(state)
            state_result = new_state.result(action, opponent_player(self.player))
            value = self.alfa_beta_max(state_result, alfa, beta, depth - 1)

            if value < min_value:
                min_value = value 

            if min_value <= alfa:
                return min_value 
            
            if min_value < beta: 
                beta = min_value 
            
                
        return min_value


    def alfa_beta_max(self, state, alfa, beta, depth):
        if state.is_terminal() or depth == 0:
            return state.evaluation(self.player)
     
        max_value = -math.inf
        for action in state.actions():
            new_state = copy.deepcopy(state)
            state_result = new_state.result(action, self.player)
            
            value = self.alfa_beta_min(state_result, alfa, beta, depth - 1)

            if value > max_value:
                max_value = value

            if max_value >= beta: 
                return max_value 

            if max_value > alfa:
                alfa = max_value 

        return max_value