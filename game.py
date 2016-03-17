from board import Board

class Game():
    def __init__(self):
        self.whitePlayer = Player()
        self.blackPlayer = Player()
        self.board = Board()
        self.nextPlayer = self.whitePlayer
    
    def move(self, initialPosition, finalPosition):
        if not ( self.board.isValidPosition(initialPosition) and self.board.isValidPosition(finalPosition) ):
            print("Invalid position!")
            return False
        
        if ( self.board.isEmpty(initialPosition) ):
            print('Invalid move: initial position is empty!')
            return False
        
        moving_piece = self.board.getPiece(initialPosition)
        
        if ( (self.nextPlayer == self.whitePlayer and moving_piece.color == 'black') or 
             (self.nextPlayer == self.blackPlayer and moving_piece.color == 'white') ):
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

game.move('e2', 'e4') # e4
game.move('d7', 'd5') # ...d5

game.move('b1', 'c3') # Nc3
game.move('d5', 'e4') # ...dxe4
    
game.move('j9', 'f3') # INVALID POSITIONS
game.move('h1', 'h8') # Rh7 (INVALID JUMP BY ROOK)
game.move('f1', 'h3') # Bh3 (INVALID JUMP BY BISHOP)
game.move('c1', 'g5') # Bg5 (INVALID JUMP BY BISHOP)   
game.move('f1', 'c4') # Bc4
game.move('c7', 'c5') # ...c5

game.move('g1', 'f3') # Nf3
game.move('b7', 'b6') # ...b6

game.move('e1', 'g1') # O-O

game.board._print()