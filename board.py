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
        for row in self:
            print(row)
            
    def populate(self):
        for i in range(8):
            self.putPiece(Pawn('black'), 0, i)
            self.putPiece(Pawn('white'), -2, i)
            
        self.putPiece(Rook('black'), 1, 0)
        self.putPiece(Knight('black'), 1, 1)
        self.putPiece(Bishop('black'), 1, 2)
        self.putPiece(Queen('black'), 1, 3)
        self.putPiece(King('black'), 1, 4)
        self.putPiece(Bishop('black'), 1, 5)
        self.putPiece(Knight('black'), 1, 6)
        self.putPiece(Rook('black'), 1, 7)
        
        self.putPiece(Rook('white'), -1, 0)
        self.putPiece(Knight('white'), -1, 1)
        self.putPiece(Bishop('white'), -1, 2)
        self.putPiece(Queen('white'), -1, 3)
        self.putPiece(King('white'), -1, 4)
        self.putPiece(Bishop('white'), -1, 5)
        self.putPiece(Knight('white'), -1, 6)
        self.putPiece(Rook('white'), -1, 7)
            
    def putPiece(self, piece, row, col):
        self[row][col] = piece
        
    def removePiece(self, row, col):
        self[row][col] = Board.EMPTY_BOX
        