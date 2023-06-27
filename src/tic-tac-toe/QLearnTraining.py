import copy
import json
from Algorithms.QLearning import QLearn
from State import State


players = ['X', '0']

def play(qlearn, state):
    turn = 0
    while not state.is_terminal():
        qlearn.state = copy.deepcopy(state)
        qlearn.player = players[turn]

        move = qlearn.get_move()
        qlearn.learn(move)

        state = state.result(move, qlearn.player)
        turn = (turn + 1) % 2

def train():
    start_game = [[None, None, None], [None, None, None], [None, None, None]]
    start_state = State(start_game)

    qlearn = QLearn(learn_active=True, epsilon=0.2, gamma=1)

    N_episodes = 20000
    for episodes in range(N_episodes):
        play(qlearn, copy.deepcopy(start_state))
        
        print(f'{episodes+1}/{N_episodes}', end='\r')


    with open('qlearn.json', 'w') as file:
        json.dump(qlearn.Q, file)


train()
