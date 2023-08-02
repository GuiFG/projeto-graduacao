import copy
import json
from Algorithms.QLearning import QLearn
from State import State
from datetime import datetime
import Metrics
from bigBoard import BigBoard

players = ['X', 'O']

def play(qlearn, state):
    turn = 0
    while not state.is_terminal():
        qlearn.state = copy.deepcopy(state)
        qlearn.player = players[turn]

        move = qlearn.get_move()
        qlearn.learn(move)

        state = state.result(move, qlearn.player)
        turn = (turn + 1) % 2

def train(episodes):
    start_game = BigBoard()
    start_state = State(start_game, None)

    qlearn = QLearn(learn_active=True)

    start_train = datetime.now()
    for episode in range(episodes):
        play(qlearn, copy.deepcopy(start_state))
        
        print(f'{episode+1}/{episodes}', end='\r')

    end_train = datetime.now() - start_train
    Metrics.save_train_time(end_train, episodes)

    with open(f'qlearn_{episodes}.json', 'w') as file:
        json.dump(qlearn.Q, file)


train(50000)
