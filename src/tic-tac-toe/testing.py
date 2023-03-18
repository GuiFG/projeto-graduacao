from MonteCarlo import *

player = '0'
grid = [['X', None, None], [None, None, None], [None, None, None]]
state = State(grid, opponent(player))

print(state.actions())
mcts = MCTS(state)
mcts.print_state(state)

mcts.run(1000)

move = mcts.next_move()
print('move', move)
state.grid[move[0]][move[1]] = player 

mcts.print_state(state)


