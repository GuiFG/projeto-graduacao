from State import State
from Algorithms.HAlfaBeta import HAlfaBeta
from Algorithms.MonteCarlo import MonteCarlo
from Algorithms.RaveMcts import RaveMcts
from Algorithms.QLearning import QLearn
import random
import json
import os.path

RANDOM = 0
PAB_3 = 1
PAB_6 = 2
MCTS_1000 = 3
MCTS_5000 = 4
RAVE_1000 = 5
RAVE_5000 = 6
QLEARN_1 = 7
QLEARN_2 = 8

Q_TABLE_1 = {}
Q_TABLE_2 = {}

class Player():
    def __init__(self, type, player):
        self.type = type 
        self.player = player

    def get_action(self, board, prevMove):
        action = None

        state = State(board, prevMove)

        if self.type == RANDOM:
            return self.random(board, prevMove)
        elif self.type == PAB_3:
            action = self.h_alfa_beta(state, 3)
        elif self.type == PAB_6:
            action = self.h_alfa_beta(state, 6)
        elif self.type == MCTS_1000:
            action = self.mcts(state, 1000)
        elif self.type == MCTS_5000:
            action = self.mcts(state, 5000)
        elif self.type == RAVE_1000:
            action = self.rave_mcts(state, 1000)
        elif self.type == RAVE_5000:
            action = self.rave_mcts(state, 5000)
        elif self.type == QLEARN_1:
            action = self.qlearn(state, 50000)
        elif self.type == QLEARN_2:
            action = self.qlearn(state, 100000)
       
        return action

    def random(self, board, prevMove):
        nextMoves, _ = board.getValidMoves(prevMove)

        return random.choice(nextMoves)
    
    def h_alfa_beta(self, state, depth):
        h_alfa_beta = HAlfaBeta(state, self.player, depth)

        action = h_alfa_beta.search()

        return action
        
    def mcts(self, state, simulations):
        mcts = MonteCarlo(state, self.player)
        mcts.run(simulations)
        action = mcts.next_move()

        return action
    
    def rave_mcts(self, state, simulations):
        rave_mcts = RaveMcts(state, self.player)
        rave_mcts.run(simulations)
        action = rave_mcts.next_move()

        return action
    
    def qlearn(self, state, episodes):
        
        qtable = Player.get_qtable(episodes)
        qlearn = QLearn(state, self.player, qtable)

        move = qlearn.get_move()
        qlearn.learn(move)

        return move

    def get_qtable(episodes):
        qtable = {}
        
        global Q_TABLE_1, Q_TABLE_2
        if episodes == 100000:
            if len(Q_TABLE_1) == 0:
                Q_TABLE_1 = Player.get_qtable_json(episodes)
            
            qtable = Q_TABLE_1
        elif episodes == 300000:
            if len(Q_TABLE_2) == 0:
                Q_TABLE_2 = Player.get_qtable_json(episodes)
            
            qtable = Q_TABLE_2
        
        return qtable
    
    def get_qtable_json(episodes):
        filename = f'qlearn_{episodes}.json'
        if os.path.isfile(filename):
            with open(f'qlearn_{episodes}.json', 'r') as file:
                return json.load(file)