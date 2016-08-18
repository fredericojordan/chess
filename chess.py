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

PIECE_TYPES = [ PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING ]

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

EMPTY_BOARD = [ EMPTY for _ in range(64) ]

INITIAL_GAME = { 'board': INITIAL_BOARD,
                 'to_move': WHITE,
                 'epsquare': EMPTY_BOARD, # maybe use bitmask?
                 'halfmove_clock': 0,
                 'fullmove_number': 1 }

def get_piece(board, bitboard):
    for i in range(64):
        if (bitboard >> i) & 0b1:
            return board[i]

def parse_pos(position):
    fille = FILES.index(position[0].lower())
    rank = RANKS.index(position[1])
    return 8*rank + fille

def single_pos(position):
    return 0b1 << parse_pos(position)

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

def piece_str(piece):
    piece_strings = { WHITE|KING:  'K',
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
    return piece_strings[ piece & (PIECE_MASK|COLOR_MASK) ]
    
def print_board(board):
    print('')
    for i in range(len(RANKS)):
        rank_str = str(8-i) + ' '
        first = len(board) - 8*(i+1)
        for fille in range(len(FILES)):
            rank_str += '{} '.format(piece_str(board[first+fille]))
        print(rank_str)
    print('  a b c d e f g h')
    
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

def black_pieces(board):
    return get_colored_pieces(board, BLACK)
 
def white_pieces(board):
    return get_colored_pieces(board, WHITE)

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

# ========== PAWN ==========

def get_pawns(board, color):
    return list2int([ i&(COLOR_MASK|PIECE_MASK) == color|PAWN for i in board ])

def pawn_moves(moving_piece, board, color):
    return pawn_pushes(moving_piece, board, color) | pawn_captures(moving_piece, board, color)

def pawn_pushes(moving_piece, board, color):
    return pawn_simple_pushes(moving_piece, board, color) | pawn_double_pushes(moving_piece, board, color)

def pawn_captures(attacking_piece, board, color):
    return pawn_attacks(attacking_piece, board, color) & get_colored_pieces(board, opposing_color(color))

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
    init_bitboard = single_pos(pos1)
    end_bitboard = single_pos(pos2)
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

def pseudo_legal_moves(board, color): # FIXME: add castling?
    return pawn_moves(get_pawns(board, color), board, color)     | \
           knight_moves(get_knights(board, color), board, color) | \
           bishop_moves(get_bishops(board, color), board, color) | \
           rook_moves(get_rooks(board, color), board, color)     | \
           queen_moves(get_queen(board, color), board, color)    | \
           king_moves(get_king(board, color), board, color)

def is_attacked(target, board, color):
    return pseudo_legal_moves(board, color)&target != 0

def is_check(board, color):
    return is_attacked(get_king(board, color), TEST_BOARD, opposing_color(color))

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


TEST_BOARD = [ WHITE|ROOK, WHITE|KNIGHT, WHITE|BISHOP, WHITE|QUEEN, EMPTY,       WHITE|BISHOP, WHITE|KNIGHT, WHITE|ROOK,
               WHITE|PAWN, WHITE|PAWN,   WHITE|PAWN,   WHITE|PAWN,  WHITE|PAWN,  WHITE|PAWN,   EMPTY,        EMPTY,
               EMPTY,      BLACK|BISHOP, EMPTY,        EMPTY,       WHITE|KING,  EMPTY,        WHITE|PAWN,   EMPTY,
               EMPTY,      BLACK|KNIGHT, EMPTY,        EMPTY,       EMPTY,       EMPTY,        EMPTY,        WHITE|PAWN,
               EMPTY,      EMPTY,        EMPTY,        EMPTY,       EMPTY,       EMPTY,        EMPTY,        EMPTY,
               EMPTY,      EMPTY,        EMPTY,        BLACK|PAWN,  BLACK|QUEEN, BLACK|PAWN,   EMPTY,        EMPTY,
               BLACK|PAWN, BLACK|PAWN,   BLACK|PAWN,   EMPTY,       EMPTY,       EMPTY,        BLACK|PAWN,   BLACK|PAWN,
               BLACK|ROOK, EMPTY,        EMPTY,        EMPTY,       BLACK|KING,  BLACK|BISHOP, BLACK|KNIGHT, BLACK|ROOK ]

print_board(TEST_BOARD)
# print_bitboard(empty_squares(TEST_BOARD))
# print_bitboard(occupied_squares(TEST_BOARD))
# print_bitboard(pawn_attacks(get_pawns(TEST_BOARD, WHITE), TEST_BOARD, WHITE))
# print_bitboard(pawn_double_attacks(get_pawns(TEST_BOARD, WHITE), TEST_BOARD, WHITE))
# print_bitboard(pawn_captures(get_pawns(TEST_BOARD, WHITE), TEST_BOARD, WHITE))
# print_bitboard(king_moves(get_king(TEST_BOARD, BLACK), TEST_BOARD, BLACK) | pawn_moves(get_pawns(TEST_BOARD, WHITE), TEST_BOARD, WHITE))
# print_bitboard(knight_moves(get_knights(TEST_BOARD, BLACK), TEST_BOARD, BLACK))
# print_bitboard(get_rooks(TEST_BOARD, WHITE) | get_bishops(TEST_BOARD, WHITE))
# print_bitboard(rook_rays(get_queen(TEST_BOARD, BLACK)))
# print_bitboard(queen_rays(get_queen(TEST_BOARD, WHITE)))
# print_bitboard(bishop_rays(single_pos('c5')))
# print_bitboard(rook_rays(single_pos('f2')))
# print_bitboard(queen_rays(single_pos('h4')))
# print_bitboard(msb(ALL_SQUARES))
# print_bitboard(lsb(ALL_SQUARES))
# print_bitboard(rook_moves(get_queen(TEST_BOARD, WHITE), TEST_BOARD, WHITE))
# print_bitboard(bishop_moves(get_bishops(TEST_BOARD, WHITE)&black_pieces(TEST_BOARD), TEST_BOARD, BLACK))
# print_bitboard(queen_moves(get_queen(TEST_BOARD, WHITE)&black_pieces(TEST_BOARD), TEST_BOARD, BLACK))
# print_bitboard(queen_moves(get_queen(TEST_BOARD, WHITE), TEST_BOARD, BLACK))
# print_bitboard(king_moves(get_queen(TEST_BOARD, WHITE), TEST_BOARD, WHITE))
# print_bitboard(pseudo_legal_moves(TEST_BOARD, WHITE)&get_colored_pieces(TEST_BOARD, BLACK))
# print_bitboard(pseudo_legal_moves(TEST_BOARD, BLACK)&get_colored_pieces(TEST_BOARD, WHITE))
# print_bitboard(knight_fill(single_pos('a1'), 2))
# print(knight_distance('a1', 'h8'))
# print_bitboard(pseudo_legal_moves(TEST_BOARD, BLACK))
# print(is_check(TEST_BOARD, WHITE))
# print(is_check(TEST_BOARD, BLACK))
# print_bitboard(pawn_moves(single_pos('d2'), TEST_BOARD, WHITE))
# print_bitboard(pseudo_legal_moves(TEST_BOARD, WHITE)&get_colored_pieces(TEST_BOARD, BLACK))
# print_bitboard(pseudo_legal_moves(TEST_BOARD, BLACK)&get_colored_pieces(TEST_BOARD, WHITE))
# print(count_attacks(single_pos('B3'), TEST_BOARD, WHITE))
# print(count_attacks(single_pos('B3'), TEST_BOARD, BLACK))