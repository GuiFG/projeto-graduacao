import math 
import copy 
import time 
import os 
import sys
import random 

class Random():
    def __init__(self, game, player) -> None:
        self.game = game 
        self.player = player 
    
    def next_move(self, state):
        actions = self.game.actions(state)
        return random.choice(actions)

class MinMax():

    def __init__(self, game, player) -> None:
        self.game = game
        self.player = player


    def search(self, state):
        value, move = self.max_value(state)

        return move 
        

    def max_value(self, state):
        terminal, _ = self.game.terminal(state)
        if terminal:
            return self.game.utility(state, self.player), None
        
        max = -math.inf
        max_move = 0

        actions = self.game.actions(state)
        for action in actions:
            new_state = copy.deepcopy(state)
            result = self.game.result(new_state, action, self.player)
            
            value, move = self.min_value(result)
            if value > max:
                max = value
                max_move = action 

        return max, max_move 
        

    def min_value(self, state):
        terminal, _ = self.game.terminal(state)
        if terminal:
            return self.game.utility(state, self.player), None 

        min = math.inf 
        min_move = 0 

        actions = self.game.actions(state)
        for action in actions:
            new_state = copy.deepcopy(state)
            result = self.game.result(new_state, action, self.player * -1)
            value, move = self.max_value(result)
            if value < min:
                min = value 
                min_move = action 

        return min, min_move 

    def print_state(self, state, player):
        print("max" if player == -1 else "min")
        for i in range(3):
            for j in range(3):
                if state[i][j][0].value == None:
                    print("-", end='')
                else:
                    print("x" if state[i][j][0].value == "x" else "o", end='')
            print()
        print()
