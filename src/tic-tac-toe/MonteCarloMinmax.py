import math
import random
import copy 
from utils import wins, opponent, empty_cells
import time 

from HMinimax import HMinimax
from Minimax import Minimax

class Node:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action 
        self.children = []
        self.visits = 0
        self.utility = 0
        self.player = state.player

    def expand(self):
        for action in self.state.actions():
            next_state = self.state.result(action)
            child = Node(next_state, self, action)
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
    def __init__(self, state):
        self.root = Node(state)
        self.player = state.player
        self.root.expand()

    def run(self, simulations):
        for i in range(simulations):
            node = self.root
            while len(node.children) > 0:
                node = node.select_child()

            if node.visits == 0:
                node.expand()

            reward, player = self.simulate(node.state)
            node.backpropagate(reward, player)

    def simulate(self, state):
        copy_state = copy.deepcopy(state)

        while not copy_state.is_terminal():
            action = self.move_hminimax(copy_state)
            if action == None: 
                action = random.choice(copy_state.actions())
            else:
                print('action diferente de None')
            #print(action)
            #copy_state.print()
            #time.sleep(5)
            copy_state = copy_state.result(action)
        
        #print(action)
        #copy_state.print()
        #print('fim simulacao')
        #print(copy_state.utility(), copy_state.player)
        #time.sleep(5)

        return copy_state.utility(), copy_state.player

    def move_hminimax(self, state):
        copy_state = copy.deepcopy(state)
        copy_state.opponent_action = False 
        
        hminimax = Minimax(copy_state)     
        move = hminimax.search()
        
        return move 

    def next_move(self):
        return max(self.root.children, key=lambda c: c.visits).action

