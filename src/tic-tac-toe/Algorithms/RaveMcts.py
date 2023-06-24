import math
import random
import copy 
from utils import opponent
from State import State

class Node:
    def __init__(self, state, player, parent=None, action=None, depth=0):
        self.state = state
        self.player = player
        self.parent = parent
        self.action = action
        self.move = State.get_action_key(action)
        self.children = []
        self.depth = depth
        
        self.visits = 0
        self.utility = 0

    def expand(self, amaf_visits, amaf_reward):
        for action in self.state.actions():
            next_state = self.state.result(action, opponent(self.player))
            child = Node(next_state, opponent(self.player), self, action, self.depth + 1)
            self.children.append(child)

            if child.depth not in amaf_visits:
                amaf_visits[child.depth] = { child.move: 0 }
                amaf_reward[child.depth] = { child.move: 0 }
            elif child.move not in amaf_visits[child.depth]:
                amaf_visits[child.depth][child.move] = 0
                amaf_reward[child.depth][child.move] = 0
                

    def rave_score(self, child_node, amaf_visits, amaf_reward, exploration_constant, equivalent_parameter):
        if child_node.visits == 0:
            return math.inf
        
        q = child_node.utility / child_node.visits
        amaf_score = self.calculate_amaf_score(amaf_visits, amaf_reward, child_node.move)
        beta_parameter = math.sqrt(equivalent_parameter/(3*self.visits + equivalent_parameter))

        exploitation = (1 - beta_parameter) * q + beta_parameter * amaf_score
        exploration = math.sqrt(math.log(self.visits) / child_node.visits)

        return exploitation + exploration_constant * exploration
    
    def calculate_amaf_score(self, amaf_visits, amaf_reward, move):
        visits = 0
        reward = 0

        for depth in amaf_visits.keys():
            if depth >= self.depth:
                if move in amaf_visits[depth]:
                    visits += amaf_visits[depth][move]
                    reward += amaf_reward[depth][move]
        
        return reward / visits


    def select_child(self, amaf_visits, amaf_reward, exploration_constant=1.4, equivalent_parameter=250):
        return max(self.children, key=lambda c: self.rave_score(c, amaf_visits, amaf_reward, exploration_constant, equivalent_parameter))

    def backpropagate(self, reward, player, amaf_visits, amaf_reward):
        self.visits += 1

        utility = reward if self.player == player else reward * -1
        self.utility += utility

        amaf_visits[self.depth][self.move] += 1
        amaf_reward[self.depth][self.move] += utility

        if self.parent:
            self.parent.backpropagate(reward, player, amaf_visits, amaf_reward)


class RaveMcts:
    def __init__(self, state, player):
        self.root = Node(state, opponent(player))
        self.amaf_visits = {}
        self.amaf_reward = {}

        self.amaf_visits[self.root.depth] = { self.root.move: 0 }
        self.amaf_reward[self.root.depth] = { self.root.move: 0 }

    def run(self, simulations):
        for i in range(simulations):
            node = self.root
            while len(node.children) > 0:
                node = node.select_child(self.amaf_visits, self.amaf_reward)

            if node.visits == 0:
                node.expand(self.amaf_visits, self.amaf_reward)

            reward, player = self.simulate(node.state, node.player)
            node.backpropagate(reward, player, self.amaf_visits, self.amaf_reward)
            print(i, end='\r')

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