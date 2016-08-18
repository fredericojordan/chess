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
    fille = FILES.index(position[0])
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

def pawns(board):
    return list2int([ i&PIECE_MASK == PAWN for i in board ])

def pawn_moves(board, color):
    return pawn_pushes(board, color) | pawn_captures(board, color)

def pawn_pushes(board, color):
    return pawn_simple_pushes(board, color) | pawn_double_pushes(board, color)

def pawn_captures(board, color):
    if color == WHITE:
        return pawn_attacks(board, color) & get_colored_pieces(board, BLACK)
    if color == BLACK:
        return pawn_attacks(board, color) & get_colored_pieces(board, WHITE)

def pawn_attacks(board, color):
    return pawn_east_attacks(board, color) | pawn_west_attacks(board, color)

def pawn_simple_pushes(board, color):
    if color == WHITE:
        return north_one(pawns(board) & get_colored_pieces(board, color)) & empty_squares(board)
    if color == BLACK:
        return south_one(pawns(board) & get_colored_pieces(board, color)) & empty_squares(board)
    
def pawn_double_pushes(board, color):
    if color == WHITE:
        return north_one(pawn_simple_pushes(board, color)) & (empty_squares(board) & RANK_4)
    if color == BLACK:
        return south_one(pawn_simple_pushes(board, color)) & (empty_squares(board) & RANK_5)

def pawn_east_attacks(board, color):
    if color == WHITE:
        return NE_one(pawns(board) & get_colored_pieces(board, color))
    if color == BLACK:
        return SE_one(pawns(board) & get_colored_pieces(board, color))

def pawn_west_attacks(board, color):
    if color == WHITE:
        return NW_one(pawns(board) & get_colored_pieces(board, color))
    if color == BLACK:
        return SW_one(pawns(board) & get_colored_pieces(board, color))

def pawn_double_attacks(board, color):
    return pawn_east_attacks(board, color) & pawn_west_attacks(board, color)

# ========== KNIGHT ==========

def knights(board):
    return list2int([ i&PIECE_MASK == KNIGHT for i in board ])

def knight_moves(board, color):
    return knight_attacks(knights(board) & get_colored_pieces(board, color)) & nnot(get_colored_pieces(board, color))

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

def knight_fill(bitboard, n):
    fill = bitboard
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

def kings(board):
    return list2int([ i&PIECE_MASK == KING for i in board ])

def get_king(board, color):
    return kings(board)&get_colored_pieces(board, color)

def king_moves(board, color):
    return king_attacks(kings(board) & get_colored_pieces(board, color)) & nnot(get_colored_pieces(board, color))

def king_attacks(bitboard):
    king_atks = bitboard | east_one(bitboard) | west_one(bitboard)
    king_atks |= north_one(king_atks) | south_one(king_atks)
    return king_atks & nnot(bitboard)

# ========== BISHOP ==========

def bishops(board):
    return list2int([ i&PIECE_MASK == BISHOP for i in board ])

def bishop_rays(bitboard):
    return diagonal_rays(bitboard) | anti_diagonal_rays(bitboard)
           
def diagonal_rays(bitboard):
    return NE_ray(bitboard) | SW_ray(bitboard)

def anti_diagonal_rays(bitboard):
    return NW_ray(bitboard) | SE_ray(bitboard)

def NE_ray(bitboard):
    ray_atks = NE_one(bitboard)
    for _ in range(6):
        ray_atks |= NE_one(ray_atks)
    return ray_atks & ALL_SQUARES

def SE_ray(bitboard):
    ray_atks = SE_one(bitboard)
    for _ in range(6):
        ray_atks |= SE_one(ray_atks)
    return ray_atks & ALL_SQUARES

def NW_ray(bitboard):
    ray_atks = NW_one(bitboard)
    for _ in range(6):
        ray_atks |= NW_one(ray_atks)
    return ray_atks & ALL_SQUARES

def SW_ray(bitboard):
    ray_atks = SW_one(bitboard)
    for _ in range(6):
        ray_atks |= SW_one(ray_atks)
    return ray_atks & ALL_SQUARES

def NE_attacks(single_bb, board, color):
    blocker = lsb(NE_ray(single_bb) & occupied_squares(board))
    if blocker:
        if get_piece(board, blocker)&COLOR_MASK == color:
            return (NE_ray(single_bb) ^ NE_ray(blocker)) & nnot(blocker)
        else:
            return NE_ray(single_bb) ^ NE_ray(blocker)
    else:
        return NE_ray(single_bb)
    
def NW_attacks(single_bb, board, color):
    blocker = lsb(NW_ray(single_bb) & occupied_squares(board))
    if blocker:
        if get_piece(board, blocker)&COLOR_MASK == color:
            return (NW_ray(single_bb) ^ NW_ray(blocker)) & nnot(blocker)
        else:
            return NW_ray(single_bb) ^ NW_ray(blocker)
    else:
        return NW_ray(single_bb)

def SE_attacks(single_bb, board, color):
    blocker = msb(SE_ray(single_bb) & occupied_squares(board))
    if blocker:
        if get_piece(board, blocker)&COLOR_MASK == color:
            return (SE_ray(single_bb) ^ SE_ray(blocker)) & nnot(blocker)
        else:
            return SE_ray(single_bb) ^ SE_ray(blocker)
    else:
        return SE_ray(single_bb)

def SW_attacks(single_bb, board, color):
    blocker = msb(SW_ray(single_bb) & occupied_squares(board))
    if blocker:
        if get_piece(board, blocker)&COLOR_MASK == color:
            return (SW_ray(single_bb) ^ SW_ray(blocker)) & nnot(blocker)
        else:
            return SW_ray(single_bb) ^ SW_ray(blocker)
    else:
        return SW_ray(single_bb)

def diagonal_attacks(single_bb, board, color):
    return NE_attacks(single_bb, board, color) | SW_attacks(single_bb, board, color)

def anti_diagonal_attacks(single_bb, board, color):
    return NW_attacks(single_bb, board, color) | SE_attacks(single_bb, board, color)

def bishop_attacks(bitboard, board, color):
    atks = 0
    for single_bb in single_gen(bitboard):
        atks |= diagonal_attacks(single_bb, board, color) | anti_diagonal_attacks(single_bb, board, color)
    return atks

def bishop_moves(board, color):
    bitboard = bishops(board)&get_colored_pieces(board, color)
    return bishop_attacks(bitboard, board, color)

# ========== ROOK ==========

def rooks(board):
    return list2int([ i&PIECE_MASK == ROOK for i in board ])

def rook_rays(bitboard):
    return rank_rays(bitboard) | file_rays(bitboard)

def rank_rays(bitboard):
    return east_ray(bitboard) | west_ray(bitboard)

def file_rays(bitboard):
    return north_ray(bitboard) | south_ray(bitboard)

def east_ray(bitboard):
    ray_atks = east_one(bitboard)
    for _ in range(6):
        ray_atks |= east_one(ray_atks)
    return ray_atks & ALL_SQUARES

def west_ray(bitboard):
    ray_atks = west_one(bitboard)
    for _ in range(6):
        ray_atks |= west_one(ray_atks)
    return ray_atks & ALL_SQUARES

def north_ray(bitboard):
    ray_atks = north_one(bitboard)
    for _ in range(6):
        ray_atks |= north_one(ray_atks)
    return ray_atks & ALL_SQUARES

def south_ray(bitboard):
    ray_atks = south_one(bitboard)
    for _ in range(6):
        ray_atks |= south_one(ray_atks)
    return ray_atks & ALL_SQUARES

def east_attacks(single_bb, board, color):
    blocker = lsb(east_ray(single_bb) & occupied_squares(board))
    if blocker:
        if get_piece(board, blocker)&COLOR_MASK == color:
            return (east_ray(single_bb) ^ east_ray(blocker)) & nnot(blocker)
        else:
            return east_ray(single_bb) ^ east_ray(blocker)
    else:
        return east_ray(single_bb)
    
def west_attacks(single_bb, board, color):
    blocker = msb(west_ray(single_bb) & occupied_squares(board))
    if blocker:
        if get_piece(board, blocker)&COLOR_MASK == color:
            return (west_ray(single_bb) ^ west_ray(blocker)) & nnot(blocker)
        else:
            return west_ray(single_bb) ^ west_ray(blocker)
    else:
        return west_ray(single_bb)
    
def rank_attacks(single_bb, board, color):
    return east_attacks(single_bb, board, color) | west_attacks(single_bb, board, color)

def north_attacks(single_bb, board, color):
    blocker = lsb(north_ray(single_bb) & occupied_squares(board))
    if blocker:
        if get_piece(board, blocker)&COLOR_MASK == color:
            return (north_ray(single_bb) ^ north_ray(blocker)) & nnot(blocker)
        else:
            return north_ray(single_bb) ^ north_ray(blocker)
    else:
        return north_ray(single_bb)
    
def south_attacks(single_bb, board, color):
    blocker = msb(south_ray(single_bb) & occupied_squares(board))
    if blocker:
        if get_piece(board, blocker)&COLOR_MASK == color:
            return (south_ray(single_bb) ^ south_ray(blocker)) & nnot(blocker)
        else:
            return south_ray(single_bb) ^ south_ray(blocker)
    else:
        return south_ray(single_bb)
    
def file_attacks(single_bb, board, color):
    return north_attacks(single_bb, board, color) | south_attacks(single_bb, board, color)

def rook_attacks(bitboard, board, color):
    atks = 0
    for single_bb in single_gen(bitboard):
        atks |= rank_attacks(single_bb, board, color) | file_attacks(single_bb, board, color)
    return atks

def rook_moves(board, color):
    bitboard = rooks(board)&get_colored_pieces(board, color)
    return rook_attacks(bitboard, board, color)

# ========== QUEEN ==========

def queens(board):
    return list2int([ i&PIECE_MASK == QUEEN for i in board ])

def queen_rays(bitboard):
    return rook_rays(bitboard) | bishop_rays(bitboard)

def queen_attacks(bitboard, board, color):
    return rook_attacks(bitboard, board, color) | bishop_attacks(bitboard, board, color)

def queen_moves(board, color):
    bitboard = queens(board)&get_colored_pieces(board, color)
    return queen_attacks(bitboard, board, color)

def pseudo_legal_moves(board, color): # FIXME: add castling?
    return pawn_moves(board, color)   | \
           knight_moves(board, color) | \
           bishop_moves(board, color) | \
           rook_moves(board, color)   | \
           queen_moves(board, color)  | \
           king_moves(board, color)

def is_attacked_by(bitboard, board, color):
    return pseudo_legal_moves(board, color)&bitboard != 0

def is_check_on(board, color):
    if color == WHITE:
        return is_attacked_by(get_king(board, WHITE), TEST_BOARD, BLACK)
    if color == BLACK:
        return is_attacked_by(get_king(board, BLACK), TEST_BOARD, WHITE)

def is_check(board):
    return is_check_on(board, WHITE) | is_check_on(board, BLACK) 


TEST_BOARD = [ WHITE|ROOK, WHITE|KNIGHT, WHITE|BISHOP, WHITE|QUEEN, EMPTY,       WHITE|BISHOP, WHITE|KNIGHT, WHITE|ROOK,
               WHITE|PAWN, WHITE|PAWN,   WHITE|PAWN,   WHITE|PAWN,  WHITE|PAWN,  WHITE|PAWN,   EMPTY,        EMPTY,
               EMPTY,      BLACK|BISHOP, EMPTY,        EMPTY,       WHITE|KING,  EMPTY,        WHITE|PAWN,   EMPTY,
               EMPTY,      BLACK|KNIGHT, EMPTY,        EMPTY,       EMPTY,       EMPTY,        EMPTY,        WHITE|PAWN,
               EMPTY,      EMPTY,        EMPTY,        EMPTY,       EMPTY,       EMPTY,        EMPTY,        EMPTY,
               EMPTY,      EMPTY,        EMPTY,        BLACK|PAWN,  EMPTY,       BLACK|PAWN,   EMPTY,        EMPTY,
               BLACK|PAWN, BLACK|PAWN,   BLACK|PAWN,   EMPTY,       BLACK|QUEEN, EMPTY,        BLACK|PAWN,   BLACK|PAWN,
               BLACK|ROOK, EMPTY,        EMPTY,        EMPTY,       BLACK|KING,  BLACK|BISHOP, BLACK|KNIGHT, BLACK|ROOK ]

print_board(TEST_BOARD)
# print_bitboard(empty_squares(TEST_BOARD))
# print_bitboard(occupied_squares(TEST_BOARD))
# print_bitboard(pawn_attacks(TEST_BOARD, WHITE))
# print_bitboard(pawn_double_attacks(TEST_BOARD, WHITE))
# print_bitboard(pawn_captures(TEST_BOARD, WHITE))
# print_bitboard(king_moves(TEST_BOARD, BLACK) | pawn_moves(TEST_BOARD, WHITE))
# print_bitboard(knight_moves(TEST_BOARD, BLACK))
# print_bitboard(rooks(TEST_BOARD) | bishops(TEST_BOARD))
# print_bitboard(rook_rays(queens(TEST_BOARD)))
# print_bitboard(queen_rays(queens(TEST_BOARD)))
# print_bitboard(bishop_rays(single_pos('c5')))
# print_bitboard(rook_rays(single_pos('f2')))
# print_bitboard(queen_rays(single_pos('h4')))
# print_bitboard(msb(ALL_SQUARES))
# print_bitboard(lsb(ALL_SQUARES))
# print_bitboard(rook_attacks(queens(TEST_BOARD), TEST_BOARD, WHITE))
# print_bitboard(bishop_attacks(bishops(TEST_BOARD)&black_pieces(TEST_BOARD), TEST_BOARD, BLACK))
# print_bitboard(queen_attacks(queens(TEST_BOARD)&black_pieces(TEST_BOARD), TEST_BOARD, BLACK))
# print_bitboard(queen_moves(TEST_BOARD, BLACK))
# print_bitboard(king_moves(TEST_BOARD, WHITE))
# print_bitboard(pseudo_legal_moves(TEST_BOARD, WHITE)&get_colored_pieces(TEST_BOARD, BLACK))
# print_bitboard(knight_fill(single_pos('a1'), 2))
# print(knight_distance('a1', 'h8'))
# print_bitboard(pseudo_legal_moves(TEST_BOARD, BLACK))
# print(is_check_on(TEST_BOARD, WHITE))
# print(is_check_on(TEST_BOARD, BLACK))
# print(is_check(TEST_BOARD))