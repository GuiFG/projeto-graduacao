from Checkers import Checkers
from PlayerAI import Player

if __name__ == '__main__':
    checkers = Checkers()

    player1 = Player(checkers.matrix, "B", 5)
    player2 = Player(checkers.matrix, "C", 0)

    winner = checkers.play([player1, player2])

    print(winner)
