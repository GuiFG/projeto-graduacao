import numpy as np
import random
from State import State
from utils import opponent_player

class QLearn:
    def __init__(self, state=None, player=1, Q={}, epsilon=0.2, alpha=0.1, gamma=1, default_Qvalue=1, learn_active=False):
        self.state = state
        self.player = player
        self.Q = Q
        self.epsilon = epsilon
        self.default_Qvalue = default_Qvalue
        self.alpha = alpha
        self.gamma = gamma
        self.learn_active = learn_active
        self.ref_player = 1
    
    def get_move(self):
        if self.learn_active:
            if np.random.uniform() < self.epsilon:
                actions = self.state.actions()
                return random.choice(actions)
        
        state_key = self.state.get_state_key(self.player)
        self.initialize_qvalue(self.state, state_key)
        
        action_key = self.stochastic_argmax(self.Q[state_key])

        return State.get_action_from_key(action_key)
    
    def learn(self, action):
        action_key = self.state.get_action_key(action)

        state_key = self.state.get_state_key(self.player)
        self.initialize_qvalue(self.state, state_key)

        next_state = self.state.result(action, self.player)

        reward = next_state.utility(self.ref_player)
        if not next_state.is_terminal():
            next_state_key = next_state.get_state_key(opponent_player(self.player))
            self.initialize_qvalue(next_state, next_state_key)
            
            next_Q = self.Q[next_state_key]
            values = min(next_Q.values()) if self.player == self.ref_player else max(next_Q.values())

            expected = reward + (self.gamma * values)
        else:
            expected = reward

        change = self.alpha * (expected - self.Q[state_key][action_key])
        self.Q[state_key][action_key] += change

    def initialize_qvalue(self, state, state_key):
        if self.Q.get(state_key) is None:
            actions = state.actions()
            actions = [state.get_action_key(action) for action in actions]
            
            self.Q[state_key] = { action: self.default_Qvalue for action in actions }

    def stochastic_argmax(self, Qs):
        values = list(Qs.values())
        max_value = max(values) if self.player == self.ref_player else min(values)
        if values.count(max_value) > 1:
            best_options = [action for action in list(Qs.keys()) if Qs[action] == max_value]
            action = random.choice(best_options)
        else:
            action = max(Qs, key=Qs.get) if self.player == self.ref_player else min(Qs, key=Qs.get)
        
        return action

