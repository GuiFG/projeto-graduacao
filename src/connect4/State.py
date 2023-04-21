import copy 
from utils import *

class State:
    def __init__(self, board):
        self.board = board
    
    def is_terminal(self):
        return is_terminal_node(self.board)
        
    def actions(self):
        return get_valid_locations(self.board)
    
    def result(self, action, player):
        board = copy.deepcopy(self.board)

        row = get_next_open_row(board, action)
        drop_piece(board, row, action, player)

        return State(board)
    
    def utility(self, player):
        if winning_move(self.board, player):
            return 1
        
        return -1 if winning_move(self.board, opponent_player(player)) else 0
    
    def evaluation(self, player):
        score = 0

        # verifica as posicoes promissoras na horizontal
        for row in self.board:
            for i in range(len(row) - 3):
                line = row[i:i+4]
                count, op_count, empty_count = count_player(line, player)

                score += State.get_score_by_count(count, op_count, empty_count)
        
        # verifica as posicoes promissoras na vertical
        for col in range(7):
            column = [self.board[row][col] for row in range(6)]
            for j in range(len(column) - 3):
                line = column[j:j+4]
                count, op_count, empty_count = count_player(line, player)

                score += State.get_score_by_count(count, op_count, empty_count)

        # verifica as posicoes promissoras na diagonal
        for i in range(3):
            for j in range(4):
                subboard = get_sub_board(self.board, i, j)
                diagonal1 = [subboard[x][x] for x in range(4)]
                diagonal2 = [subboard[x][3-x] for x in range(4)]

                count, op_count, empty_count = count_player(diagonal1, player)
                score += State.get_score_by_count(count, op_count, empty_count)

                count, op_count, empty_count = count_player(diagonal2, player)
                score += State.get_score_by_count(count, op_count, empty_count)

        return score
    
    @staticmethod
    def get_score_by_count(count, op_count, empty_count):
        score = 0

        if count == 4:
            score += 100
        elif count == 3 and empty_count == 1:
            score += 10
        elif count == 2 and empty_count == 2:
            score += 1
        elif op_count == 4:
            score -= 100
        elif op_count == 3 and empty_count == 1:
            score -= 10
        elif op_count == 2 and empty_count == 2:
            score -= 1


        return score

