from MonteCarlo import *
from State import State 


def test_next_move():
    player = '0'
    grid = [['X', 'X', None], [None, '0', None], [None, '0', 'X']]
    state = State(grid)

    print(state.actions())
    mcts = MCTS(state, player)
    state.print()

    mcts.run(1000)

    move = mcts.next_move()

    print('move', move)
    state.grid[move[0]][move[1]] = player 

    state.print()


def test_is_terminal():
    player = '0'
    grid = [['X', 'X', 'X'], [None, '0', '0'], [None, '0', 'X']]
    state = State(grid, player)

    state.print()

    print(state.is_terminal())

    print(state.actions())



test_next_move()