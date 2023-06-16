import math
import random
import copy 
import time 

from datetime import datetime 

from utils import opponent_player
    
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
        op_player = opponent_player(self.player)
        for action in self.state.actions(op_player):
            next_state = self.state.result(action, op_player)
            child = Node(next_state, op_player, self, action)
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
        self.root = Node(state, opponent_player(player))

    def run(self, simulations):
        now = datetime.now()
        for i in range(simulations):
            node = self.root
            while len(node.children) > 0:
                node = node.select_child()

            if node.visits == 0:
                node.expand()

            reward, player = self.simulate(node.state, node.player)
            node.backpropagate(reward, player)

        delta = datetime.now() - now 
        print(f'levou: {delta.total_seconds()}s')

    def simulate(self, state, player):
        copy_state = copy.deepcopy(state)
        copy_player = copy.deepcopy(player)

        while not copy_state.is_terminal():
            copy_player = opponent_player(copy_player)
            action = random.choice(copy_state.actions(copy_player))
            copy_state = copy_state.result(action, copy_player)
        
        return copy_state.utility(copy_player), copy_player

    def next_move(self):
        return max(self.root.children, key=lambda c: c.visits).action
    