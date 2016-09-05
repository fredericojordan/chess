'''
Created on 2 de set de 2016

@author: fvj
'''
import sys, pygame, chess
pygame.init()

SQUARE_SIDE = 50
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT) = (8*SQUARE_SIDE, 8*SQUARE_SIDE)

LIGHT_GRAY = (240,240,240)
DARK_GRAY  = (200,200,200)

BLACK_KING   = pygame.transform.scale(pygame.image.load("images/black_king.png"),   (SQUARE_SIDE,SQUARE_SIDE) )
BLACK_QUEEN  = pygame.transform.scale(pygame.image.load("images/black_queen.png"),  (SQUARE_SIDE,SQUARE_SIDE) )
BLACK_ROOK   = pygame.transform.scale(pygame.image.load("images/black_rook.png"),   (SQUARE_SIDE,SQUARE_SIDE) )
BLACK_BISHOP = pygame.transform.scale(pygame.image.load("images/black_bishop.png"), (SQUARE_SIDE,SQUARE_SIDE) )
BLACK_KNIGHT = pygame.transform.scale(pygame.image.load("images/black_knight.png"), (SQUARE_SIDE,SQUARE_SIDE) )
BLACK_PAWN   = pygame.transform.scale(pygame.image.load("images/black_pawn.png"),   (SQUARE_SIDE,SQUARE_SIDE) )

WHITE_KING   = pygame.transform.scale(pygame.image.load("images/white_king.png"),   (SQUARE_SIDE,SQUARE_SIDE) )
WHITE_QUEEN  = pygame.transform.scale(pygame.image.load("images/white_queen.png"),  (SQUARE_SIDE,SQUARE_SIDE) )
WHITE_ROOK   = pygame.transform.scale(pygame.image.load("images/white_rook.png"),   (SQUARE_SIDE,SQUARE_SIDE) )
WHITE_BISHOP = pygame.transform.scale(pygame.image.load("images/white_bishop.png"), (SQUARE_SIDE,SQUARE_SIDE) )
WHITE_KNIGHT = pygame.transform.scale(pygame.image.load("images/white_knight.png"), (SQUARE_SIDE,SQUARE_SIDE) )
WHITE_PAWN   = pygame.transform.scale(pygame.image.load("images/white_pawn.png"),   (SQUARE_SIDE,SQUARE_SIDE) )

CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode(SCREEN_SIZE)

def print_empty_board():
    SCREEN.fill(LIGHT_GRAY)
    print_dark_squares()

def print_dark_squares():
    for position in chess.single_gen(chess.DARK_SQUARES):
        square = chess.bb2str(position)
        col = chess.FILES.index(square[0])
        row = 7-chess.RANKS.index(square[1])
        pygame.draw.rect(SCREEN, DARK_GRAY, (SQUARE_SIDE*col,SQUARE_SIDE*row,SQUARE_SIDE,SQUARE_SIDE), 0)
            
def get_square(square):
    col = chess.FILES.index(square[0])
    row = 7-chess.RANKS.index(square[1])
    return pygame.Rect((col*SQUARE_SIDE, row*SQUARE_SIDE), (SQUARE_SIDE,SQUARE_SIDE))

def print_initial_board():
    print_empty_board()
    
    SCREEN.blit(BLACK_ROOK,   get_square('a8'))
    SCREEN.blit(BLACK_KNIGHT, get_square('b8'))
    SCREEN.blit(BLACK_BISHOP, get_square('c8'))
    SCREEN.blit(BLACK_QUEEN,  get_square('d8'))
    SCREEN.blit(BLACK_KING,   get_square('e8'))
    SCREEN.blit(BLACK_BISHOP, get_square('f8'))
    SCREEN.blit(BLACK_KNIGHT, get_square('g8'))
    SCREEN.blit(BLACK_ROOK,   get_square('h8'))
    
    SCREEN.blit(BLACK_PAWN, get_square('a7'))
    SCREEN.blit(BLACK_PAWN, get_square('b7'))
    SCREEN.blit(BLACK_PAWN, get_square('c7'))
    SCREEN.blit(BLACK_PAWN, get_square('d7'))
    SCREEN.blit(BLACK_PAWN, get_square('e7'))
    SCREEN.blit(BLACK_PAWN, get_square('f7'))
    SCREEN.blit(BLACK_PAWN, get_square('g7'))
    SCREEN.blit(BLACK_PAWN, get_square('h7'))
    
    SCREEN.blit(WHITE_ROOK,   get_square('a1'))
    SCREEN.blit(WHITE_KNIGHT, get_square('b1'))
    SCREEN.blit(WHITE_BISHOP, get_square('c1'))
    SCREEN.blit(WHITE_QUEEN,  get_square('d1'))
    SCREEN.blit(WHITE_KING,   get_square('e1'))
    SCREEN.blit(WHITE_BISHOP, get_square('f1'))
    SCREEN.blit(WHITE_KNIGHT, get_square('g1'))
    SCREEN.blit(WHITE_ROOK,   get_square('h1'))
     
    SCREEN.blit(WHITE_PAWN, get_square('a2'))
    SCREEN.blit(WHITE_PAWN, get_square('b2'))
    SCREEN.blit(WHITE_PAWN, get_square('c2'))
    SCREEN.blit(WHITE_PAWN, get_square('d2'))
    SCREEN.blit(WHITE_PAWN, get_square('e2'))
    SCREEN.blit(WHITE_PAWN, get_square('f2'))
    SCREEN.blit(WHITE_PAWN, get_square('g2'))
    SCREEN.blit(WHITE_PAWN, get_square('h2'))
    
def print_board(board):
    print_empty_board()
    
    for position in chess.colored_piece_gen(board, chess.KING, chess.BLACK):
        SCREEN.blit(BLACK_KING, get_square(chess.bb2str(position)))
    for position in chess.colored_piece_gen(board, chess.QUEEN, chess.BLACK):
        SCREEN.blit(BLACK_QUEEN, get_square(chess.bb2str(position)))
    for position in chess.colored_piece_gen(board, chess.ROOK, chess.BLACK):
        SCREEN.blit(BLACK_ROOK, get_square(chess.bb2str(position)))
    for position in chess.colored_piece_gen(board, chess.BISHOP, chess.BLACK):
        SCREEN.blit(BLACK_BISHOP, get_square(chess.bb2str(position)))
    for position in chess.colored_piece_gen(board, chess.KNIGHT, chess.BLACK):
        SCREEN.blit(BLACK_KNIGHT, get_square(chess.bb2str(position)))
    for position in chess.colored_piece_gen(board, chess.PAWN, chess.BLACK):
        SCREEN.blit(BLACK_PAWN, get_square(chess.bb2str(position)))
        
    for position in chess.colored_piece_gen(board, chess.KING, chess.WHITE):
        SCREEN.blit(WHITE_KING, get_square(chess.bb2str(position)))
    for position in chess.colored_piece_gen(board, chess.QUEEN, chess.WHITE):
        SCREEN.blit(WHITE_QUEEN, get_square(chess.bb2str(position)))
    for position in chess.colored_piece_gen(board, chess.ROOK, chess.WHITE):
        SCREEN.blit(WHITE_ROOK, get_square(chess.bb2str(position)))
    for position in chess.colored_piece_gen(board, chess.BISHOP, chess.WHITE):
        SCREEN.blit(WHITE_BISHOP, get_square(chess.bb2str(position)))
    for position in chess.colored_piece_gen(board, chess.KNIGHT, chess.WHITE):
        SCREEN.blit(WHITE_KNIGHT, get_square(chess.bb2str(position)))
    for position in chess.colored_piece_gen(board, chess.PAWN, chess.WHITE):
        SCREEN.blit(WHITE_PAWN, get_square(chess.bb2str(position)))
    
 
game = chess.Game('1r1q2k1/B4p1p/4r1p1/3n2P1/b4P2/7P/8/3R2K1 w - - 1 28')
print_board(game.board)
 
while True:
    CLOCK.tick(15)
     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
         
    pygame.display.flip()