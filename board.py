from pieces import Pawn, Knight, Bishop, Rook, Queen, King

class Board(list):
#     EMPTY_BOX = None
    EMPTY_BOX = ''
    
    def __init__(self):
        self.makeBoxes()
        self.populate()
        
    def makeBoxes(self):
        del self[:]
        for _ in range(8):
            self.append([Board.EMPTY_BOX for _ in range(8)])
    
    def _print(self):
        print('')
        for row in self:
            print(row)
        print('')
            
    def populate(self):
        for i in range(8):
            self.putPiece(Pawn('black'), 1, i)
            self.putPiece(Pawn('white'), -2, i)
            
        self.putPiece(Rook('black'), 0, 0)
        self.putPiece(Knight('black'), 0, 1)
        self.putPiece(Bishop('black'), 0, 2)
        self.putPiece(Queen('black'), 0, 3)
        self.putPiece(King('black'), 0, 4)
        self.putPiece(Bishop('black'), 0, 5)
        self.putPiece(Knight('black'), 0, 6)
        self.putPiece(Rook('black'), 0, 7)
        
        self.putPiece(Rook('white'), -1, 0)
        self.putPiece(Knight('white'), -1, 1)
        self.putPiece(Bishop('white'), -1, 2)
        self.putPiece(Queen('white'), -1, 3)
        self.putPiece(King('white'), -1, 4)
        self.putPiece(Bishop('white'), -1, 5)
        self.putPiece(Knight('white'), -1, 6)
        self.putPiece(Rook('white'), -1, 7)
    
    def move(self, initialPosition, finalPosition):
        piece = self[initialPosition.row][initialPosition.col]
        
        if not piece.isValidMove(initialPosition, finalPosition, self) or self.isInvalidJump(initialPosition, finalPosition):
            return False
        
#         If the player was previous under check and the move does not remove the check, it must be undone.
#         If the move exposes check, it must be undone / disallowed.
#         If the piece is a pawn reaching the back rank, promote it.
#         If the move is a castling, set the new position of the rook accordingly. But a king and rook can only castle if they haven't moved, so you need to keep track of that. And if the king moves through a check to castle, that's disallowed, too.
#         If the move results in a stalemate or checkmate, the game is over.

        final_box = self[finalPosition.row][finalPosition.col]
        
        if final_box != Board.EMPTY_BOX and final_box.color == piece.color:
            print("Can't capture own piece")
            return False

        self.makeMove(initialPosition, finalPosition)
        return True
        
    def makeMove(self, initialPosition, finalPosition):
        print('Making move ' + str(initialPosition) + ' to ' + str(finalPosition))
        piece = self[initialPosition.row][initialPosition.col]
        self.removePiece(finalPosition.row, finalPosition.col)
        self.putPiece(piece, finalPosition.row, finalPosition.col)
        self.removePiece(initialPosition.row, initialPosition.col)
        piece.hasMoved = True
    
    def isInvalidJump(self, initialPosition, finalPosition):
        if (False): # TODO
            print("Invalid move: can't jump like that!")
            return True
        else:
            return False
        
            
    def putPiece(self, piece, row, col):
        self[row][col] = piece
        
    def removePiece(self, row, col):
        self[row][col] = Board.EMPTY_BOX
        
class Box():
    def __init__(self, row, col):
        if row < 0:
            row += 8
        if col < 0:
            col += 8
        self.row = row
        self.col = col
        
    def __repr__(self):
        return '(' + str(self.row) + ',' + str(self.col) + ')' 