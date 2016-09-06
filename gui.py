'''
Created on 2 de set de 2016

@author: fvj
'''
import pygame, chess
from random import choice
pygame.init()

SQUARE_SIDE = 50
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT) = (8*SQUARE_SIDE, 8*SQUARE_SIDE)

LIGHT_RED  = (240,180,180)
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
SCREEN_TITLE = 'Chess Game'

pygame.display.set_icon(pygame.image.load('images/chess_icon.ico'))
pygame.display.set_caption(SCREEN_TITLE)

def print_empty_board():
    SCREEN.fill(LIGHT_GRAY)
    paint_dark_squares()
    
def paint_square(square, square_color):
    col = chess.FILES.index(square[0])
    row = 7-chess.RANKS.index(square[1])
    pygame.draw.rect(SCREEN, square_color, (SQUARE_SIDE*col,SQUARE_SIDE*row,SQUARE_SIDE,SQUARE_SIDE), 0)

def paint_dark_squares():
    for position in chess.single_gen(chess.DARK_SQUARES):
        paint_square(chess.bb2str(position), DARK_GRAY)
            
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
    
    if chess.is_check(board, chess.WHITE):
        paint_square(chess.bb2str(chess.get_king(board, chess.WHITE)), LIGHT_RED)
    if chess.is_check(board, chess.BLACK):
        paint_square(chess.bb2str(chess.get_king(board, chess.BLACK)), LIGHT_RED)
    
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
    
def set_title(title):
    pygame.display.set_caption(title)
    pygame.display.flip()
    
def make_AI_move(game, color):
    set_title(SCREEN_TITLE + ' - Calculating move...')
    new_game = chess.make_move(game, chess.get_AI_move(game, 2))
    set_title(SCREEN_TITLE)
    print_board(new_game.board, color)
    return new_game

def try_move(game, attempted_move):
    for move in chess.legal_moves_gen(game, game.to_move):
        if move == attempted_move:
            game = chess.make_move(game, move)
    return game

def play_as(game, color):
    run = True
    ongoing = True
    
    try:
    
        while run:
            CLOCK.tick(CLOCK_TICK)
            print_board(game.board, color)
            
            if chess.game_ended(game):
                set_title(SCREEN_TITLE + ' - ' + chess.get_outcome(game))
                ongoing = False
            
            if ongoing and game.to_move == chess.opposing_color(color):
                game = make_AI_move(game, color)
            
            if chess.game_ended(game):
                set_title(SCREEN_TITLE + ' - ' + chess.get_outcome(game))
                ongoing = False
             
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    leaving_square = coord2str(event.pos, color)
                    
                if event.type == pygame.MOUSEBUTTONUP:
                    arriving_square = coord2str(event.pos, color)
                    
                    if ongoing and game.to_move == color:
                        move = [chess.str2bb(leaving_square), chess.str2bb(arriving_square)]
                        game = try_move(game, move)
                        print_board(game.board, color)
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                    if event.key == 104 and ongoing: # H key
                        game = make_AI_move(game, color)
                    if event.key == 117: # U key
                        game = chess.unmake_move(game)
                        game = chess.unmake_move(game)
                        set_title(SCREEN_TITLE)
                        print_board(game.board, color)
                        ongoing = True
    except:
        bug_file = open('bug_report.txt', 'a')
        bug_file.write('\n'.join(game.position_history))
        bug_file.write('\n\n')
        bug_file.close()

def play_as_white(game=chess.Game()):
    return play_as(game, chess.WHITE)

def play_as_black(game=chess.Game()):
    return play_as(game, chess.BLACK)

def play_random_color(game=chess.Game()):
    color = choice([chess.WHITE, chess.BLACK])
    play_as(game, color)

# chess.verbose = True
play_random_color()