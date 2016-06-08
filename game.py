from board import Board
from random import randint

class Game():
    def __init__(self):
        self.whitePlayer = Player('white')
        self.blackPlayer = Player('black')
        self.board = Board()
        self.nextPlayer = self.whitePlayer

    def move(self, initialPosition, finalPosition):
        if self.canMove(initialPosition, finalPosition):
            self.board.makeMove(initialPosition, finalPosition)
            self.changePlayer()
            return True
        return False

    def canMove(self, initialPosition, finalPosition):
        return self.board.isValidPosition(initialPosition) and \
            self.board.isValidPosition(finalPosition) and \
            not self.board.isEmpty(initialPosition) and \
            self.board.getPiece(initialPosition).color == self.nextPlayer.color and \
            self.board.canMove(initialPosition, finalPosition)
    
    def aiMove(self):
        moves = self.getAllLegalMoves()
        print(str(len(moves)) + " legal moves: " + str(moves))
        rand_i = randint(0, len(moves)-1)
        chosen_move = moves[rand_i]
        self.move(chosen_move[0:2],chosen_move[2:4])
        
    def changePlayer(self):
        if self.nextPlayer == self.whitePlayer:
            self.nextPlayer = self.blackPlayer
        else:
            self.nextPlayer = self.whitePlayer
            
    def getLegalMoves(self, initial_position):
        legal_moves = []
        for final_position in self.board.getAllPositions():
            if self.canMove(initial_position, final_position):
                legal_moves.append(initial_position + final_position)
        return legal_moves
    
    def getAllLegalMoves(self):
        legal_moves = []
        for pos in self.board.getAllNonEmptyPositions():
            for move in self.getLegalMoves(pos):
                legal_moves.append(move)
        return legal_moves

class Player():
        def __init__(self, player_color):
            self.color = player_color