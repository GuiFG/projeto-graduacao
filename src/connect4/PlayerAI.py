from State import State
from Algorithms.Random import Random
from Algorithms.Minimax import Minimax
from Algorithms.PodaAlfaBeta import PodaAlfaBeta
from Algorithms.MonteCarlo import MonteCarlo
from Algorithms.HMinimax import HMinimax
from Algorithms.HAlfaBeta import HAlfaBeta
from Algorithms.RaveMcts import RaveMcts
from Algorithms.QLearning import QLearn
import json
import os.path

filename = 'qlearn.json'

if os.path.isfile(filename):
    with open('qlearn.json', 'r') as file:
        Q = json.load(file)

RANDOM = 0
PAB_3 = 1
PAB_4 = 2
PAB_5 = 3
PAB_6 = 4
MCTS_500 = 5
MCTS_1000 = 6
MCTS_5000 = 7
MCTS_10000 = 8
RAVE = 9
QLEARN = 10


class Player():
    def __init__(self, board, player, type):
        self.board = board
        self.player = player
        self.type = type

    def get_action(self):
        action = None 

        if self.type == RANDOM:
            action = self.random()
        elif self.type == PAB_3:
            action = self.h_alfa_beta(3)
        elif self.type == PAB_4:
            action = self.h_alfa_beta(4)
        elif self.type == PAB_5:
            action = self.h_alfa_beta(5)
        elif self.type == PAB_6:
            action = self.h_alfa_beta(6)
        elif self.type == MCTS_500:
            action = self.mcts(500)
        elif self.type == MCTS_1000:
            action = self.mcts(1000)
        elif self.type == MCTS_5000:
            action = self.mcts(5000)
        elif self.type == MCTS_10000:
            action = self.mcts(10000)
        elif self.type == RAVE:
            action = self.rave_mcts(1000)
        elif self.type == QLEARN:
            action = self.qlearn()
       
        return action
    
    def random(self):
        return Random.get_move()

    def minimax(self):
        state = State(self.board)
        minimax = Minimax(state, self.player)
        action = minimax.search()
        
        return action 
    
    def alfa_beta(self):
        state = State(self.board)
        alfa_beta = PodaAlfaBeta(state, self.player)
        action = alfa_beta.search()

        return action
    
    def hminimax(self, depth):
        state = State(self.board)
        hminimax = HMinimax(state, self.player, depth)
        
        action = hminimax.search()

        return action 
    
    def h_alfa_beta(self, depth):
        state = State(self.board)
        h_alfa_beta = HAlfaBeta(state, self.player, depth)

        action = h_alfa_beta.search()

        return action
        
    def mcts(self, simulations):
        state = State(self.board)
        mcts = MonteCarlo(state, self.player)
        mcts.run(simulations)
        action = mcts.next_move()

        return action

    def rave_mcts(self, simulations):
        state = State(self.board)
        rave_mcts = RaveMcts(state, self.player)
        rave_mcts.run(simulations)
        action = rave_mcts.next_move()

        return action
    
    def qlearn(self):
        state = State(self.board)

        qlearn = QLearn(state, self.player, Q)
        move = qlearn.get_move()
        qlearn.learn(move)

        return move