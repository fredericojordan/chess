'''
Created on 2 de set de 2016

@author: fvj
'''
import sys, pygame, chess
pygame.init()

SIZE = width, height = 400, 400
SQUARE_SIZE = (50,50)
LIGHT_GRAY = 240,240,240
WHITE = 255,255,255

DARK_SQUARE = pygame.image.load("images/gray_square.png")

b_king   = pygame.transform.scale(pygame.image.load("images/black_king.png"), SQUARE_SIZE)
b_queen  = pygame.transform.scale(pygame.image.load("images/black_queen.png"), SQUARE_SIZE)
b_rook   = pygame.transform.scale(pygame.image.load("images/black_rook.png"), SQUARE_SIZE)
b_bishop = pygame.transform.scale(pygame.image.load("images/black_bishop.png"), SQUARE_SIZE)
b_knight = pygame.transform.scale(pygame.image.load("images/black_knight.png"), SQUARE_SIZE)
b_pawn   = pygame.transform.scale(pygame.image.load("images/black_pawn.png"), SQUARE_SIZE)

w_king   = pygame.transform.scale(pygame.image.load("images/white_king.png"), SQUARE_SIZE)
w_queen  = pygame.transform.scale(pygame.image.load("images/white_queen.png"), SQUARE_SIZE)
w_rook   = pygame.transform.scale(pygame.image.load("images/white_rook.png"), SQUARE_SIZE)
w_bishop = pygame.transform.scale(pygame.image.load("images/white_bishop.png"), SQUARE_SIZE)
w_knight = pygame.transform.scale(pygame.image.load("images/white_knight.png"), SQUARE_SIZE)
w_pawn   = pygame.transform.scale(pygame.image.load("images/white_pawn.png"), SQUARE_SIZE)

SQUARE_A8 = DARK_SQUARE.get_rect()

CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode(SIZE)

def print_empty_board():
#     SCREEN.fill(WHITE)
    SCREEN.fill(LIGHT_GRAY)
    print_dark_squares()

def print_dark_squares():
    for col in range(8):
        square_rect = SQUARE_A8.move(col*50, (col+1)%2*50)
        for _ in range(4):
            SCREEN.blit(DARK_SQUARE, square_rect)
            square_rect = square_rect.move([0,100])
            
def get_square(square):
    FILES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    RANKS = ['1', '2', '3', '4', '5', '6', '7', '8']
    col = FILES.index(square[0])
    row = 7-RANKS.index(square[1])
    return SQUARE_A8.move(col*50, row*50)

def print_initial_board():
    print_empty_board()
    
    SCREEN.blit(b_rook,   get_square('a8'))
    SCREEN.blit(b_knight, get_square('b8'))
    SCREEN.blit(b_bishop, get_square('c8'))
    SCREEN.blit(b_queen,  get_square('d8'))
    SCREEN.blit(b_king,   get_square('e8'))
    SCREEN.blit(b_bishop, get_square('f8'))
    SCREEN.blit(b_knight, get_square('g8'))
    SCREEN.blit(b_rook,   get_square('h8'))
    
    SCREEN.blit(b_pawn, get_square('a7'))
    SCREEN.blit(b_pawn, get_square('b7'))
    SCREEN.blit(b_pawn, get_square('c7'))
    SCREEN.blit(b_pawn, get_square('d7'))
    SCREEN.blit(b_pawn, get_square('e7'))
    SCREEN.blit(b_pawn, get_square('f7'))
    SCREEN.blit(b_pawn, get_square('g7'))
    SCREEN.blit(b_pawn, get_square('h7'))
    
    SCREEN.blit(w_rook,   get_square('a1'))
    SCREEN.blit(w_knight, get_square('b1'))
    SCREEN.blit(w_bishop, get_square('c1'))
    SCREEN.blit(w_queen,  get_square('d1'))
    SCREEN.blit(w_king,   get_square('e1'))
    SCREEN.blit(w_bishop, get_square('f1'))
    SCREEN.blit(w_knight, get_square('g1'))
    SCREEN.blit(w_rook,   get_square('h1'))
     
    SCREEN.blit(w_pawn, get_square('a2'))
    SCREEN.blit(w_pawn, get_square('b2'))
    SCREEN.blit(w_pawn, get_square('c2'))
    SCREEN.blit(w_pawn, get_square('d2'))
    SCREEN.blit(w_pawn, get_square('e2'))
    SCREEN.blit(w_pawn, get_square('f2'))
    SCREEN.blit(w_pawn, get_square('g2'))
    SCREEN.blit(w_pawn, get_square('h2'))
    
def print_board(board):
    print_empty_board()
    
    for position in chess.colored_piece_gen(board, chess.KING, chess.BLACK):
        SCREEN.blit(b_king, get_square(chess.bb2str(position)))
    for position in chess.colored_piece_gen(board, chess.QUEEN, chess.BLACK):
        SCREEN.blit(b_queen, get_square(chess.bb2str(position)))
    for position in chess.colored_piece_gen(board, chess.ROOK, chess.BLACK):
        SCREEN.blit(b_rook, get_square(chess.bb2str(position)))
    for position in chess.colored_piece_gen(board, chess.BISHOP, chess.BLACK):
        SCREEN.blit(b_bishop, get_square(chess.bb2str(position)))
    for position in chess.colored_piece_gen(board, chess.KNIGHT, chess.BLACK):
        SCREEN.blit(b_knight, get_square(chess.bb2str(position)))
    for position in chess.colored_piece_gen(board, chess.PAWN, chess.BLACK):
        SCREEN.blit(b_pawn, get_square(chess.bb2str(position)))
        
    for position in chess.colored_piece_gen(board, chess.KING, chess.WHITE):
        SCREEN.blit(w_king, get_square(chess.bb2str(position)))
    for position in chess.colored_piece_gen(board, chess.QUEEN, chess.WHITE):
        SCREEN.blit(w_queen, get_square(chess.bb2str(position)))
    for position in chess.colored_piece_gen(board, chess.ROOK, chess.WHITE):
        SCREEN.blit(w_rook, get_square(chess.bb2str(position)))
    for position in chess.colored_piece_gen(board, chess.BISHOP, chess.WHITE):
        SCREEN.blit(w_bishop, get_square(chess.bb2str(position)))
    for position in chess.colored_piece_gen(board, chess.KNIGHT, chess.WHITE):
        SCREEN.blit(w_knight, get_square(chess.bb2str(position)))
    for position in chess.colored_piece_gen(board, chess.PAWN, chess.WHITE):
        SCREEN.blit(w_pawn, get_square(chess.bb2str(position)))
    
 
game = chess.Game('1r1q2k1/B4p1p/4r1p1/3n2P1/b4P2/7P/8/3R2K1 w - - 1 28')
print_board(game.board)
 
while True:
    CLOCK.tick(15)
     
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
         
    pygame.display.flip()