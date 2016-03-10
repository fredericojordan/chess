from board import Board

class Game():
    def __init__(self):
        self.whitePlayer = Player()
        self.blackPlayer = Player()
        self.board = Board()

class Player():
    pass

game = Game()
game.board._print()