'''
Created on 2 de set de 2016

@author: fvj
'''
import sys, pygame, chess
from random import choice
pygame.init()

SQUARE_SIDE = 50
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT) = (8*SQUARE_SIDE, 8*SQUARE_SIDE)

LIGHT_GRAY = (240,240,240)
DARK_GRAY  = (200,200,200)

BLACK_KING   = pygame.transform.scale(pygame.image.load('images/black_king.png'),   (SQUARE_SIDE,SQUARE_SIDE) )
BLACK_QUEEN  = pygame.transform.scale(pygame.image.load('images/black_queen.png'),  (SQUARE_SIDE,SQUARE_SIDE) )
BLACK_ROOK   = pygame.transform.scale(pygame.image.load('images/black_rook.png'),   (SQUARE_SIDE,SQUARE_SIDE) )
BLACK_BISHOP = pygame.transform.scale(pygame.image.load('images/black_bishop.png'), (SQUARE_SIDE,SQUARE_SIDE) )
BLACK_KNIGHT = pygame.transform.scale(pygame.image.load('images/black_knight.png'), (SQUARE_SIDE,SQUARE_SIDE) )
BLACK_PAWN   = pygame.transform.scale(pygame.image.load('images/black_pawn.png'),   (SQUARE_SIDE,SQUARE_SIDE) )

WHITE_KING   = pygame.transform.scale(pygame.image.load('images/white_king.png'),   (SQUARE_SIDE,SQUARE_SIDE) )
WHITE_QUEEN  = pygame.transform.scale(pygame.image.load('images/white_queen.png'),  (SQUARE_SIDE,SQUARE_SIDE) )
WHITE_ROOK   = pygame.transform.scale(pygame.image.load('images/white_rook.png'),   (SQUARE_SIDE,SQUARE_SIDE) )
WHITE_BISHOP = pygame.transform.scale(pygame.image.load('images/white_bishop.png'), (SQUARE_SIDE,SQUARE_SIDE) )
WHITE_KNIGHT = pygame.transform.scale(pygame.image.load('images/white_knight.png'), (SQUARE_SIDE,SQUARE_SIDE) )
WHITE_PAWN   = pygame.transform.scale(pygame.image.load('images/white_pawn.png'),   (SQUARE_SIDE,SQUARE_SIDE) )

CLOCK = pygame.time.Clock()
CLOCK_TICK = 15

SCREEN = pygame.display.set_mode(SCREEN_SIZE)

pygame.display.set_icon(pygame.image.load('images/chess_icon.ico'))
pygame.display.set_caption('Chess Game')

def print_empty_board():
    SCREEN.fill(LIGHT_GRAY)
    print_dark_squares()

def print_dark_squares():
    for position in chess.single_gen(chess.DARK_SQUARES):
        square = chess.bb2str(position)
        col = chess.FILES.index(square[0])
        row = 7-chess.RANKS.index(square[1])
        pygame.draw.rect(SCREEN, DARK_GRAY, (SQUARE_SIDE*col,SQUARE_SIDE*row,SQUARE_SIDE,SQUARE_SIDE), 0)
            
def get_square_rect(square):
    col = chess.FILES.index(square[0])
    row = 7-chess.RANKS.index(square[1])
    return pygame.Rect((col*SQUARE_SIDE, row*SQUARE_SIDE), (SQUARE_SIDE,SQUARE_SIDE))

def coord2str(position, color=chess.WHITE):
    if color == chess.WHITE:
        file_index = int(position[0]/SQUARE_SIDE)
        rank_index = 7 - int(position[1]/SQUARE_SIDE)
        return chess.FILES[file_index] + chess.RANKS[rank_index]
    if color == chess.BLACK:
        file_index = 7 - int(position[0]/SQUARE_SIDE)
        rank_index = int(position[1]/SQUARE_SIDE)
        return chess.FILES[file_index] + chess.RANKS[rank_index]
    
def print_board(board, color=chess.WHITE):
    if color == chess.BLACK:
        board = chess.rotate_board(board)
    
    print_empty_board()
    
    for position in chess.colored_piece_gen(board, chess.KING, chess.BLACK):
        SCREEN.blit(BLACK_KING, get_square_rect(chess.bb2str(position)))
    for position in chess.colored_piece_gen(board, chess.QUEEN, chess.BLACK):
        SCREEN.blit(BLACK_QUEEN, get_square_rect(chess.bb2str(position)))
    for position in chess.colored_piece_gen(board, chess.ROOK, chess.BLACK):
        SCREEN.blit(BLACK_ROOK, get_square_rect(chess.bb2str(position)))
    for position in chess.colored_piece_gen(board, chess.BISHOP, chess.BLACK):
        SCREEN.blit(BLACK_BISHOP, get_square_rect(chess.bb2str(position)))
    for position in chess.colored_piece_gen(board, chess.KNIGHT, chess.BLACK):
        SCREEN.blit(BLACK_KNIGHT, get_square_rect(chess.bb2str(position)))
    for position in chess.colored_piece_gen(board, chess.PAWN, chess.BLACK):
        SCREEN.blit(BLACK_PAWN, get_square_rect(chess.bb2str(position)))
        
    for position in chess.colored_piece_gen(board, chess.KING, chess.WHITE):
        SCREEN.blit(WHITE_KING, get_square_rect(chess.bb2str(position)))
    for position in chess.colored_piece_gen(board, chess.QUEEN, chess.WHITE):
        SCREEN.blit(WHITE_QUEEN, get_square_rect(chess.bb2str(position)))
    for position in chess.colored_piece_gen(board, chess.ROOK, chess.WHITE):
        SCREEN.blit(WHITE_ROOK, get_square_rect(chess.bb2str(position)))
    for position in chess.colored_piece_gen(board, chess.BISHOP, chess.WHITE):
        SCREEN.blit(WHITE_BISHOP, get_square_rect(chess.bb2str(position)))
    for position in chess.colored_piece_gen(board, chess.KNIGHT, chess.WHITE):
        SCREEN.blit(WHITE_KNIGHT, get_square_rect(chess.bb2str(position)))
    for position in chess.colored_piece_gen(board, chess.PAWN, chess.WHITE):
        SCREEN.blit(WHITE_PAWN, get_square_rect(chess.bb2str(position)))
        
    pygame.display.flip()

def play_as(game, color):
    ongoing = True
    
    while True:
        CLOCK.tick(CLOCK_TICK)
        print_board(game.board, color)
        
        if chess.game_ended(game):
            pygame.display.set_caption('Chess Game - ' + chess.get_outcome(game))
            pygame.display.flip()
            ongoing = False
        
        if ongoing and game.to_move == chess.opposing_color(color):
            pygame.display.set_caption('Chess Game - Calculating move...')
            pygame.display.flip()
            game = chess.make_move(game, chess.get_AI_move(game, 2))
            pygame.display.set_caption('Chess Game')
            print_board(game.board, color)
        
        if chess.game_ended(game):
            pygame.display.set_caption('Chess Game - ' + chess.get_outcome(game))
            pygame.display.flip()
            ongoing = False
         
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                leaving_square = coord2str(event.pos, color)
                
            if event.type == pygame.MOUSEBUTTONUP:
                arriving_square = coord2str(event.pos, color)
                
                if ongoing:
                    for move in chess.legal_moves_gen(game, color):
                        if move == [chess.str2bb(leaving_square), chess.str2bb(arriving_square)]:
                            game = chess.make_move(game, move)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == 104 and ongoing: # H key
                    game = chess.make_move(game, chess.get_AI_move(game, 2))
                if event.key == 117: # U key
                    game = chess.unmake_move(game)
                    game = chess.unmake_move(game)
                    pygame.display.set_caption('Chess Game')
                    print_board(game.board, color)
                    ongoing = True

def play_as_white(game=chess.Game()):
    return play_as(game, chess.WHITE)

def play_as_black(game=chess.Game()):
    return play_as(game, chess.BLACK)

def play_random_color(game=chess.Game()):
    color = choice([chess.WHITE, chess.BLACK])
    play_as(game, color)

# chess.verbose = True
play_random_color()