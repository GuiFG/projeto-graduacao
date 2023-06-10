import time
import math
from copy import deepcopy

import utils
from PlayerAI import Player


ansi_black = "\u001b[30m"
ansi_red = "\u001b[31m"
ansi_green = "\u001b[32m"
ansi_yellow = "\u001b[33m"
ansi_blue = "\u001b[34m"
ansi_magenta = "\u001b[35m"
ansi_cyan = "\u001b[36m"
ansi_white = "\u001b[37m"
ansi_reset = "\u001b[0m"

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
            available_moves = utils.find_available_moves(current_state, mandatory_jumping)
            big_letter = "C"
            queen_row = 7
        else:
            available_moves = utils.find_player_available_moves(current_state, mandatory_jumping)
            big_letter = "B"
            queen_row = 0
        for i in range(len(available_moves)):
            old_i = available_moves[i][0]
            old_j = available_moves[i][1]
            new_i = available_moves[i][2]
            new_j = available_moves[i][3]
            state = deepcopy(current_state)
            utils.make_a_move(state, old_i, old_j, new_i, new_j, big_letter, queen_row)
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


class Checkers:
    def __init__(self):
        self.matrix = [[], [], [], [], [], [], [], []]
        self.player_turn = True
        self.computer_pieces = 12
        self.player_pieces = 12
        self.available_moves = []
        self.mandatory_jumping = False

        for row in self.matrix:
            for i in range(8):
                row.append("---")
        self.position_computer()
        self.position_player()

    def position_computer(self):
        for i in range(3):
            for j in range(8):
                if (i + j) % 2 == 1:
                    self.matrix[i][j] = ("c" + str(i) + str(j))

    def position_player(self):
        for i in range(5, 8, 1):
            for j in range(8):
                if (i + j) % 2 == 1:
                    self.matrix[i][j] = ("b" + str(i) + str(j))

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

    def get_player_input(self):
        available_moves = utils.find_player_available_moves(self.matrix, self.mandatory_jumping)
        if len(available_moves) == 0:
            if self.computer_pieces > self.player_pieces:
                print(ansi_red + "You have no moves left, and you have fewer pieces than the computer.YOU LOSE!" + ansi_reset)
                exit()
            else:
                print(ansi_yellow + "You have no available moves.\nGAME ENDED!" + ansi_reset)
                exit()
        self.player_pieces = 0
        self.computer_pieces = 0

        player = Player(self.matrix, "B", 5)
        move = player.get_action()

        print('mcts_move', move)
        old = [str(move[0]), str(move[1])]
        new = [str(move[2]), str(move[3])]

        old_i = old[0]
        old_j = old[1]
        new_i = new[0]
        new_j = new[1]

        move = [int(old_i), int(old_j), int(new_i), int(new_j)]

        utils.make_a_move(self.matrix, int(old_i), int(old_j), int(new_i), int(new_j), "B", 0)
        for m in range(8):
            for n in range(8):
                if self.matrix[m][n][0] == "c" or self.matrix[m][n][0] == "C":
                    self.computer_pieces += 1
                elif self.matrix[m][n][0] == "b" or self.matrix[m][n][0] == "B":
                    self.player_pieces += 1

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

        first_computer_moves = current_state.get_children(True, self.mandatory_jumping)
        if len(first_computer_moves) == 0:
            if self.player_pieces > self.computer_pieces:
                print(
                    ansi_yellow + "Computer has no available moves left, and you have more pieces left.\nYOU WIN!" + ansi_reset)
                exit()
            else:
                print(ansi_yellow + "Computer has no available moves left.\nGAME ENDED!" + ansi_reset)
                exit()
        dict = {}
        for i in range(len(first_computer_moves)):
            child = first_computer_moves[i]
            value = Checkers.minimax(child.get_board(), 4, -math.inf, math.inf, False, self.mandatory_jumping)
            dict[value] = child
        if len(dict.keys()) == 0:
            print(ansi_green + "Computer has cornered itself.\nYOU WIN!" + ansi_reset)
            exit()
        new_board = dict[max(dict)].get_board()
        move = dict[max(dict)].move
        self.matrix = new_board
        t2 = time.time()
        diff = t2 - t1
        print("Computer has moved (" + str(move[0]) + "," + str(move[1]) + ") to (" + str(move[2]) + "," + str(
            move[3]) + ").")
        print("It took him " + str(diff) + " seconds.")

    @staticmethod
    def minimax(board, depth, alpha, beta, maximizing_player, mandatory_jumping):
        if depth == 0:
            return Checkers.calculate_heuristics(board)
        current_state = Node(deepcopy(board))
        if maximizing_player is True:
            max_eval = -math.inf
            for child in current_state.get_children(True, mandatory_jumping):
                ev = Checkers.minimax(child.get_board(), depth - 1, alpha, beta, False, mandatory_jumping)
                max_eval = max(max_eval, ev)
                alpha = max(alpha, ev)
                if beta <= alpha:
                    break
            current_state.set_value(max_eval)
            return max_eval
        else:
            min_eval = math.inf
            for child in current_state.get_children(False, mandatory_jumping):
                ev = Checkers.minimax(child.get_board(), depth - 1, alpha, beta, True, mandatory_jumping)
                min_eval = min(min_eval, ev)
                beta = min(beta, ev)
                if beta <= alpha:
                    break
            current_state.set_value(min_eval)
            return min_eval

    def play(self):
        print(ansi_cyan + "##### WELCOME TO CHECKERS ####" + ansi_reset)
        print("\nSome basic rules:")
        print("1.You enter the coordinates in the form i,j.")
        print("2.You can quit the game at any time by pressing enter.")
        print("3.You can surrender at any time by pressing 's'.")
        print("Now that you've familiarized yourself with the rules, enjoy!")
        
        self.mandatory_jumping = True

        while True:
            self.print_matrix()
            if self.player_turn is True:
                print(ansi_cyan + "\nPlayer's turn." + ansi_reset)
                self.get_player_input()
            else:
                print(ansi_cyan + "Computer's turn." + ansi_reset)
                print("Thinking...")
                self.evaluate_states()
            if self.player_pieces == 0:
                self.print_matrix()
                print(ansi_red + "You have no pieces left.\nYOU LOSE!" + ansi_reset)
                exit()
            elif self.computer_pieces == 0:
                self.print_matrix()
                print(ansi_green + "Computer has no pieces left.\nYOU WIN!" + ansi_reset)
                exit()

            self.player_turn = not self.player_turn
