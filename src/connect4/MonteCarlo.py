import math
import random
import copy 
import time 

from utils import *

class State:
    def __init__(self, board, player):
        self.board = board
        self.player = player
    
    def is_terminal(self):
        return is_terminal_node(self.board)
        
    def actions(self):
        return get_valid_locations(self.board)
    
    def result(self, action):
        board = copy.deepcopy(self.board)

        row = get_next_open_row(board, action)
        drop_piece(board, row, action, opponent_player(self.player))

        return State(board, opponent_player(self.player))
    
    def utility(self):
        if winning_move(self.board, self.player):
            return 1
        
        return -1 if winning_move(self.board, opponent_player(self.player)) else 0

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


class MCTS:
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
            action = random.choice(copy_state.actions())
            copy_state = copy_state.result(action)
            
        return copy_state.utility(), copy_state.player

    def next_move(self):
        return max(self.root.children, key=lambda c: c.visits).action
    
    def print_state(self, state):
        board = state.board 
        for line in board:
            for value in line:
                if value is not None:
                    print(int(value), end=' ')
                else:
                    print('-', end=' ')
            print()
        print()

