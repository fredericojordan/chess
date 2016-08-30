'''
Created on 12 de ago de 2016

@author: fvj

BITMASK = 0bC**KMPPP

where:
C - color
* - not used
K - castling flag
P - piece code

This program uses "Little-Endian Rank-File Mapping":
bit_boards = 0b(h8)(g8)...(b1)(a1)

board = [ a1, b1, ..., g8, h8 ]

move = [ leaving_position, arriving_position ]

'''
from copy import deepcopy
from random import choice
from time import sleep
import sys

COLOR_MASK = 1 << 4
WHITE = 0 << 4
BLACK = 1 << 4

PIECE_MASK = 0b111
EMPTY  = 0
PAWN   = 1
KNIGHT = 2
BISHOP = 3
ROOK   = 4
QUEEN  = 5
KING   = 6

PIECE_TYPES = [ PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING ]
PIECE_VALUES = { EMPTY:0, PAWN:100, KNIGHT:300, BISHOP:300, ROOK:500, QUEEN:900, KING:42000 }

FILES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
RANKS = ['1', '2', '3', '4', '5', '6', '7', '8']

CASTLE_KINGSIDE_WHITE  = 0b1 << 0
CASTLE_QUEENSIDE_WHITE = 0b1 << 1
CASTLE_KINGSIDE_BLACK  = 0b1 << 2
CASTLE_QUEENSIDE_BLACK = 0b1 << 3

FULL_CASTLING_RIGHTS = CASTLE_KINGSIDE_WHITE|CASTLE_QUEENSIDE_WHITE|CASTLE_KINGSIDE_BLACK|CASTLE_QUEENSIDE_BLACK

ALL_SQUARES    = 0xFFFFFFFFFFFFFFFF
FILE_A         = 0x0101010101010101
FILE_B         = 0x0202020202020202
FILE_C         = 0x0404040404040404
FILE_D         = 0x0808080808080808
FILE_E         = 0x1010101010101010
FILE_F         = 0x2020202020202020
FILE_G         = 0x4040404040404040
FILE_H         = 0x8080808080808080
RANK_1         = 0x00000000000000FF
RANK_2         = 0x000000000000FF00
RANK_3         = 0x0000000000FF0000
RANK_4         = 0x00000000FF000000
RANK_5         = 0x000000FF00000000
RANK_6         = 0x0000FF0000000000
RANK_7         = 0x00FF000000000000
RANK_8         = 0xFF00000000000000
DIAG_A1H8      = 0x8040201008040201
ANTI_DIAG_H1A8 = 0x0102040810204080
LIGHT_SQUARES  = 0x55AA55AA55AA55AA
DARK_SQUARES   = 0xAA55AA55AA55AA55

INITIAL_BOARD = [ WHITE|ROOK, WHITE|KNIGHT, WHITE|BISHOP, WHITE|QUEEN, WHITE|KING, WHITE|BISHOP, WHITE|KNIGHT, WHITE|ROOK,
                  WHITE|PAWN, WHITE|PAWN,   WHITE|PAWN,   WHITE|PAWN,  WHITE|PAWN, WHITE|PAWN,   WHITE|PAWN,   WHITE|PAWN, 
                  EMPTY,      EMPTY,        EMPTY,        EMPTY,       EMPTY,      EMPTY,        EMPTY,        EMPTY,
                  EMPTY,      EMPTY,        EMPTY,        EMPTY,       EMPTY,      EMPTY,        EMPTY,        EMPTY,
                  EMPTY,      EMPTY,        EMPTY,        EMPTY,       EMPTY,      EMPTY,        EMPTY,        EMPTY,
                  EMPTY,      EMPTY,        EMPTY,        EMPTY,       EMPTY,      EMPTY,        EMPTY,        EMPTY,
                  BLACK|PAWN, BLACK|PAWN,   BLACK|PAWN,   BLACK|PAWN,  BLACK|PAWN, BLACK|PAWN,   BLACK|PAWN,   BLACK|PAWN,
                  BLACK|ROOK, BLACK|KNIGHT, BLACK|BISHOP, BLACK|QUEEN, BLACK|KING, BLACK|BISHOP, BLACK|KNIGHT, BLACK|ROOK ]

EMPTY_BOARD = [ EMPTY for _ in range(64) ]

INITIAL_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
STROKES_YOLO = '1k6/2b1p3/Qp4N1/4r2P/2B2q2/1R6/2Pn2K1/8 w - - 0 1'

PIECE_CODES = { WHITE|KING:  'K',
                WHITE|QUEEN: 'Q',
                WHITE|ROOK:  'R',
                WHITE|BISHOP:'B',
                WHITE|KNIGHT:'N',
                WHITE|PAWN:  'P',
                BLACK|KING:  'k',
                BLACK|QUEEN: 'q',
                BLACK|ROOK:  'r',
                BLACK|BISHOP:'b',
                BLACK|KNIGHT:'n',
                BLACK|PAWN:  'p',
                EMPTY:       '.' }
PIECE_CODES.update({v: k for k, v in PIECE_CODES.items()})


# ========== CHESS GAME ==========

class ChessGame:
    def __init__(self, FEN=''):
        self.board = INITIAL_BOARD
        self.to_move = WHITE
        self.ep_square = 0
        self.castling_rights = FULL_CASTLING_RIGHTS
        self.halfmove_clock = 0
        self.fullmove_number = 1
        
        self.position_history = []
        if FEN != '':
            self.load_FEN(FEN)
            self.position_history.append(FEN)
        else:
            self.position_history.append(INITIAL_FEN)
            
        self.move_history = []
    
    def get_move_list(self):
        return ' '.join(self.move_history)
    
    def to_FEN(self):
        FEN_str = ''
        
        for i in range(len(RANKS)):
            first = len(self.board) - 8*(i+1)
            empty_sqrs = 0
            for fille in range(len(FILES)):
                piece = self.board[first+fille]
                if piece&PIECE_MASK == EMPTY:
                    empty_sqrs += 1
                else:
                    if empty_sqrs > 0:
                        FEN_str += '{}'.format(empty_sqrs)
                    FEN_str += '{}'.format(piece2str(piece))
                    empty_sqrs = 0
            if empty_sqrs > 0:
                FEN_str += '{}'.format(empty_sqrs)
            FEN_str += '/'
        FEN_str = FEN_str[:-1] + ' '
        
        if self.to_move == WHITE:
            FEN_str += 'w '
        if self.to_move == BLACK:
            FEN_str += 'b '
            
        if self.castling_rights & CASTLE_KINGSIDE_WHITE:
            FEN_str += 'K'
        if self.castling_rights & CASTLE_QUEENSIDE_WHITE:
            FEN_str += 'Q'
        if self.castling_rights & CASTLE_KINGSIDE_BLACK:
            FEN_str += 'k'
        if self.castling_rights & CASTLE_QUEENSIDE_BLACK:
            FEN_str += 'q'
        if self.castling_rights == 0:
            FEN_str += '-'
        FEN_str += ' '
            
        if self.ep_square == 0:
            FEN_str += '-'
        else:
            FEN_str += bb2str(self.ep_square)
        
        FEN_str += ' {}'.format(self.halfmove_clock)
        FEN_str += ' {}'.format(self.fullmove_number)
        return FEN_str
    
    def load_FEN(self, FEN_str):
        FEN_list = FEN_str.split(' ')
        
        board_str = FEN_list[0]
        rank_list = board_str.split('/')
        rank_list.reverse()
        self.board = []
        
        for rank in rank_list:
            rank_pieces = []
            for p in rank:
                if p.isdigit():
                    for _ in range(int(p)):
                        rank_pieces.append(EMPTY)
                else:
                    rank_pieces.append(str2piece(p))
            self.board.extend(rank_pieces)
        
        to_move_str = FEN_list[1].lower()
        if to_move_str == 'w':
            self.to_move = WHITE
        if to_move_str == 'b':
            self.to_move = BLACK
        
        castling_rights_str = FEN_list[2]
        self.castling_rights = 0
        if castling_rights_str.find('K') >= 0:
            self.castling_rights |= CASTLE_KINGSIDE_WHITE
        if castling_rights_str.find('Q') >= 0:
            self.castling_rights |= CASTLE_QUEENSIDE_WHITE
        if castling_rights_str.find('k') >= 0:
            self.castling_rights |= CASTLE_KINGSIDE_BLACK
        if castling_rights_str.find('q') >= 0:
            self.castling_rights |= CASTLE_QUEENSIDE_BLACK 
        
        ep_str = FEN_list[3]
        if ep_str == '-':
            self.ep_square = 0
        else:
            self.ep_square = str2bb(ep_str)
        
        self.halfmove_clock = int(FEN_list[4])
        self.fullmove_number = int(FEN_list[5])

# ================================


def get_piece(board, bitboard):
    return board[bb2index(bitboard)]
        
def bb2index(bitboard):
    for i in range(64):
        if bitboard & (0b1 << i):
            return i

def str2index(position_str):
    fille = FILES.index(position_str[0].lower())
    rank = RANKS.index(position_str[1])
    return 8*rank + fille

def bb2str(bitboard):
    for i in range(64):
        if bitboard & (0b1 << i):
            fille = i%8
            rank = int(i/8)
            return '{}{}'.format(FILES[fille], RANKS[rank])

def str2bb(position_str):
    return 0b1 << str2index(position_str)

def move2str(move):
    return '{}{}'.format(bb2str(move[0]), bb2str(move[1]))

def single_gen(bitboard):
    for i in range(64):
        bit = 0b1 << i
        if bitboard & bit:
            yield bit

def piece_gen(board, piece_code):
    for i in range(64):
        if board[i]&PIECE_MASK == piece_code:
            yield 0b1 << i

def colored_piece_gen(board, piece_code, color):
    for i in range(64):
        if board[i]&(PIECE_MASK|COLOR_MASK) == piece_code|color:
            yield 0b1 << i
            
def opposing_color(color):
    if color == WHITE:
        return BLACK
    if color == BLACK:
        return WHITE

def piece2str(piece):
    return PIECE_CODES[ piece & (PIECE_MASK|COLOR_MASK) ]

def str2piece(string):
    return PIECE_CODES[string]
    
def print_board(board):
    print('')
    for i in range(len(RANKS)):
        rank_str = str(8-i) + ' '
        first = len(board) - 8*(i+1)
        for fille in range(len(FILES)):
            rank_str += '{} '.format(piece2str(board[first+fille]))
        print(rank_str)
    print('  a b c d e f g h')

def print_rotated_board(board):
    r_board = rotate_board(board)
    print('')
    for i in range(len(RANKS)):
        rank_str = str(i+1) + ' '
        first = len(r_board) - 8*(i+1)
        for fille in range(len(FILES)):
            rank_str += '{} '.format(piece2str(r_board[first+fille]))
        print(rank_str)
    print('  h g f e d c b a')
    
def print_bitboard(bitboard):
    print('')
    for rank in range(len(RANKS)):
        rank_str = str(8-rank) + ' '
        for fille in range(len(FILES)):
            if (bitboard >> (fille + (7-rank)*8)) & 0b1:
                rank_str += '# '
            else:
                rank_str += '. '
        print(rank_str)
    print('  a b c d e f g h')
    
def lsb(bitboard):
    for i in range(64):
        bit = (0b1 << i) 
        if bit & bitboard:
            return bit

def msb(bitboard):
    for i in range(64):
        bit = (0b1 << (63-i)) 
        if bit & bitboard:
            return bit

def get_colored_pieces(board, color):
    return list2int([ (i&COLOR_MASK == color and i&PIECE_MASK != EMPTY) for i in board ])

def empty_squares(board):
    return list2int([ i&PIECE_MASK == EMPTY for i in board ])

def occupied_squares(board):
    return nnot(empty_squares(board))

def list2int(lst):
    rev_list = lst[:]
    rev_list.reverse()
    return int('0b' + ''.join(['1' if i else '0' for i in rev_list]), 2)

def nnot(bitboard):
    return ~bitboard & ALL_SQUARES

def rotate_board(board):
    rotated_board = deepcopy(board)
    rotated_board.reverse()
    return rotated_board

def east_one(bitboard):
    return (bitboard << 1) & nnot(FILE_A)

def west_one(bitboard):
    return (bitboard >> 1) & nnot(FILE_H)

def north_one(bitboard):
    return (bitboard << 8) & nnot(RANK_1)

def south_one(bitboard):
    return (bitboard >> 8) & nnot(RANK_8)

def NE_one(bitboard):
    return north_one(east_one(bitboard))

def NW_one(bitboard):
    return north_one(west_one(bitboard))

def SE_one(bitboard):
    return south_one(east_one(bitboard))

def SW_one(bitboard):
    return south_one(west_one(bitboard))

def move_piece(board, move):
    new_board = deepcopy(board)
    new_board[bb2index(move[1])] = new_board[bb2index(move[0])] 
    new_board[bb2index(move[0])] = EMPTY
    return new_board

def make_move(game, move):
    new_game = deepcopy(game)
    leaving_position = move[0]
    arriving_position = move[1]
    
    # update_clocks
    new_game.halfmove_clock += 1
    if new_game.to_move == BLACK:
        new_game.fullmove_number += 1
    
    # reset clock if capture
    if get_piece(new_game.board, arriving_position)&PIECE_MASK != EMPTY:
        new_game.halfmove_clock = 0
    
    # for pawns: reset clock, removed captured ep, set new ep, promote
    if get_piece(new_game.board, leaving_position)&PIECE_MASK == PAWN:
        new_game.halfmove_clock = 0
        
        if arriving_position == game.ep_square:
            new_game.board = remove_captured_ep(new_game)
    
        if is_double_push(leaving_position, arriving_position):
            new_game.ep_square = new_ep_square(leaving_position)
            
        if arriving_position&(RANK_1|RANK_8):
            new_game.board[bb2index(leaving_position)] = new_game.to_move|QUEEN
    
    # reset ep square if not updated
    if new_game.ep_square == game.ep_square:
        new_game.ep_square = 0
        
    # update castling rights for rook moves
    if leaving_position == str2bb('a1'):
        new_game.castling_rights = remove_castling_rights(new_game, CASTLE_QUEENSIDE_WHITE)
    if leaving_position == str2bb('h1'):
        new_game.castling_rights = remove_castling_rights(new_game, CASTLE_KINGSIDE_WHITE)
    if leaving_position == str2bb('a8'):
        new_game.castling_rights = remove_castling_rights(new_game, CASTLE_QUEENSIDE_BLACK)
    if leaving_position == str2bb('h8'):
        new_game.castling_rights = remove_castling_rights(new_game, CASTLE_KINGSIDE_BLACK)
    
    # castling
    if get_piece(new_game.board, leaving_position)&(PIECE_MASK|COLOR_MASK) == WHITE|KING:
        new_game.castling_rights = remove_castling_rights(new_game, CASTLE_KINGSIDE_WHITE|CASTLE_QUEENSIDE_WHITE)
        if leaving_position == str2bb('e1'):
            if arriving_position == str2bb('g1'):
                new_game.board = move_piece(new_game.board, [str2bb('h1'), str2bb('f1')])
            if arriving_position == str2bb('c1'):
                new_game.board = move_piece(new_game.board, [str2bb('a1'), str2bb('d1')])
        
    if get_piece(new_game.board, leaving_position)&(PIECE_MASK|COLOR_MASK) == BLACK|KING:
        new_game.castling_rights = remove_castling_rights(new_game, CASTLE_KINGSIDE_BLACK|CASTLE_QUEENSIDE_BLACK)
        if leaving_position == str2bb('e8'):
            if arriving_position == str2bb('g8'):
                new_game.board = move_piece(new_game.board, [str2bb('h8'), str2bb('f8')])
            if arriving_position == str2bb('c8'):
                new_game.board = move_piece(new_game.board, [str2bb('a8'), str2bb('d8')])
    
    # update positions and next to move
    new_game.board = move_piece(new_game.board, (leaving_position, arriving_position))
    new_game.to_move = opposing_color(new_game.to_move)
    
    # update history
    new_game.move_history.append(bb2str(move[0]) + bb2str(move[1]))
    new_game.position_history.append(new_game.to_FEN())
    return new_game

def get_rank(rank_num):
    rank_num = int(rank_num)
    if rank_num == 1:
        return RANK_1
    if rank_num == 2:
        return RANK_2
    if rank_num == 3:
        return RANK_3
    if rank_num == 4:
        return RANK_4
    if rank_num == 5:
        return RANK_5
    if rank_num == 6:
        return RANK_6
    if rank_num == 7:
        return RANK_7
    if rank_num == 8:
        return RANK_8
    
def get_file(fille):
    fille = fille.lower()
    if fille == 'a':
        return FILE_A
    if fille == 'b':
        return FILE_B
    if fille == 'c':
        return FILE_C
    if fille == 'd':
        return FILE_D
    if fille == 'e':
        return FILE_E
    if fille == 'f':
        return FILE_F
    if fille == 'g':
        return FILE_G
    if fille == 'h':
        return FILE_H
    
def get_filter(filter_str):
    if filter_str in FILES:
        return get_file(filter_str)
    if filter_str in RANKS:
        return get_rank(filter_str)

# ========== PAWN ==========

def get_pawns(board, color):
    return list2int([ i&(COLOR_MASK|PIECE_MASK) == color|PAWN for i in board ])

def pawn_moves(moving_piece, game, color):
    return pawn_pushes(moving_piece, game.board, color) | pawn_captures(moving_piece, game, color)

def pawn_captures(moving_piece, game, color):
    return pawn_simple_captures(moving_piece, game, color) | pawn_ep_captures(moving_piece, game, color)

def pawn_pushes(moving_piece, board, color):
    return pawn_simple_pushes(moving_piece, board, color) | pawn_double_pushes(moving_piece, board, color)

def pawn_simple_captures(attacking_piece, game, color):
    return pawn_attacks(attacking_piece, game.board, color) & get_colored_pieces(game.board, opposing_color(color))

def pawn_ep_captures(attacking_piece, game, color):
    if color == WHITE:
        ep_squares = game.ep_square & RANK_6
    if color == BLACK:
        ep_squares = game.ep_square & RANK_3
    return pawn_attacks(attacking_piece, game.board, color) & ep_squares

def pawn_attacks(attacking_piece, board, color):
    return pawn_east_attacks(attacking_piece, board, color) | pawn_west_attacks(attacking_piece, board, color)

def pawn_simple_pushes(moving_piece, board, color):
    if color == WHITE:
        return north_one(moving_piece) & empty_squares(board)
    if color == BLACK:
        return south_one(moving_piece) & empty_squares(board)
    
def pawn_double_pushes(moving_piece, board, color):
    if color == WHITE:
        return north_one(pawn_simple_pushes(moving_piece, board, color)) & (empty_squares(board) & RANK_4)
    if color == BLACK:
        return south_one(pawn_simple_pushes(moving_piece, board, color)) & (empty_squares(board) & RANK_5)

def pawn_east_attacks(attacking_piece, board, color):
    if color == WHITE:
        return NE_one(attacking_piece & get_colored_pieces(board, color))
    if color == BLACK:
        return SE_one(attacking_piece & get_colored_pieces(board, color))

def pawn_west_attacks(attacking_piece, board, color):
    if color == WHITE:
        return NW_one(attacking_piece & get_colored_pieces(board, color))
    if color == BLACK:
        return SW_one(attacking_piece & get_colored_pieces(board, color))

def pawn_double_attacks(attacking_piece, board, color):
    return pawn_east_attacks(attacking_piece, board, color) & pawn_west_attacks(attacking_piece, board, color)

def is_double_push(leaving_square, target_square):
    return (leaving_square&RANK_2 and target_square&RANK_4) or \
           (leaving_square&RANK_7 and target_square&RANK_5)
    
def new_ep_square(leaving_square):
    if leaving_square&RANK_2:
        return north_one(leaving_square)
    if leaving_square&RANK_7:
        return south_one(leaving_square)

def remove_captured_ep(game):
    new_board = deepcopy(game.board)
    if game.ep_square & RANK_3:
        new_board[bb2index(south_one(game.ep_square))] = EMPTY
    if game.ep_square & RANK_6:
        new_board[bb2index(north_one(game.ep_square))] = EMPTY
    return new_board

# ========== KNIGHT ==========

def get_knights(board, color):
    return list2int([ i&(COLOR_MASK|PIECE_MASK) == color|KNIGHT for i in board ])

def knight_moves(moving_piece, board, color):
    return knight_attacks(moving_piece) & nnot(get_colored_pieces(board, color))

def knight_attacks(moving_piece):
    return knight_NNE(moving_piece) | \
           knight_ENE(moving_piece) | \
           knight_NNW(moving_piece) | \
           knight_WNW(moving_piece) | \
           knight_SSE(moving_piece) | \
           knight_ESE(moving_piece) | \
           knight_SSW(moving_piece) | \
           knight_WSW(moving_piece)

def knight_WNW(moving_piece):
    return moving_piece << 6 & nnot(FILE_G | FILE_H)

def knight_ENE(moving_piece):
    return moving_piece << 10 & nnot(FILE_A | FILE_B)

def knight_NNW(moving_piece):
    return moving_piece << 15 & nnot(FILE_H)

def knight_NNE(moving_piece):
    return moving_piece << 17 & nnot(FILE_A)

def knight_ESE(moving_piece):
    return moving_piece >> 6 & nnot(FILE_A | FILE_B)

def knight_WSW(moving_piece):
    return moving_piece >> 10 & nnot(FILE_G | FILE_H)

def knight_SSE(moving_piece):
    return moving_piece >> 15 & nnot(FILE_A)

def knight_SSW(moving_piece):
    return moving_piece >> 17 & nnot(FILE_H)

def knight_fill(moving_piece, n):
    fill = moving_piece
    for _ in range(n):
        fill |= knight_attacks(fill)
    return fill

def knight_distance(pos1, pos2):
    init_bitboard = str2bb(pos1)
    end_bitboard = str2bb(pos2)
    fill = init_bitboard
    dist = 0
    while fill & end_bitboard == 0:
        dist += 1
        fill = knight_fill(init_bitboard, dist)
    return dist
    
# ========== KING ==========

def get_king(board, color):
    return list2int([ i&(COLOR_MASK|PIECE_MASK) == color|KING for i in board ])

def king_moves(moving_piece, board, color):
    return king_attacks(moving_piece) & nnot(get_colored_pieces(board, color))

def king_attacks(moving_piece):
    king_atks = moving_piece | east_one(moving_piece) | west_one(moving_piece)
    king_atks |= north_one(king_atks) | south_one(king_atks)
    return king_atks & nnot(moving_piece)

def can_castle_kingside(game, color):
    if color == WHITE:
        return (game.castling_rights & CASTLE_KINGSIDE_WHITE) and \
                game.board[str2index('f1')] == EMPTY and \
                game.board[str2index('g1')] == EMPTY and \
                (not is_attacked(str2bb('e1'), game.board, opposing_color(color))) and \
                (not is_attacked(str2bb('f1'), game.board, opposing_color(color))) and \
                (not is_attacked(str2bb('g1'), game.board, opposing_color(color)))
    if color == BLACK:
        return (game.castling_rights & CASTLE_KINGSIDE_BLACK) and \
                game.board[str2index('f8')] == EMPTY and \
                game.board[str2index('g8')] == EMPTY and \
                (not is_attacked(str2bb('e8'), game.board, opposing_color(color))) and \
                (not is_attacked(str2bb('f8'), game.board, opposing_color(color))) and \
                (not is_attacked(str2bb('g8'), game.board, opposing_color(color)))

def can_castle_queenside(game, color):
    if color == WHITE:
        return (game.castling_rights & CASTLE_QUEENSIDE_WHITE) and \
                game.board[str2index('b1')] == EMPTY and \
                game.board[str2index('c1')] == EMPTY and \
                game.board[str2index('d1')] == EMPTY and \
                (not is_attacked(str2bb('c1'), game.board, opposing_color(color))) and \
                (not is_attacked(str2bb('d1'), game.board, opposing_color(color))) and \
                (not is_attacked(str2bb('e1'), game.board, opposing_color(color)))
    if color == BLACK:
        return (game.castling_rights & CASTLE_QUEENSIDE_BLACK) and \
                game.board[str2index('b8')] == EMPTY and \
                game.board[str2index('c8')] == EMPTY and \
                game.board[str2index('d8')] == EMPTY and \
                (not is_attacked(str2bb('c8'), game.board, opposing_color(color))) and \
                (not is_attacked(str2bb('d8'), game.board, opposing_color(color))) and \
                (not is_attacked(str2bb('e8'), game.board, opposing_color(color)))

def castle_kingside_move(game):
    if game.to_move == WHITE:
        return (str2bb('e1'), str2bb('g1'))
    if game.to_move == BLACK:
        return (str2bb('e8'), str2bb('g8'))

def castle_queenside_move(game):
    if game.to_move == WHITE:
        return (str2bb('e1'), str2bb('c1'))
    if game.to_move == BLACK:
        return (str2bb('e8'), str2bb('c8'))

def remove_castling_rights(game, removed_rights):
    return game.castling_rights & ~removed_rights

# ========== BISHOP ==========

def get_bishops(board, color):
    return list2int([ i&(COLOR_MASK|PIECE_MASK) == color|BISHOP for i in board ])

def bishop_rays(moving_piece):
    return diagonal_rays(moving_piece) | anti_diagonal_rays(moving_piece)
           
def diagonal_rays(moving_piece):
    return NE_ray(moving_piece) | SW_ray(moving_piece)

def anti_diagonal_rays(moving_piece):
    return NW_ray(moving_piece) | SE_ray(moving_piece)

def NE_ray(moving_piece):
    ray_atks = NE_one(moving_piece)
    for _ in range(6):
        ray_atks |= NE_one(ray_atks)
    return ray_atks & ALL_SQUARES

def SE_ray(moving_piece):
    ray_atks = SE_one(moving_piece)
    for _ in range(6):
        ray_atks |= SE_one(ray_atks)
    return ray_atks & ALL_SQUARES

def NW_ray(moving_piece):
    ray_atks = NW_one(moving_piece)
    for _ in range(6):
        ray_atks |= NW_one(ray_atks)
    return ray_atks & ALL_SQUARES

def SW_ray(moving_piece):
    ray_atks = SW_one(moving_piece)
    for _ in range(6):
        ray_atks |= SW_one(ray_atks)
    return ray_atks & ALL_SQUARES

def NE_attacks(single_piece, board, color):
    blocker = lsb(NE_ray(single_piece) & occupied_squares(board))
    if blocker:
        return NE_ray(single_piece) ^ NE_ray(blocker)
    else:
        return NE_ray(single_piece)
    
def NW_attacks(single_piece, board, color):
    blocker = lsb(NW_ray(single_piece) & occupied_squares(board))
    if blocker:
        return NW_ray(single_piece) ^ NW_ray(blocker)
    else:
        return NW_ray(single_piece)

def SE_attacks(single_piece, board, color):
    blocker = msb(SE_ray(single_piece) & occupied_squares(board))
    if blocker:
        return SE_ray(single_piece) ^ SE_ray(blocker)
    else:
        return SE_ray(single_piece)

def SW_attacks(single_piece, board, color):
    blocker = msb(SW_ray(single_piece) & occupied_squares(board))
    if blocker:
        return SW_ray(single_piece) ^ SW_ray(blocker)
    else:
        return SW_ray(single_piece)

def diagonal_attacks(single_piece, board, color):
    return NE_attacks(single_piece, board, color) | SW_attacks(single_piece, board, color)

def anti_diagonal_attacks(single_piece, board, color):
    return NW_attacks(single_piece, board, color) | SE_attacks(single_piece, board, color)

def bishop_attacks(moving_piece, board, color):
    atks = 0
    for piece in single_gen(moving_piece):
        atks |= diagonal_attacks(piece, board, color) | anti_diagonal_attacks(piece, board, color)
    return atks

def bishop_moves(moving_piece, board, color):
    return bishop_attacks(moving_piece, board, color) & nnot(get_colored_pieces(board, color))

# ========== ROOK ==========

def get_rooks(board, color):
    return list2int([ i&(COLOR_MASK|PIECE_MASK) == color|ROOK for i in board ])

def rook_rays(moving_piece):
    return rank_rays(moving_piece) | file_rays(moving_piece)

def rank_rays(moving_piece):
    return east_ray(moving_piece) | west_ray(moving_piece)

def file_rays(moving_piece):
    return north_ray(moving_piece) | south_ray(moving_piece)

def east_ray(moving_piece):
    ray_atks = east_one(moving_piece)
    for _ in range(6):
        ray_atks |= east_one(ray_atks)
    return ray_atks & ALL_SQUARES

def west_ray(moving_piece):
    ray_atks = west_one(moving_piece)
    for _ in range(6):
        ray_atks |= west_one(ray_atks)
    return ray_atks & ALL_SQUARES

def north_ray(moving_piece):
    ray_atks = north_one(moving_piece)
    for _ in range(6):
        ray_atks |= north_one(ray_atks)
    return ray_atks & ALL_SQUARES

def south_ray(moving_piece):
    ray_atks = south_one(moving_piece)
    for _ in range(6):
        ray_atks |= south_one(ray_atks)
    return ray_atks & ALL_SQUARES

def east_attacks(single_piece, board, color):
    blocker = lsb(east_ray(single_piece) & occupied_squares(board))
    if blocker:
        return east_ray(single_piece) ^ east_ray(blocker)
    else:
        return east_ray(single_piece)
    
def west_attacks(single_piece, board, color):
    blocker = msb(west_ray(single_piece) & occupied_squares(board))
    if blocker:
        return west_ray(single_piece) ^ west_ray(blocker)
    else:
        return west_ray(single_piece)
    
def rank_attacks(single_piece, board, color):
    return east_attacks(single_piece, board, color) | west_attacks(single_piece, board, color)

def north_attacks(single_piece, board, color):
    blocker = lsb(north_ray(single_piece) & occupied_squares(board))
    if blocker:
        return north_ray(single_piece) ^ north_ray(blocker)
    else:
        return north_ray(single_piece)
    
def south_attacks(single_piece, board, color):
    blocker = msb(south_ray(single_piece) & occupied_squares(board))
    if blocker:
        return south_ray(single_piece) ^ south_ray(blocker)
    else:
        return south_ray(single_piece)
    
def file_attacks(single_piece, board, color):
    return north_attacks(single_piece, board, color) | south_attacks(single_piece, board, color)

def rook_attacks(moving_piece, board, color):
    atks = 0
    for single_piece in single_gen(moving_piece):
        atks |= rank_attacks(single_piece, board, color) | file_attacks(single_piece, board, color)
    return atks

def rook_moves(moving_piece, board, color):
    return rook_attacks(moving_piece, board, color) & nnot(get_colored_pieces(board, color))

# ========== QUEEN ==========

def get_queen(board, color):
    return list2int([ i&(COLOR_MASK|PIECE_MASK) == color|QUEEN for i in board ])

def queen_rays(moving_piece):
    return rook_rays(moving_piece) | bishop_rays(moving_piece)

def queen_attacks(moving_piece, board, color):
    return bishop_attacks(moving_piece, board, color) | rook_attacks(moving_piece, board, color)

def queen_moves(moving_piece, board, color):
    return bishop_moves(moving_piece, board, color) | rook_moves(moving_piece, board, color)

# ===========================

def pseudo_legal_moves(game, color):
    return pawn_moves(get_pawns(game.board, color), game, color)           | \
           knight_moves(get_knights(game.board, color), game.board, color) | \
           bishop_moves(get_bishops(game.board, color), game.board, color) | \
           rook_moves(get_rooks(game.board, color), game.board, color)     | \
           queen_moves(get_queen(game.board, color), game.board, color)    | \
           king_moves(get_king(game.board, color), game.board, color)

def is_attacked(target, board, color):
    return count_attacks(target, board, color) > 0

def is_check(board, color):
    return is_attacked(get_king(board, color), board, opposing_color(color))

def count_attacks(target, board, attacking_color):
    attack_count = 0
    for pawn in colored_piece_gen(board, PAWN, attacking_color):
        if pawn_attacks(pawn, board, attacking_color)&target:
            attack_count += 1
    for knight in colored_piece_gen(board, KNIGHT, attacking_color):
        if knight_attacks(knight)&target:
            attack_count += 1
    for bishop in colored_piece_gen(board, BISHOP, attacking_color):
        if bishop_attacks(bishop, board, attacking_color)&target:
            attack_count += 1
    for rook in colored_piece_gen(board, ROOK, attacking_color):
        if rook_attacks(rook, board, attacking_color)&target:
            attack_count += 1
    for queen in colored_piece_gen(board, QUEEN, attacking_color):
        if queen_attacks(queen, board, attacking_color)&target:
            attack_count += 1
    for king in colored_piece_gen(board, KING, attacking_color):
        if king_attacks(king)&target:
            attack_count += 1
    return attack_count

def material_sum(board, color):
    material = 0
    for piece in board:
        if piece&COLOR_MASK == color:
            material += PIECE_VALUES[piece&PIECE_MASK]
    return material

def material_balance(board):
    return material_sum(board, WHITE) - material_sum(board, BLACK)
    
def pseudo_legal_moves_gen(game, color):
    for pawn in colored_piece_gen(game.board, PAWN, color):
        for pawn_move in single_gen(pawn_moves(pawn, game, color)):
            yield [pawn, pawn_move]
    for knight in colored_piece_gen(game.board, KNIGHT, color):
        for knight_move in single_gen(knight_moves(knight, game.board, color)):
            yield [knight, knight_move]
    for bishop in colored_piece_gen(game.board, BISHOP, color):
        for bishop_move in single_gen(bishop_moves(bishop, game.board, color)):
            yield [bishop, bishop_move]
    for rook in colored_piece_gen(game.board, ROOK, color):
        for rook_move in single_gen(rook_moves(rook, game.board, color)):
            yield [rook, rook_move]
    for queen in colored_piece_gen(game.board, QUEEN, color):
        for queen_move in single_gen(queen_moves(queen, game.board, color)):
            yield [queen, queen_move]
    for king in colored_piece_gen(game.board, KING, color):
        for king_move in single_gen(king_moves(king, game.board, color)):
            yield [king, king_move]
        if can_castle_kingside(game, color):
            yield [king, east_one(east_one(king))]
        if can_castle_queenside(game, color):
            yield [king, west_one(west_one(king))]

def legal_moves_gen(game, color):
    for move in pseudo_legal_moves_gen(game, color):
        if is_legal_move(game, move):
            yield move

def is_legal_move(game, move):
    new_game = make_move(game, move)
    return not is_check(new_game.board, game.to_move)
    
def count_legal_moves(game, color):
    count = 0
    for _ in legal_moves_gen(game, color):
        count += 1
    return count

def is_checkmate(game, color):
    return count_legal_moves(game, color) == 0 and is_check(game.board, color)

def is_stalemate(game):
    return count_legal_moves(game, game.to_move) == 0 and not is_check(game.board, game.to_move)

def insufficient_material(game): # TODO: other insufficient positions
    if material_sum(game.board, WHITE) + material_sum(game.board, BLACK) == 2*PIECE_VALUES[KING]:
        return True
    if material_sum(game.board, WHITE) == PIECE_VALUES[KING]:
        if material_sum(game.board, BLACK) == PIECE_VALUES[KING] + PIECE_VALUES[KNIGHT] and \
        (get_knights(game.board, BLACK) != 0 or get_bishops(game.board, BLACK) != 0):
            return True
    if material_sum(game.board, BLACK) == PIECE_VALUES[KING]:
        if material_sum(game.board, WHITE) == PIECE_VALUES[KING] + PIECE_VALUES[KNIGHT] and \
        (get_knights(game.board, WHITE) != 0 or get_bishops(game.board, WHITE) != 0):
            return True
    return False

def game_ended(game):
    return is_checkmate(game, WHITE) or \
           is_checkmate(game, BLACK) or \
           is_stalemate(game) or \
           insufficient_material(game)

def random_move(game, color):
    if count_legal_moves(game, color) == 0:
        print('Game over! ' + 'BLACK' if game.to_move == WHITE else 'WHITE' + ' wins!' )
        sys.exit(0)
        
    legal_moves = []
    for move in legal_moves_gen(game, color):
        legal_moves.append(move)
    return choice(legal_moves)
        
def material_move(game, color):
    
    if count_legal_moves(game, color) == 0:
        print('Game over! ' + 'BLACK' if game.to_move == WHITE else 'WHITE' + ' wins!' )
        sys.exit(0)
    
    if color == WHITE:
        best_material = -PIECE_VALUES[KING]
        best_moves = []
        for move in legal_moves_gen(game, color):
            material = material_balance(make_move(game, move).board)
            if material > best_material:
                best_material = material
                best_moves = [move]
            elif material == best_material:
                best_moves.append(move)
        return choice(best_moves)
        
    if color == BLACK:
        best_material = PIECE_VALUES[KING]
        best_moves = []
        for move in legal_moves_gen(game, color):
            material = material_balance(make_move(game, move).board)
            if material < best_material:
                best_material = material
                best_moves = [move]
            elif material == best_material:
                best_moves.append(move)
        return choice(best_moves)

def iterated_material_move(game, color):
    
    if color == WHITE:
        best_material = -PIECE_VALUES[KING]
        best_moves = []
        
        for move in legal_moves_gen(game, color):
            his_game = make_move(game, move)
            best_reply = material_move(his_game, opposing_color(color))
            
            material = material_balance(make_move(his_game, best_reply).board)
            
            if material > best_material:
                best_material = material
                best_moves = [move]
            elif material == best_material:
                best_moves.append(move)
        
    if color == BLACK:
        best_material = PIECE_VALUES[KING]
        best_moves = []
        
        for move in legal_moves_gen(game, color):
            his_game = make_move(game, move)
            best_reply = material_move(his_game, opposing_color(color))
            
            material = material_balance(make_move(his_game, best_reply).board)
            
            if material < best_material:
                best_material = material
                best_moves = [move]
            elif material == best_material:
                best_moves.append(move)
    return choice(best_moves)
        

def parse_move_code(game, move_code):
    move_code = move_code.replace(" ","")
    move_code = move_code.replace("x","")
    
    if move_code.upper() == 'O-O' or move_code == '0-0':
        if can_castle_kingside(game, game.to_move):
            return castle_kingside_move(game)
        
    if move_code.upper() == 'O-O-O' or move_code == '0-0-0':
        if can_castle_queenside(game, game.to_move):
            return castle_queenside_move(game)
    
    if len(move_code) < 2 or len(move_code) > 4:
        return False
    
    if len(move_code) == 4:
        filter_squares = get_filter(move_code[1])
    else:
        filter_squares = ALL_SQUARES

    destination_str = move_code[-2:]
    if destination_str[0] in FILES and destination_str[1] in RANKS:
        target_square = str2bb(destination_str)
    else:
        return False

    if len(move_code) == 2:
        piece = PAWN
    else:
        piece_code = move_code[0]
        if piece_code in FILES:
            piece = PAWN
            filter_squares = get_filter(piece_code)
        elif piece_code in PIECE_CODES:
            piece = PIECE_CODES[piece_code]&PIECE_MASK
        else:
            return False
    
    valid_moves = []
    for move in legal_moves_gen(game, game.to_move):
        if move[1] & target_square and \
           move[0] & filter_squares and \
           get_piece(game.board, move[0])&PIECE_MASK == piece:
            valid_moves.append(move)                     
    
    if len(valid_moves) == 1:
        return valid_moves[0]
    else:
        return False

def get_player_move(game):
    move = None
    while not move:
        move = parse_move_code(game, raw_input())
        if not move:
            print('Invalid move!')
    return move

def get_AI_move(game):
#     move = random_move(game, game.to_move)

    if find_in_book(game):
        move = get_book_move(game)
    else:
#         move = material_move(game, game.to_move)
        move = iterated_material_move(game, game.to_move)
    
    print(PIECE_CODES[get_piece(game.board, move[0])] + ' from ' + str(bb2str(move[0])) + ' to ' + str(bb2str(move[1])))
    return move

def print_outcome(game):
    if is_stalemate(game):
        print('Draw by stalemate')
    if is_checkmate(game, WHITE):
        print('BLACK wins!')
    if is_checkmate(game, BLACK):
        print('WHITE wins!')
    if insufficient_material(game):
        print('Draw by insufficient material!')

def play_as_white():
    game = ChessGame()
    print('Playing as white!')
    while True:
        print_board(game.board)
        if game_ended(game):
            break
        
        game = make_move(game, get_player_move(game))
        
        print_board(game.board)
        if game_ended(game):
            break
        
        game = make_move(game, get_AI_move(game))
    print_outcome(game)


def play_as_black():
    game = ChessGame()
    print('Playing as black!')
    while True:
        print_rotated_board(game.board)
        if game_ended(game):
            break
        
        game = make_move(game, get_AI_move(game))
        
        print_rotated_board(game.board)
        if game_ended(game):
            break
        
        game = make_move(game, get_player_move(game))
    print_outcome(game)

def watch_AI_game(sleep_seconds=0):
    game = ChessGame()
    print('Watching AI-vs-AI game!')
    while True:
        print_board(game.board)
        if game_ended(game):
            break
                
        game = make_move(game, get_AI_move(game))
        sleep(sleep_seconds)
    print_outcome(game)
    
        
def play_as(color):
    if color == WHITE:
        play_as_white()
    if color == BLACK:
        play_as_black()

def play_random_color():
    color = choice([WHITE, BLACK])
    play_as(color)

def find_in_book(game):    
    openings = []
    book_file = open("book.txt")
    for line in book_file:
        if line.startswith(game.get_move_list()) and line.rstrip() > game.get_move_list():
            openings.append(line.rstrip())
    book_file.close()
    return openings

def get_book_move(game):
    openings = find_in_book(game)
    chosen_opening = choice(openings)
    next_moves = chosen_opening.replace(game.get_move_list(), '').lstrip()
    move_str = next_moves.split(' ')[0]
    move = [str2bb(move_str[:2]), str2bb(move_str[-2:])]
    return move

# ========== TESTS ==========

# for move in legal_moves_gen(test_game, test_game.to_move):
#     new_pos = make_move(test_game, move).board
#     print_board(new_pos)
# test_game = ChessGame('r3kbnr/ppp3pp/3pqp2/8/1n5P/1b2K1P1/PPPPPP2/RNBQ1BNR w kq - 0 1')
# print_board(test_game.board)
# print_bitboard(empty_squares(test_game.board))
# print_bitboard(occupied_squares(test_game.board))
# print_bitboard(pawn_attacks(get_pawns(test_game.board, WHITE), test_game.board, WHITE))
# print_bitboard(pawn_double_attacks(get_pawns(test_game.board, WHITE), test_game.board, WHITE))
# print_bitboard(pawn_captures(get_pawns(test_game.board, WHITE), test_game, WHITE))
# print_bitboard(king_moves(get_king(test_game.board, BLACK), test_game.board, BLACK) | pawn_moves(get_pawns(test_game.board, WHITE), ChessGame(), WHITE))
# print_bitboard(knight_moves(get_knights(test_game.board, BLACK), test_game.board, BLACK))
# print_bitboard(get_rooks(test_game.board, WHITE) | get_bishops(test_game.board, WHITE))
# print_bitboard(rook_rays(get_queen(test_game.board, BLACK)))
# print_bitboard(queen_rays(get_queen(test_game.board, WHITE)))
# print_bitboard(bishop_rays(str2bb('c5')))
# print_bitboard(rook_rays(str2bb('f2')))
# print_bitboard(queen_rays(str2bb('h4')))
# print_bitboard(msb(ALL_SQUARES))
# print_bitboard(lsb(ALL_SQUARES))
# print_bitboard(rook_moves(get_queen(test_game.board, WHITE), test_game.board, WHITE))
# print_bitboard(bishop_moves(get_bishops(test_game.board, WHITE)&black_pieces(test_game.board), test_game.board, BLACK))
# print_bitboard(queen_moves(get_queen(test_game.board, WHITE)&black_pieces(test_game.board), test_game.board, BLACK))
# print_bitboard(queen_moves(get_queen(test_game.board, WHITE), test_game.board, BLACK))
# print_bitboard(king_moves(get_queen(test_game.board, WHITE), test_game.board, WHITE))
# print_bitboard(pseudo_legal_moves(test_game, WHITE)&get_colored_pieces(test_game.board, BLACK))
# print_bitboard(pseudo_legal_moves(test_game, BLACK)&get_colored_pieces(test_game.board, WHITE))
# print_bitboard(knight_fill(str2bb('a1'), 2))
# print(knight_distance('a1', 'h8'))
# print_bitboard(pseudo_legal_moves(test_game, BLACK))
# print(is_check(test_game.board, WHITE))
# print(is_check(test_game.board, BLACK))
# print_bitboard(pawn_moves(str2bb('d2'), test_game, WHITE))
# print_bitboard(pseudo_legal_moves(test_game, WHITE)&get_colored_pieces(test_game.board, BLACK))
# print_bitboard(pseudo_legal_moves(test_game, BLACK)&get_colored_pieces(test_game.board, WHITE))
# print(count_attacks(str2bb('B3'), test_game.board, WHITE))
# print(count_attacks(str2bb('B3'), test_game.board, BLACK))
# print(bin(FULL_CASTLING_RIGHTS))
# game = ChessGame('r3kbnr/ppp3pp/3pqp2/8/1n5P/1b2K1P1/PPPPPP2/RNBQ1BNR b KQkq - 0 1')
# print(can_castle_kingside(game, WHITE))
# print(can_castle_queenside(game, WHITE))
# print(can_castle_kingside(game, BLACK))
# print(can_castle_queenside(game, BLACK))
# print(bin(game.castling_rights))
# print(game.make_castle_queenside())
# print(game.make_castle_queenside())
# print(bin(game.castling_rights))
# print_board(game.board)
# print_board(move_piece(test_game.board, (str2bb('g1'), str2bb('f3'))))
# print_board(move_piece(test_game.board, (str2bb('e2'), str2bb('f3'))))
# print(game.to_FEN())
# game = ChessGame('1r1q2k1/B4p1p/4r1p1/3n2P1/b4P2/7P/8/3R2K1 w - - 1 28')
# print_board(game.board)
# print_rotated_board(game.board)
# print(game.to_FEN())
# print(material_sum(game.board, WHITE))
# print(material_sum(game.board, BLACK))
# print(material_balance(game.board))
# print(piece2str(get_piece(game.board, str2bb('a7'))))
# game = ChessGame('1r1q2k1/B4p2/4r1p1/3n2Pp/b4P2/7P/8/3R2K1 w KQ h6 1 28')
# print_board(game.board)
# print(game.to_FEN())
# game = ChessGame('1r1q2k1/B4p2/4r1p1/3n2Pp/b4P2/7P/8/3R2K1 b - h6 1 28')
# print_board(game.board)
# game = ChessGame('rnbqkbnr/1pppppp1/8/2p2P2/1P6/Q6Q/1PP2BP1/RNBQKBNR w KQkq - 0 1')
# print_board(game.board)
# test_game = ChessGame('k7/8/1Q6/8/8/8/8/1R4K1 b - - 0 15')
# print('checkmate = ' + str(is_checkmate(test_game, test_game.to_move)))
# print('stalemate = ' + str(is_stalemate(test_game)))
# print_board(test_game.board)
# print(test_game.to_FEN())
# game = ChessGame('rnbqkbnr/1pppppp1/3B4/2p2P2/1P1P4/Q6Q/1PP3P1/RNBQKBNR w KQkq - 0 1')

# ========== /TESTS ==========

# watch_AI_game()
play_random_color()