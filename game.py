from board import Board, Box

class Game():
    def __init__(self):
        self.whitePlayer = Player()
        self.blackPlayer = Player()
        self.board = Board()
        self.nextPlayer = self.whitePlayer
    
    def move(self, initialPosition, finalPosition):
        piece = self.board[initialPosition.row][initialPosition.col]
        
        if ( piece == Board.EMPTY_BOX ):
            print('Invalid move: initial position is empty!')
            return False
        
        if ( (self.nextPlayer == self.whitePlayer and piece.color == 'black') or 
             (self.nextPlayer == self.blackPlayer and piece.color == 'white') ):
            print('Invalid move: wrong player!')
            return False
        
        if self.board.move(initialPosition, finalPosition):
            self.changePlayer()
            return True
        else:
            return False
        
    def changePlayer(self):
        if self.nextPlayer == self.whitePlayer:
            self.nextPlayer = self.blackPlayer
        else:
            self.nextPlayer = self.whitePlayer

class Player():
    pass

game = Game()
game.board._print()

game.move(Box(-2,4), Box(-4,4)) # e4
game.move(Box(1,3), Box(3,3)) # ...d5
game.move(Box(-1,1), Box(-3,2)) # nc3


game.move(Box(3,3), Box(5,4)) # ...dxe4 (VALID CAPTURE BY PAWN)
game.move(Box(0,7), Box(7,7)) # ...rh1 (INVALID JUMP BY ROOK)

game.board._print()