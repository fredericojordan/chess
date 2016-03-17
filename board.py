from pieces import Pawn, Knight, Bishop, Rook, Queen, King, Box

class Board(list):
#     EMPTY_BOX = None
    EMPTY_BOX = ''
    COLS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    ROWS = ['1', '2', '3', '4', '5', '6', '7', '8']
    
    def __init__(self):
        self.makeBoxes()
        self.populate()
        
    def makeBoxes(self):
        del self[:]
        for _ in range(8):
            self.append([Board.EMPTY_BOX for _ in range(8)])
    
    def _print(self):
        print('')
        for i in range(len(Board.ROWS)):
            print( str(8-i) + " " + str(self[i]) )
        print('   a   b   c   d   e   f   g   h')
            
    def populate(self):
        for col in Board.COLS:
            self.putPiece(Pawn('black'), col+'7')
            self.putPiece(Pawn('white'), col+'2')
             
        self.putPiece(Rook('black'), 'a8')
        self.putPiece(Knight('black'), 'b8')
        self.putPiece(Bishop('black'), 'c8')
        self.putPiece(Queen('black'), 'd8')
        self.putPiece(King('black'), 'e8')
        self.putPiece(Bishop('black'), 'f8')
        self.putPiece(Knight('black'), 'g8')
        self.putPiece(Rook('black'), 'h8')
         
        self.putPiece(Rook('white'), 'a1')
        self.putPiece(Knight('white'), 'b1')
        self.putPiece(Bishop('white'), 'c1')
        self.putPiece(Queen('white'), 'd1')
        self.putPiece(King('white'), 'e1')
        self.putPiece(Bishop('white'), 'f1')
        self.putPiece(Knight('white'), 'g1')
        self.putPiece(Rook('white'), 'h1')
        
    def move(self, initialPosition, finalPosition):
        moving_piece = self.getPiece(initialPosition)
        
        if not self.isPathClear(initialPosition, finalPosition) or not moving_piece.isValidMove(initialPosition, finalPosition, self):
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
        self.checkForPromotion(finalPosition)
        return True
        
    def makeMove(self, initialPosition, finalPosition):
        print('Making move ' + str(initialPosition) + ' to ' + str(finalPosition))
        moving_piece = self.getPiece(initialPosition)
        self.removePiece(finalPosition)
        self.putPiece(moving_piece, finalPosition)
        self.removePiece(initialPosition)
        moving_piece.hasMoved = True
    
    def checkForPromotion(self, position):
        if ( isinstance(self.getPiece(position), Pawn) ):
            if ( (self.getPiece(position).color == 'white' and Box(position).row == 0) or 
                 (self.getPiece(position).color == 'black' and Box(position).row == 7) ):
                self.promote(position)
            
    def promote(self, position):
        color = self.getPiece(position).color
        self.removePiece(position)
        self.putPiece(Queen(color), position)
        
    def isValidPosition(self, position):
        if (position[0] in Board.COLS and
            position[1] in Board.ROWS):
            return True
        else:
            return False
    
    def isPathClear(self, initialPosition, finalPosition):
        if ( isinstance(self.getPiece(initialPosition), Knight) ):
            return True
        
        for position in self.getInBetweenPositions(initialPosition, finalPosition):
            if not self.isEmpty(position):
                print("Invalid move: path is not clear!")
                return False
        
        return True
        
            
    def putPiece(self, piece, position):
        self[Box(position).row][Box(position).col] = piece
        
    def removePiece(self, position):
        self[Box(position).row][Box(position).col] = Board.EMPTY_BOX
        
    def getPiece(self, position):
        return self[Box(position).row][Box(position).col]
    
    def isEmpty(self, position):
        return self[Box(position).row][Box(position).col] == Board.EMPTY_BOX
    
    def getInBetweenPositions(self, initialPosition, finalPosition):
        positions = []
        min_row = min(Box(finalPosition).row, Box(initialPosition).row)
        min_col = min(Box(finalPosition).col, Box(initialPosition).col)
        d_row = Box(finalPosition).row - Box(initialPosition).row
        d_col = Box(finalPosition).col - Box(initialPosition).col
        
        if d_row == 0:
            for i in range(1, abs(d_col)):
                positions.append(Box.makePos(Box(initialPosition).row, min_col+i))
        
        if d_col == 0:
            for i in range(1, abs(d_row)):
                positions.append(Box.makePos(min_row+i, Box(initialPosition).col))
        
        if abs(d_row) == abs(d_col):
            if ( d_row*d_col > 0 ):
                for i in range(1, abs(d_row)):
                    positions.append(Box.makePos(min_row+i, min_col+i))
            else:
                max_col = max(Box(finalPosition).col, Box(initialPosition).col)
                for i in range(1, abs(d_row)):
                    positions.append(Box.makePos(min_row+i, max_col-i))
        
        return positions
