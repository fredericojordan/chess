class Piece():
    def __init__(self, color):
        self.color = color
    
    def __repr__(self):
        return self.color[0] + self.pieceCode()

class Pawn(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.hasMoved = False
        
    def pieceCode(self):
        return 'p'

class Knight(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
    
    def pieceCode(self):
        return 'n'

class Bishop(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
    
    def pieceCode(self):
        return 'b'

class Rook(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.hasMoved = False
        
    def pieceCode(self):
        return 'r'

class Queen(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        
    def pieceCode(self):
        return 'q'

class King(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.hasMoved = False
        
    def pieceCode(self):
        return 'k'