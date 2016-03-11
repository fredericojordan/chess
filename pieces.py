class Piece():
    def __init__(self, color):
        self.color = color
        self.hasMoved = False
    
    def __repr__(self):
        return self.color[0] + self.type()
    
    def isValidMove(self, inital_position, final_position, board):
        if (self.isNotMoving(inital_position, final_position) or
            self.isOutOfBounds(inital_position) or
            self.isOutOfBounds(final_position) ):
            return False
        else:
            return True
    
    def isNotMoving(self, inital_position, final_position):
        if (inital_position.row == final_position.row and
            inital_position.col == final_position.col ):
            print('Stationary move')
            return True
        else:
            return False
    
    def isOutOfBounds(self, position):
        if not (self.isOnBoard(position.row) and
                    self.isOnBoard(position.col)):
            print('Out of bounds')
            return True
        else:
            return False
    
    def isOnBoard(self, index):
        if index < 0 or index > 7:
            return False
        else:
            return True

class Pawn(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        
    def type(self):
        return 'p'
    
    def isValidMove(self, inital_position, final_position, board):
        if not Piece.isValidMove(self, inital_position, final_position, board):
            return False
        
        if (self.isValidWalk(inital_position, final_position, board) or
            self.isValidCapture(inital_position, final_position, board) ):
            return True
        else:
            print('Invalid pawn move')
            return False
    
    def isValidWalk(self, inital_position, final_position, board):
        d_row = final_position.row - inital_position.row
        d_col = final_position.col - inital_position.col
        
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
        
    def isValidCapture(self,inital_position, final_position, board):
        d_row = final_position.row - inital_position.row
        d_col = final_position.col - inital_position.col
        
        if abs(d_col) == 1 and not board.isEmpty(final_position):
            if (self.color == 'white' and
                d_row == -1 and
                board.getPiece(final_position).color == 'black'):
                return True
            if (self.color == 'black' and
                d_row == 1 and
                board.getPiece(final_position).color == 'white'):
                return True            

class Knight(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
    
    def type(self):
        return 'n'
    
    def isValidMove(self, inital_position, final_position, board):
        if not Piece.isValidMove(self, inital_position, final_position, board):
            return False
        
        d_row = abs(final_position.row - inital_position.row)
        d_col = abs(final_position.col - inital_position.col)
        if ( d_col == 1 and d_row == 2 or
             d_col == 2 and d_row == 1 ):
                return True
        
        print('Invalid knight move')
        return False

class Bishop(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
    
    def type(self):
        return 'b'

    def isValidMove(self, inital_position, final_position, board):
        if not Piece.isValidMove(self, inital_position, final_position, board):
            return False
        
        d_row = abs(final_position.row - inital_position.row)
        d_col = abs(final_position.col - inital_position.col)
        if ( d_col == d_row ):
                return True
        
        print('Invalid bishop move')
        return False

class Rook(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        
    def type(self):
        return 'r'
    
    def isValidMove(self, inital_position, final_position, board):
        if not Piece.isValidMove(self, inital_position, final_position, board):
            return False
        
        d_row = abs(final_position.row - inital_position.row)
        d_col = abs(final_position.col - inital_position.col)
        if ( d_row == 0 or
             d_col == 0 ):
                return True
        
        print('Invalid rook move')
        return False

class Queen(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        
    def type(self):
        return 'q'
    
    def isValidMove(self, inital_position, final_position, board):
        if not Piece.isValidMove(self, inital_position, final_position, board):
            return False
        
        if ( Bishop.isValidMove(self, inital_position, final_position, board) or
             Rook.isValidMove(self, inital_position, final_position, board) ):
            return True
        
        print('Invalid queen move')
        return False

class King(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        
    def type(self):
        return 'k'
    
    def isValidMove(self, inital_position, final_position, board):
        if not Piece.isValidMove(self, inital_position, final_position, board):
            return False
        
        d_row = abs(final_position.row - inital_position.row)
        d_col = abs(final_position.col - inital_position.col)
        if ( d_row <= 1 or
             d_col <= 1 ):
                return True
            
        # TODO: CASTLING
        
        print('Invalid king move')
        return False