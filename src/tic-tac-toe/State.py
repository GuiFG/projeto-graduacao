import copy 
from utils import wins, opponent, empty_cells

class State:
    def __init__(self, grid, player, opponnent_action = False):
        self.grid = grid
        self.player = player
        self.opponent_action = opponnent_action
    
    def is_terminal(self):
        return wins(self.grid, self.player) or wins(self.grid, opponent(self.player)) or len(empty_cells(self.grid)) == 0

    def actions(self):
        return empty_cells(self.grid)
    
    def result(self, action):
        row = action[0]
        col = action[1]

        grid = copy.deepcopy(self.grid)
        grid[row][col] = opponent(self.player) if self.opponent_action else self.player 

        return State(grid, opponent(self.player), self.opponent_action)
    
    def utility(self, player = None):
        if player == None: 
            player = self.player 

        if wins(self.grid, player):
            return 1 
        
        return -1 if wins(self.grid, opponent(player)) else 0

    def print(self):
        print("max" if self.player == -1 else "min")
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == None:
                    print("-", end='')
                else:
                    print(self.grid[i][j], end='')
            print()
        print()

