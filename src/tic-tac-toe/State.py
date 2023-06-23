import copy 
from utils import wins, opponent, empty_cells, count_player

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
        
        if wins(self.grid, opponent(player)): 
            return -1
        
        return 0.5 if self.is_terminal() else 0
        

    def evaluation(self, player):
        score = 0
        op = opponent(player)

        # verifica a contagem nas linhas
        for row in self.grid:
            count = count_player(row, player)
            op_count = count_player(row, op)

            score += State.get_score_by_count(count, op_count)

            
        # verifica a contagem nas colunas
        for col in range(3):
            column = [self.grid[row][col] for row in range(3)]

            count = count_player(column, player)
            op_count = count_player(column, op)

            score += State.get_score_by_count(count, op_count)

        # verifica a contagem nas diagonais
        diagonal1 = [self.grid[i][i] for i in range(3)]
        diagonal2 = [self.grid[i][2-i] for i in range(3)]

        count = count_player(diagonal1, player)
        op_count = count_player(diagonal1, op)
        score += State.get_score_by_count(count, op_count)

        count = count_player(diagonal2, player)
        op_count = count_player(diagonal2, op)
        score += State.get_score_by_count(count, op_count)

        return score
    
    @staticmethod
    def get_score_by_count(count, op_count):
        score = 0
        if count == 2 and op_count == 0:
            score += 10
        elif count == 1 and op_count == 0:
            score += 1
        elif count == 0 and op_count == 2:
            score -= 10
        elif count == 0 and op_count == 1:
            score -= 1

        return score
    
    def get_state_key(self, player):
        key = ''
        for line in self.grid:
            for value in line:
                if value is not None:
                    key += value
                else:
                    key += '9'
        
        return key + player

    @staticmethod
    def get_action_key(action):
        return ''.join([str(a) for a in action]) if action is not None else '9'
    
    @staticmethod
    def get_action_from_key(key):
        return [int(k) for k in key]
    
    

