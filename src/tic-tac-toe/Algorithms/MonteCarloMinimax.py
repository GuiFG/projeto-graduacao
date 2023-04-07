import math
import random
import copy 
from utils import opponent
import time 

class Node:
    def __init__(self, state, player, parent=None, action=None):
        self.state = state
        self.player = player
        self.parent = parent
        self.action = action 
        self.children = []
        self.visits = 0
        self.utility = 0

    def expand(self):
        for action in self.state.actions():
            next_state = self.state.result(action, opponent(self.player))
            child = Node(next_state, opponent(self.player), self, action)
            self.children.append(child)

    def ucb_score(self, utility, visits, exploration_constant):
        if visits == 0:
            return math.inf
        
        exploitation = utility / visits
        exploration = math.sqrt(math.log(self.visits) / visits)
        
        return exploitation + exploration_constant * exploration 
        
    def select_child(self, exploration_constant=1.4):
        return max(self.children, key=lambda c: self.ucb_score(c.utility, c.visits, exploration_constant))
    
    def update_utility(self, reward, player):
        if self.player == player:
            self.utility += reward
        else:
            self.utility += (reward * -1)

    def backpropagate(self, reward, player):
        self.visits += 1
        self.update_utility(reward, player)

        if self.parent:
            self.parent.backpropagate(reward, player)


class MCTSMinimax:
    def __init__(self, state, player, depth):
        self.root = Node(state, opponent(player))
        self.depth = depth 

    def run(self, simulations):
        for i in range(simulations):
            node = self.root
            while len(node.children) > 0:
                node = node.select_child()

            if node.visits == 0:
                node.expand()

            reward, player = self.simulate(node.state, node.player)
            node.backpropagate(reward, player)

    def simulate(self, state, player):
        copy_state = copy.deepcopy(state)
        copy_player = copy.deepcopy(player)

        while not copy_state.is_terminal():
            action = self.move_minimax(copy_state, copy_player)
            if action == None: 
                action = random.choice(copy_state.actions())
            
            copy_player = opponent(copy_player)
            copy_state = copy_state.result(action, copy_player)

        return copy_state.utility(copy_player), copy_player

    def move_minimax(self, state, player):
        copy_state = copy.deepcopy(state)
        
        minimax = MinimaxFixed(copy_state, player, self.depth)     
        move = minimax.search()
        
        return move

    def next_move(self):
        return max(self.root.children, key=lambda c: c.visits).action


class MinimaxFixed():
    def __init__(self, state, player, depth) -> None:
        self.state = state
        self.player = player
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

        for action in state.actions():
            new_state = copy.deepcopy(state)
            state_result = new_state.result(action, self.player)
            
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

        for action in state.actions():
            new_state = copy.deepcopy(state)
            state_result = new_state.result(action, opponent(self.player))
            value, move = self.max_value(state_result, depth + 1)

            if value == None:
                return None, None 

            if value < min:
                min = value 
                min_move = action 

        return min, min_move 

