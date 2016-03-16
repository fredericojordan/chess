from board import Board, Box

class Game():
    def __init__(self):
        self.whitePlayer = Player()
        self.blackPlayer = Player()
        self.board = Board()
        self.nextPlayer = self.whitePlayer
    
    def move(self, initialPosition, finalPosition):
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

game.move(Box.fromPos('e2'), Box.fromPos('e4')) # e4
game.move(Box.fromPos('d7'), Box.fromPos('d5')) # ...d5
game.move(Box.fromPos('b1'), Box.fromPos('c3')) # nc3
game.move(Box.fromPos('d5'), Box.fromPos('e4')) # ...dxe4
  
game.move(Box.fromPos('h1'), Box.fromPos('h8')) # rh7 (INVALID JUMP BY ROOK)
game.move(Box.fromPos('f1'), Box.fromPos('h3')) # bh3 (INVALID JUMP BY BISHOP)
 
game.move(Box.fromPos('c3'), Box.fromPos('e4')) # ne4

# game.move(Box(-2,4), Box(-4,4)) # e4
# game.move(Box(1,3), Box(3,3)) # ...d5
# game.move(Box(-1,1), Box(-3,2)) # nc3
# game.move(Box(3,3), Box(4,4)) # ...dxe4
#  
# game.move(Box(7,7), Box(0,7)) # rh7 (INVALID JUMP BY ROOK)
# game.move(Box(7,5), Box(5,7)) # bh3 (INVALID JUMP BY BISHOP)
# 
# game.move(Box(5,2), Box(4,4)) # ne4


game.board._print()