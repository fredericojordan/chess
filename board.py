from pieces import Pawn, Knight, Bishop, Rook, Queen, King, Box

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
            self.putPiece(Pawn('black'), Box(1, i))
            self.putPiece(Pawn('white'), Box(-2, i))
            
        self.putPiece(Rook('black'), Box(0, 0))
        self.putPiece(Knight('black'), Box(0, 1))
        self.putPiece(Bishop('black'), Box(0, 2))
        self.putPiece(Queen('black'), Box(0, 3))
        self.putPiece(King('black'), Box(0, 4))
        self.putPiece(Bishop('black'), Box(0, 5))
        self.putPiece(Knight('black'), Box(0, 6))
        self.putPiece(Rook('black'), Box(0, 7))
        
        self.putPiece(Rook('white'), Box(-1, 0))
        self.putPiece(Knight('white'), Box(-1, 1))
        self.putPiece(Bishop('white'), Box(-1, 2))
        self.putPiece(Queen('white'), Box(-1, 3))
        self.putPiece(King('white'), Box(-1, 4))
        self.putPiece(Bishop('white'), Box(-1, 5))
        self.putPiece(Knight('white'), Box(-1, 6))
        self.putPiece(Rook('white'), Box(-1, 7))
        
    def move(self, initialPosition, finalPosition):
        moving_piece = self.getPiece(initialPosition)
        
        if not moving_piece.isValidMove(initialPosition, finalPosition, self) or self.isInvalidJump(initialPosition, finalPosition):
            return False
        
#         If the player was previous under check and the move does not remove the check, it must be undone.
#         If the move exposes check, it must be undone / disallowed.
#         If the moving_piece is a pawn reaching the back rank, promote it.
#         If the move is a castling, set the new position of the rook accordingly. But a king and rook can only castle if they haven't moved, so you need to keep track of that. And if the king moves through a check to castle, that's disallowed, too.
#         If the move results in a stalemate or checkmate, the game is over.

        if not self.isEmpty(finalPosition) and self.getPiece(finalPosition).color == moving_piece.color:
            print("Can't capture own piece")
            return False

        self.makeMove(initialPosition, finalPosition)
        return True
        
    def makeMove(self, initialPosition, finalPosition):
        print('Making move ' + str(initialPosition) + ' to ' + str(finalPosition))
        moving_piece = self.getPiece(initialPosition)
        self.removePiece(finalPosition)
        self.putPiece(moving_piece, finalPosition)
        self.removePiece(initialPosition)
        moving_piece.hasMoved = True
    
    def isInvalidJump(self, initialPosition, finalPosition):
        if ( isinstance(self.getPiece(initialPosition), Knight) ):
            return False
        
        for box in self.getInBetweenBoxes(initialPosition, finalPosition):
            if not self.isEmpty(box):
                print("Invalid move: can't jump like that!")
                return True
        
        return False
        
            
    def putPiece(self, piece, position):
        self[position.row][position.col] = piece
        
    def removePiece(self, position):
        self[position.row][position.col] = Board.EMPTY_BOX
        
    def getPiece(self, position):
        return self[position.row][position.col]
    
    def isEmpty(self, position):
        return self[position.row][position.col] == Board.EMPTY_BOX
    
    def getInBetweenBoxes(self, initialPosition, finalPosition):
        boxes = []
        if ( initialPosition.row == finalPosition.row ):
            max_col = max(initialPosition.col, finalPosition.col)
            min_col = min(initialPosition.col, finalPosition.col)+1
            for col in range(min_col, max_col):
                boxes.append(Box(initialPosition.row, col))
        elif ( initialPosition.col == finalPosition.col ):
            max_row = max(initialPosition.row, finalPosition.row)
            min_row = min(initialPosition.row, finalPosition.row)+1
            for row in range(min_row, max_row):
                boxes.append(Box(row, initialPosition.col))
        elif ( abs(finalPosition.col-initialPosition.col) == abs(finalPosition.row-initialPosition.row) and
               abs(finalPosition.col-initialPosition.col) > 1 ):
            d_row = finalPosition.row-initialPosition.row
            d_col = finalPosition.col-initialPosition.col
            if ( d_row*d_col < 0 ):
                min_row = min(initialPosition.row, finalPosition.row)+1
                max_col = max(initialPosition.col, finalPosition.col)-1
                for diff in range(abs(d_row)-1):
                    boxes.append(Box(min_row+diff, max_col-diff))
            else:
                min_row = min(initialPosition.row, finalPosition.row)+1
                min_col = min(initialPosition.col, finalPosition.col)+1
                for diff in range(abs(d_row)-1):
                    boxes.append(Box(min_row+diff, min_col+diff))
        return boxes
