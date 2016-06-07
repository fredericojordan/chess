class Piece():
    def __init__(self, color):
        self.color = color
        self.hasMoved = False
    
    def isValidMove(self, inital_position, final_position, board):
        if self.isNotMoving(inital_position, final_position):
            return False
        else:
            return True
    
    def isNotMoving(self, initialPosition, finalPosition):
        if ( initialPosition == finalPosition ):
#             print('Stationary move')
            return True
        else:
            return False

class Pawn(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        
    def __repr__(self):
        if self.color == 'white':
#             return u'\u2659'
            return 'wp'
        if self.color == 'black':
#             return u'\u265F'
            return 'bp'
        
    
    def isValidMove(self, initialPosition, finalPosition, board):
        if not Piece.isValidMove(self, initialPosition, finalPosition, board):
            return False
        
        if (self.isValidWalk(initialPosition, finalPosition, board) or
            self.isValidCapture(initialPosition, finalPosition, board) ):
            return True
        else:
#             print('Invalid pawn move')
            return False
    
    def isValidWalk(self, initialPosition, finalPosition, board):
        d_row = Box(finalPosition).row - Box(initialPosition).row
        d_col = Box(finalPosition).col - Box(initialPosition).col
        
        if d_col == 0:
            if self.color == 'white':
                if ( d_row == -1 or
                     (d_row == -2 and not self.hasMoved) ):
                    return True
            if self.color == 'black':
                if ( d_row == 1 or
                     (d_row == 2 and not self.hasMoved) ):
                    return True

        return False
        
    def isValidCapture(self, initialPosition, finalPosition, board):
        d_row = Box(finalPosition).row - Box(initialPosition).row
        d_col = Box(finalPosition).col - Box(initialPosition).col
        
        if abs(d_col) == 1 and not board.isEmpty(finalPosition):
            if (self.color == 'white' and
                d_row == -1 and
                board.getPiece(finalPosition).color == 'black'):
                return True
            if (self.color == 'black' and
                d_row == 1 and
                board.getPiece(finalPosition).color == 'white'):
                return True            

class Knight(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
    
    def __repr__(self):
        if self.color == 'white':
#             return u'\u2658'
            return 'wN'
        if self.color == 'black':
#             return u'\u265E'
            return 'bN'
    
    def isValidMove(self, initialPosition, finalPosition, board):
        if not Piece.isValidMove(self, initialPosition, finalPosition, board):
            return False
        
        d_row = Box(finalPosition).row - Box(initialPosition).row
        d_col = Box(finalPosition).col - Box(initialPosition).col
        if ( abs(d_col) == 1 and abs(d_row) == 2 or
             abs(d_col) == 2 and abs(d_row) == 1 ):
                return True
        
#         print('Invalid knight move')
        return False

class Bishop(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
    
    def __repr__(self):
        if self.color == 'white':
#             return u'\u2657'
            return 'wB'
        if self.color == 'black':
#             return u'\u265D'
            return 'bB'

    def isValidMove(self, initialPosition, finalPosition, board):
        if not Piece.isValidMove(self, initialPosition, finalPosition, board):
            return False
        
        d_row = Box(finalPosition).row - Box(initialPosition).row
        d_col = Box(finalPosition).col - Box(initialPosition).col
        if ( abs(d_col) == abs(d_row) ):
                return True
        
#         print('Invalid bishop move')
        return False

class Rook(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        
    def __repr__(self):
        if self.color == 'white':
#             return u'\u2656'
            return 'wR'
        if self.color == 'black':
#             return u'\u265C'
            return 'bR'
    
    def isValidMove(self, initialPosition, finalPosition, board):
        if not Piece.isValidMove(self, initialPosition, finalPosition, board):
            return False
        
        d_row = Box(finalPosition).row - Box(initialPosition).row
        d_col = Box(finalPosition).col - Box(initialPosition).col
        if ( d_row == 0 or
             d_col == 0 ):
                return True
        
#         print('Invalid rook move')
        return False

class Queen(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        
    def __repr__(self):
        if self.color == 'white':
#             return u'\u2655'
            return 'wQ'
        if self.color == 'black':
#             return u'\u265B'
            return 'bQ'
    
    def isValidMove(self, initialPosition, finalPosition, board):
        if not Piece.isValidMove(self, initialPosition, finalPosition, board):
            return False
        
        if ( Bishop.isValidMove(self, initialPosition, finalPosition, board) or
             Rook.isValidMove(self, initialPosition, finalPosition, board) ):
            return True
        
#         print('Invalid queen move')
        return False

class King(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        
    def __repr__(self):
        if self.color == 'white':
#             return u'\u2654'
            return 'wK'
        if self.color == 'black':
#             return u'\u265A'
            return 'bK'
    
    def isValidMove(self, initialPosition, finalPosition, board):
        if not Piece.isValidMove(self, initialPosition, finalPosition, board):
            return False
        
        d_row = Box(finalPosition).row - Box(initialPosition).row
        d_col = Box(finalPosition).col - Box(initialPosition).col
        
        if ( abs(d_row) <= 1 and
             abs(d_col) <= 1 ):
                return True
            
        if self.isValidCastle(initialPosition, finalPosition, board):
            print('Castle!')
            return True
        
#         print('Invalid king move')
        return False
    
    def isValidCastle(self, initialPosition, finalPosition, board):
        d_row = Box(finalPosition).row - Box(initialPosition).row
        d_col = Box(finalPosition).col - Box(initialPosition).col
        
        if ( not self.hasMoved and d_row == 0 and abs(d_col) == 2 ):
            if ( d_col > 0 ):
                rookInitialPosition = Box.makePos(Box(initialPosition).row, 7)
            else:
                rookInitialPosition = Box.makePos(Box(initialPosition).row, 0)
            
            if ( not board.getPiece(rookInitialPosition).hasMoved and \
                 board.isPathClear(initialPosition, rookInitialPosition) and \
                 board.pathIsNotInCheck(initialPosition, rookInitialPosition) ):
                board.makeMove(rookInitialPosition, board.getInBetweenPositions(initialPosition, finalPosition)[0])
                return True
        
        return False

class Box():
    def __init__(self, position):
        self.position = position
        self.row = self.getRow(position)
        self.col = self.getCol(position)
        
    def __repr__(self):
        return self.position
    
    def getRow(self, position):
        return 8-int(position[1])
    
    def getCol(self, position):
        cols = { 'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7 }
        return cols[position[0].lower()]
    
    @classmethod
    def makePos(cls, row, col):
        COLS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        return COLS[col] + str(8-row)