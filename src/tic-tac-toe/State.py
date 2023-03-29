import copy 
from utils import wins, opponent, empty_cells

class State:
    def __init__(self, grid):
        self.grid = grid
    
    def is_terminal(self):
        return wins(self.grid, 'X') or wins(self.grid, '0') or len(empty_cells(self.grid)) == 0

    def actions(self):
        if self.is_terminal():
            return [] 
        
        return empty_cells(self.grid)
    
    def result(self, action, player):
        row = action[0]
        col = action[1]

        grid = copy.deepcopy(self.grid)
        grid[row][col] = player

        return State(grid)
    
    def utility(self, player):
        if wins(self.grid, player):
            return 1 
        
        return -1 if wins(self.grid, opponent(player)) else 0

    def print(self):
        for i in range(3):
            for j in range(3):
                if self.grid[j][i] == None:
                    print("-", end='')
                else:
                    print(self.grid[j][i], end='')
            print()
        print()

