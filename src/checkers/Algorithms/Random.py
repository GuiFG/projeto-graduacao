import random

from utils import find_available_moves

class Random:
    def get_move(board, player):
        return random.choice(find_available_moves(board, player))