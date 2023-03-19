import random 

class Random():
    def __init__(self, game, player) -> None:
        self.game = game 
        self.player = player 
    
    def next_move(self, state):
        actions = self.game.actions(state)
        return random.choice(actions)