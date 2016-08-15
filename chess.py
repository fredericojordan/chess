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

'''
COLOR_MASK = 1 << 7
WHITE = 0 << 7
BLACK = 1 << 7

PIECE_MASK = 0b111
EMPTY = 0
PAWN = 1
KNIGHT = 2
BISHOP = 3
ROOK = 4
QUEEN = 5
KING = 6

HAS_MOVED_FLAG = 1 << 3
CASTLE_FLAG = 1 << 4

FILES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
RANKS = ['1', '2', '3', '4', '5', '6', '7', '8']

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

EMPTY_BOARD = [ 0 for _ in range(64) ]

def parse_pos(position):
    file = FILES.index(position[0])
    rank = RANKS.index(position[1])
    return 8*rank + file

def piece_str(piece):
    piece_codes = { WHITE|KING:  'K',
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
    return piece_codes[ piece & (PIECE_MASK|COLOR_MASK) ]
    
def print_board(board):
    print('')
    for i in range(len(RANKS)):
        rank_str = str(8-i) + " "
        first = len(board) - 8*(i+1)
        for file in range(len(FILES)):
            rank_str += "{} ".format(piece_str(board[first+file]))
        print(rank_str)
    print('  a b c d e f g h')
    
def print_bitboard(board):
    print("")
    for rank in range(len(RANKS)):
        rank_str = str(8-rank) + " "
        for file in range(len(FILES)):
            if (board >> (file + (7-rank)*8)) & 0b1:
                rank_str += "# "
            else:
                rank_str += ". "
        print(rank_str)
    print('  a b c d e f g h')

def black_pieces(board):
    return list2int([ (i&COLOR_MASK == BLACK and i&PIECE_MASK != EMPTY) for i in board ])

def white_pieces(board):
    return list2int([ (i&COLOR_MASK == WHITE and i&PIECE_MASK != EMPTY) for i in board ])

def empty_squares(board):
    return list2int([ i&PIECE_MASK == EMPTY for i in board ])

def occupied_squares(board):
    return list2int([ i&PIECE_MASK != EMPTY for i in board ])

def list2int(lst):
    rev_list = lst[:]
    rev_list.reverse()
    return int('0b' + ''.join(['1' if i else '0' for i in rev_list]), 2)

def nnot(bitboard):
    return (bitboard ^ ALL_SQUARES)

def east_one(bitboard):
    return (bitboard << 1) & nnot(FILE_A)

def west_one(bitboard):
    return (bitboard >> 1) & nnot(FILE_H)

def north_one(bitboard):
    return (bitboard << 8) & nnot(RANK_1)

def south_one(bitboard):
    return (bitboard >> 8) & nnot(RANK_8)

# ========== PAWNS ==========

def pawns(board):
    return list2int([ i&PIECE_MASK == PAWN for i in board ])

def pawn_moves(board, color):
    return pawn_pushes(board, color) | pawn_captures(board, color)

def pawn_pushes(board, color):
    return pawn_simple_pushes(board, color) | pawn_double_pushes(board, color)

def pawn_captures(board, color):
    if color == WHITE:
        return pawn_attacks(board, color) & black_pieces(board)
    if color == BLACK:
        return pawn_attacks(board, color) & white_pieces(board)

def pawn_attacks(board, color):
    return pawn_east_attacks(board, color) | pawn_west_attacks(board, color)

def pawn_simple_pushes(board, color):
    if color == WHITE:
        return ((pawns(board) & white_pieces(board)) << 8) & empty_squares(board)
    if color == BLACK:
        return ((pawns(board) & black_pieces(board)) >> 8) & empty_squares(board)
    
def pawn_double_pushes(board, color):
    if color == WHITE:
        return ((pawn_simple_pushes(board, color)) << 8) & (empty_squares(board) & RANK_4)
    if color == BLACK:
        return ((pawn_simple_pushes(board, color)) >> 8) & (empty_squares(board) & RANK_5)

def pawn_east_attacks(board, color):
    if color == WHITE:
        return ((pawns(board) & white_pieces(board)) << 7 & nnot(FILE_H))
    if color == BLACK:
        return ((pawns(board) & black_pieces(board)) >> 9 & nnot(FILE_H))

def pawn_west_attacks(board, color):
    if color == WHITE:
        return ((pawns(board) & white_pieces(board)) << 9 & nnot(FILE_A))
    if color == BLACK:
        return ((pawns(board) & black_pieces(board)) >> 7 & nnot(FILE_A))

def pawn_double_attacks(board, color):
    return pawn_east_attacks(board, color) & pawn_west_attacks(board, color)

# ========== KNIGHTS ==========

def knights(board):
    return list2int([ i&PIECE_MASK == KNIGHT for i in board ])

def knight_moves(board, color):
    if color == WHITE:
        return knight_attacks(knights(board) & white_pieces(board)) & nnot(white_pieces(board))
    if color == BLACK:
        return knight_attacks(knights(board) & black_pieces(board)) & nnot(black_pieces(board))

def knight_attacks(bitboard):
    return knight_NNE(bitboard) | \
           knight_ENE(bitboard) | \
           knight_NNW(bitboard) | \
           knight_WNW(bitboard) | \
           knight_SSE(bitboard) | \
           knight_ESE(bitboard) | \
           knight_SSW(bitboard) | \
           knight_WSW(bitboard)

def knight_WNW(bitboard):
    return bitboard << 6 & nnot(FILE_G | FILE_H)

def knight_ENE(bitboard):
    return bitboard << 10 & nnot(FILE_A | FILE_B)

def knight_NNW(bitboard):
    return bitboard << 15 & nnot(FILE_H)

def knight_NNE(bitboard):
    return bitboard << 17 & nnot(FILE_A)

def knight_ESE(bitboard):
    return bitboard >> 6 & nnot(FILE_A | FILE_B)

def knight_WSW(bitboard):
    return bitboard >> 10 & nnot(FILE_G | FILE_H)

def knight_SSE(bitboard):
    return bitboard >> 15 & nnot(FILE_A)

def knight_SSW(bitboard):
    return bitboard >> 17 & nnot(FILE_H)

# ========== KINGS ==========

def kings(board):
    return list2int([ i&PIECE_MASK == KING for i in board ])

def king_moves(board, color):
    if color == WHITE:
        return king_attacks(kings(board) & white_pieces(board)) & nnot(white_pieces(board))
    if color == BLACK:
        return king_attacks(kings(board) & black_pieces(board)) & nnot(black_pieces(board))

def king_attacks(bitboard):
    king_atks = bitboard | east_one(bitboard) | west_one(bitboard)
    king_atks |= north_one(king_atks) | south_one(king_atks)
    return king_atks & nnot(bitboard)











TEST_BOARD = [ WHITE|ROOK, WHITE|KNIGHT, WHITE|BISHOP, WHITE|QUEEN, WHITE|KING, WHITE|BISHOP, WHITE|KNIGHT, WHITE|ROOK,
               WHITE|PAWN, WHITE|PAWN,   WHITE|PAWN,   WHITE|PAWN,  WHITE|PAWN, WHITE|PAWN,   EMPTY,        EMPTY,
               EMPTY,      BLACK|BISHOP, EMPTY,        EMPTY,       EMPTY,      EMPTY,        WHITE|PAWN,   EMPTY,
               EMPTY,      BLACK|KNIGHT, EMPTY,        EMPTY,       EMPTY,      EMPTY,        EMPTY,        WHITE|PAWN,
               EMPTY,      EMPTY,        EMPTY,        EMPTY,       EMPTY,      EMPTY,        EMPTY,        EMPTY,
               EMPTY,      EMPTY,        EMPTY,        BLACK|PAWN,  EMPTY,      BLACK|PAWN,   EMPTY,        EMPTY,
               BLACK|PAWN, BLACK|PAWN,   BLACK|PAWN,   EMPTY,       EMPTY,      EMPTY,        BLACK|PAWN,   BLACK|PAWN,
               BLACK|ROOK, EMPTY,        EMPTY,        BLACK|QUEEN, BLACK|KING, BLACK|BISHOP, BLACK|KNIGHT, BLACK|ROOK ]

print_board(TEST_BOARD)
print_bitboard(king_moves(TEST_BOARD, BLACK) | pawn_moves(TEST_BOARD, WHITE))
print_bitboard(knight_moves(TEST_BOARD, BLACK))

