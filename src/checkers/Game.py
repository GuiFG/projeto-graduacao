import random
from copy import deepcopy
import utils
from utils import BLACK_PIECE, WHITE_PIECE, EMPTY_SQUARE

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

            utils.update_positions(self.matrix, self.positions)
            draw = utils.check_draw(self.positions)
            if draw:
                return EMPTY_SQUARE

