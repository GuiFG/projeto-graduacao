import math
import random
import copy 
from utils import wins, opponent, empty_cells
import time 
import State 

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


class MCTS:
    def __init__(self, state, player):
        self.root = Node(state, opponent(player))

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
            action = random.choice(copy_state.actions())
            copy_player = opponent(copy_player)
            copy_state = copy_state.result(action, copy_player)

        return copy_state.utility(copy_player), copy_player

    def next_move(self):
        return max(self.root.children, key=lambda c: c.visits).action

    def result(self):
        for child in self.root.children:
            print(child.utility, child.visits, child.player, self.root.visits, self.root.ucb_score(child.utility, child.visits, 1.4))
            child.state.print()
            print()
