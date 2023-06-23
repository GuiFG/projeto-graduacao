import math
import random
import copy 
from utils import opponent
from State import State

class Node:
    def __init__(self, state, player, parent=None, action=None):
        self.state = state
        self.player = player
        self.parent = parent
        self.action = action
        self.move = State.get_action_key(action)
        self.children = []
        
        self.visits = 0
        self.utility = 0

    def expand(self, amaf_visits, amaf_reward):
        for action in self.state.actions():
            next_state = self.state.result(action, opponent(self.player))
            child = Node(next_state, opponent(self.player), self, action)
            self.children.append(child)

            if child.move not in amaf_visits:
                amaf_visits[child.move] = 0
                amaf_reward[child.move] = 0

    def rave_score(self, child_node, amaf_visits, amaf_reward, equivalent_parameter):
        if child_node.visits == 0:
            return math.inf

        exploitation = child_node.utility / child_node.visits
        amaf_score = amaf_reward[child_node.move] / amaf_visits[child_node.move]

        beta_parameter = math.sqrt(equivalent_parameter/(3*self.visits + equivalent_parameter))

        return (1 - beta_parameter) * exploitation + beta_parameter * amaf_score

    def select_child(self, amaf_visits, amaf_reward, equivalent_parameter=500):
        return max(self.children, key=lambda c: self.rave_score(c, amaf_visits, amaf_reward, equivalent_parameter))

    def backpropagate(self, reward, player, amaf_visits, amaf_reward):
        self.visits += 1

        utility = reward if self.player == player else reward * -1
        self.utility += utility

        amaf_visits[self.move] += 1
        amaf_reward[self.move] += utility

        if self.parent:
            self.parent.backpropagate(reward, player, amaf_visits, amaf_reward)


class RaveMcts:
    def __init__(self, state, player):
        self.root = Node(state, opponent(player))
        self.amaf_visits = {}
        self.amaf_reward = {}

        self.amaf_visits[self.root.move] = 0
        self.amaf_reward[self.root.move] = 0

    def run(self, simulations):
        for i in range(simulations):
            node = self.root
            while len(node.children) > 0:
                node = node.select_child(self.amaf_visits, self.amaf_reward)

            if node.visits == 0:
                node.expand(self.amaf_visits, self.amaf_reward)

            reward, player = self.simulate(node.state, node.player)
            node.backpropagate(reward, player, self.amaf_visits, self.amaf_reward)

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
