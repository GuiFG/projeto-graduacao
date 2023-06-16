import time
import math
from copy import deepcopy
import random

import utils
from utils import BLACK_PIECE, WHITE_PIECE, EMPTY_SQUARE

from PlayerAI import Player


class Node:
    def __init__(self, board, move=None, parent=None, value=None):
        self.board = board
        self.value = value
        self.move = move
        self.parent = parent

    def get_children(self, minimizing_player, mandatory_jumping):
        current_state = deepcopy(self.board)
        available_moves = []
        children_states = []
        big_letter = ""
        queen_row = 0
        if minimizing_player is True:
            big_letter = WHITE_PIECE
            available_moves = utils.find_available_moves(
                current_state, big_letter, mandatory_jumping)
            queen_row = 7
        else:
            big_letter = BLACK_PIECE
            available_moves = utils.find_available_moves(
                current_state, big_letter, mandatory_jumping)
            queen_row = 0

        for i in range(len(available_moves)):
            old_i = available_moves[i][0]
            old_j = available_moves[i][1]
            new_i = available_moves[i][2]
            new_j = available_moves[i][3]
            state = deepcopy(current_state)
            utils.make_a_move(state, old_i, old_j, new_i,
                              new_j, big_letter, queen_row)
            children_states.append(Node(state, [old_i, old_j, new_i, new_j]))

        return children_states

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def get_board(self):
        return self.board

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent


class Game:
    def __init__(self):
        self.matrix = [[], [], [], [], [], [], [], []]
        self.matrix_state = ''
        self.black_pieces = 12  # B
        self.white_pieces = 12  # C
        self.available_moves = []
        self.mandatory_jumping = True
        self.positions = []
        self.max_repeat = 3
        self.max_no_capture = 40
        self.count_no_capture = 0


        for row in self.matrix:
            for i in range(8):
                row.append(EMPTY_SQUARE)
        self.position_black()
        self.position_white()

    def position_white(self):
        for i in range(3):
            for j in range(8):
                if (i + j) % 2 == 1:
                    self.matrix[i][j] = (WHITE_PIECE.lower() + str(i) + str(j))

    def position_black(self):
        for i in range(5, 8, 1):
            for j in range(8):
                if (i + j) % 2 == 1:
                    self.matrix[i][j] = (BLACK_PIECE.lower() + str(i) + str(j))

    def print_matrix(self):
        i = 0
        print()
        for row in self.matrix:
            print(i, end="  |")
            i += 1
            for elem in row:
                print(elem, end=" ")
            print()
        print()
        for j in range(8):
            if j == 0:
                j = "     0"
            print(j, end="   ")
        print("\n")
 
    def player_play(self, player):
        if player.player == WHITE_PIECE:
            move = self.evaluate_states()
        else:
            move = player.get_action()

        print(f'move of {player.player}: ', move)

        return utils.make_move(self.matrix, move, player.player)

    def check_captures(self, capture):
        self.count_no_capture += 1

        if capture:
            self.count_no_capture = 0
        
        return self.count_no_capture > self.max_no_capture


    @staticmethod
    def calculate_heuristics(board):
        result = 0
        mine = 0
        opp = 0
        for i in range(8):
            for j in range(8):
                if board[i][j][0] == "c" or board[i][j][0] == "C":
                    mine += 1

                    if board[i][j][0] == "c":
                        result += 5
                    if board[i][j][0] == "C":
                        result += 10
                    if i == 0 or j == 0 or i == 7 or j == 7:
                        result += 7
                    if i + 1 > 7 or j - 1 < 0 or i - 1 < 0 or j + 1 > 7:
                        continue
                    if (board[i + 1][j - 1][0] == "b" or board[i + 1][j - 1][0] == "B") and board[i - 1][
                            j + 1] == "---":
                        result -= 3
                    if (board[i + 1][j + 1][0] == "b" or board[i + 1][j + 1] == "B") and board[i - 1][j - 1] == "---":
                        result -= 3
                    if board[i - 1][j - 1][0] == "B" and board[i + 1][j + 1] == "---":
                        result -= 3

                    if board[i - 1][j + 1][0] == "B" and board[i + 1][j - 1] == "---":
                        result -= 3
                    if i + 2 > 7 or i - 2 < 0:
                        continue
                    if (board[i + 1][j - 1][0] == "B" or board[i + 1][j - 1][0] == "b") and board[i + 2][
                            j - 2] == "---":
                        result += 6
                    if i + 2 > 7 or j + 2 > 7:
                        continue
                    if (board[i + 1][j + 1][0] == "B" or board[i + 1][j + 1][0] == "b") and board[i + 2][
                            j + 2] == "---":
                        result += 6

                elif board[i][j][0] == "b" or board[i][j][0] == "B":
                    opp += 1

        return result + (mine - opp) * 1000

    def evaluate_states(self):
        t1 = time.time()
        current_state = Node(deepcopy(self.matrix))

        first_computer_moves = current_state.get_children(
            True, self.mandatory_jumping)
        if len(first_computer_moves) == 0:
            if self.player_pieces > self.computer_pieces:
                print(
                    "Computer has no available moves left, and you have more pieces left.\nYOU WIN!")
                exit()
            else:
                print("Computer has no available moves left.\nGAME ENDED!")
                exit()
        dict = {}
        for i in range(len(first_computer_moves)):
            child = first_computer_moves[i]
            value = Game.minimax(
                child.get_board(), 4, -math.inf, math.inf, False, self.mandatory_jumping)
            dict[value] = child
        if len(dict.keys()) == 0:
            print("Computer has cornered itself.\nYOU WIN!")
            exit()

        move = dict[max(dict)].move
        t2 = time.time()
        diff = t2 - t1
        print("Computer has moved (" + str(move[0]) + "," + str(move[1]) + ") to (" + str(move[2]) + "," + str(
            move[3]) + ").")
        print("It took him " + str(diff) + " seconds.")

        return move

    @staticmethod
    def minimax(board, depth, alpha, beta, maximizing_player, mandatory_jumping):
        if depth == 0:
            return Game.calculate_heuristics(board)
        current_state = Node(deepcopy(board))
        if maximizing_player is True:
            max_eval = -math.inf
            for child in current_state.get_children(True, mandatory_jumping):
                ev = Game.minimax(child.get_board(), depth - 1,
                                  alpha, beta, False, mandatory_jumping)
                max_eval = max(max_eval, ev)
                alpha = max(alpha, ev)
                if beta <= alpha:
                    break
            current_state.set_value(max_eval)
            return max_eval
        else:
            min_eval = math.inf
            for child in current_state.get_children(False, mandatory_jumping):
                ev = Game.minimax(child.get_board(), depth - 1,
                                  alpha, beta, True, mandatory_jumping)
                min_eval = min(min_eval, ev)
                beta = min(beta, ev)
                if beta <= alpha:
                    break
            current_state.set_value(min_eval)
            return min_eval

    def play(self, players):
        print("##### WELCOME TO CHECKERS ####")

        self.mandatory_jumping = True

        while True:
            random.seed(42)
            for player in players:
                capture = self.player_play(player)
                
                self.print_matrix()
                black_pieces, white_pieces = utils.count_pieces(self.matrix)
                
                winner = utils.check_winner(self.matrix, black_pieces, white_pieces)
                if winner is not None:
                    return winner
                
                no_capture = self.check_captures(capture)
                if no_capture:
                    return EMPTY_SQUARE

            draw = utils.check_draw(self.matrix, self.positions)
            if draw:
                return EMPTY_SQUARE


if __name__ == '__main__':
    checkers = Game()

    player1 = Player(checkers.matrix, "B", 2)
    player2 = Player(checkers.matrix, "C", 0)

    winner = checkers.play([player1, player2])

    print(winner)
