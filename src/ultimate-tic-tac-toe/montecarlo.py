import math
import random
import copy 

from utils import *

class State:
    def __init__(self, board, player, prevMove):
        self.board = board
        self.player = player
        self.prevMove = prevMove
    
    def is_terminal(self):
        return is_terminal_node(self.board)
        
    def actions(self):
        return get_valid_moves(self.board, self.prevMove)
    
    def result(self, action):
        board = copy.deepcopy(self.board)

        board.playMove(action, opponent_player(self.player))

        return State(board, opponent_player(self.player), action)
    
    def utility(self):
        curState = self.board.getState()
        if curState[0] == 'W':
            return 1 if curState[1] == self.player else -1
        
        return 0



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


class MonteCarloTreeSearch:
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
            print(i, end='\r')

    def simulate(self, state):
        copy_state = copy.deepcopy(state)

        while not copy_state.is_terminal():
            action = random.choice(copy_state.actions())
            copy_state = copy_state.result(action)
            
        return copy_state.utility(), copy_state.player

    def next_move(self):
        return max(self.root.children, key=lambda c: c.visits).action
    