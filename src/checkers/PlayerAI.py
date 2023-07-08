from State import State
from Algorithms.Random import Random
from Algorithms.HAlfaBeta import HAlfaBeta
from Algorithms.MonteCarlo import MCTS 
from Algorithms.RaveMcts import RaveMcts
from Algorithms.QLearning import QLearn
import json
import os.path

RANDOM = 0
PAB_3 = 1
PAB_6 = 2
MCTS_1000 = 3
MCTS_10000 = 4
RAVE_1000 = 5
RAVE_10000 = 6
QLEARN_1 = 7
QLEARN_2 = 8

Q_TABLE_1 = {}
Q_TABLE_2 = {}

class Player():
    def __init__(self, board, player, type):
        self.board = board 
        self.player = player
        self.type = type

    def get_action(self):
        action = None

        if self.type == 0:
            action = self.random()
        elif self.type == PAB_3:
            action = self.h_alfa_beta(3)
        elif self.type == PAB_6:
            action = self.h_alfa_beta(6)
        elif self.type == MCTS_1000:
            action = self.mcts(1000)
        elif self.type == MCTS_10000:
            action = self.mcts(10000)
        elif self.type == RAVE_1000:
            action = self.rave_mcts(1000)
        elif self.type == RAVE_10000:
            action = self.rave_mcts(10000)
        elif self.type == QLEARN_1:
            action = self.qlearn(100000)
        elif self.type == QLEARN_2:
            action = self.qlearn(300000)
        
        return action
    
    def random(self):
        move = Random.get_move(self.board, self.player)

        return move

    def h_alfa_beta(self, depth):
        state = State(self.board)

        h_alfa_beta = HAlfaBeta(state, self.player, depth)

        action = h_alfa_beta.search()

        return action

    def mcts(self, simulations):
        state = State(self.board)
        mcts = MCTS(state, self.player)
        mcts.run(simulations)
        mcts_move = mcts.next_move()

        return mcts_move
    
    def rave_mcts(self, simulations):
        state = State(self.board)
        rave_mcts = RaveMcts(state, self.player)
        rave_mcts.run(simulations)
        move = rave_mcts.next_move()

        return move

    def qlearn(self, episodes):
        state = State(self.board)
        
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
