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
from copy import deepcopy
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

WHITE_KINGSIDE_CASTLE  = 0b1 << 0
WHITE_QUEENSIDE_CASTLE = 0b1 << 1
BLACK_KINGSIDE_CASTLE  = 0b1 << 2
BLACK_QUEENSIDE_CASTLE = 0b1 << 3

FULL_CASTLING_RIGHTS = WHITE_KINGSIDE_CASTLE|WHITE_QUEENSIDE_CASTLE|BLACK_KINGSIDE_CASTLE|BLACK_QUEENSIDE_CASTLE

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


# ========== GAME ==========

class Game:
    def __init__(self, FEN=''):
        self.board = INITIAL_BOARD 
        self.to_move = WHITE
        self.ep = 0
        self.castling_rights = FULL_CASTLING_RIGHTS
        self.halfmove_clock = 0
        self.fullmove_number = 1
        if FEN != '':
            self.load_FEN(FEN)
        
    def increase_halfmove_clock(self):
        self.halfmove_clock += 1
        
    def reset_halfmove_clock(self):
        self.halfmove_clock = 0
        
    def increase_fullmove_number(self):
        self.fullmove_number += 1
        
    def next_to_move(self):
        self.to_move = opposing_color(self.to_move)
        
    def clear_ep_square(self):
        self.ep = 0
        
    def make_move(self, move_code):
        success = False
        reset_halfmove = False
        move_code = move_code.replace(" ", "")
        move_code = move_code.replace("x", "")
        
        if move_code.upper() == 'O-O' or move_code == '0-0':
            success = self.make_castle_kingside()
        if move_code.upper() == 'O-O-O' or move_code == '0-0-0':
            success = self.make_castle_queenside()
            
        piece_code = move_code[0].upper()
        target_square = single_pos(move_code[-2:])
        
        if get_piece(game.board, target_square)&PIECE_MASK != EMPTY:
            reset_halfmove = True
        
        if piece_code.lower() in FILES or piece_code == 'P':
            success = self.make_pawn_move(move_code)
            if success:
                reset_halfmove = True
        
        if piece_code == 'K':
            success = self.make_king_move(move_code)
                
        if piece_code == 'Q':
            success = self.make_queen_move(move_code)
            
        if piece_code == 'R':
            success = self.make_rook_move(move_code)
            
        if piece_code == 'B':
            success = self.make_bishop_move(move_code)
            
        if piece_code == 'N':
            success = self.make_knight_move(move_code)
        
        if success:
            self.increase_halfmove_clock()
            if self.to_move == BLACK:
                self.increase_fullmove_number()
            if reset_halfmove:
                self.reset_halfmove_clock()
            self.next_to_move()

        return success
    
    def make_pawn_move(self, move_code): # TODO: move, set ep
        return False
    
    def make_king_move(self, move_code):
        success = False
        valid_count = 0
        target_square = single_pos(move_code[-2:])
        
        for piece_pos in colored_piece_gen(self.board, KING, self.to_move):
            if king_moves(piece_pos, self.board, self.to_move) & target_square:
                valid_count += 1
                leaving_square = piece_pos
        
        if valid_count == 1:
            self.board = move_piece(self.board, leaving_square, target_square)
            self.remove_castling_rights(self.to_move)
            self.clear_ep_square()
            success = True
        
        return success
    
    def make_queen_move(self, move_code):
        success = False
        valid_count = 0
        target_square = single_pos(move_code[-2:])
        
        if len(move_code) == 4:
            filter_squares = get_filter(move_code[1])
        else:
            filter_squares = ALL_SQUARES
            
        for piece_pos in colored_piece_gen(self.board, QUEEN, self.to_move):
            if piece_pos & filter_squares:
                if queen_moves(piece_pos, self.board, self.to_move) & target_square:
                    valid_count += 1
                    leaving_square = piece_pos
        
        if valid_count == 1:
            self.board = move_piece(self.board, leaving_square, target_square)
            self.clear_ep_square()
            success = True
        
        return success
    
    def make_rook_move(self, move_code):
        success = False
        valid_count = 0
        target_square = single_pos(move_code[-2:])
        
        if len(move_code) == 4:
            filter_squares = get_filter(move_code[1])
        else:
            filter_squares = ALL_SQUARES
        
        for piece_pos in colored_piece_gen(self.board, ROOK, self.to_move):
            if piece_pos & filter_squares:
                if rook_moves(piece_pos, self.board, self.to_move) & target_square:
                    valid_count += 1
                    leaving_square = piece_pos
        
        if valid_count == 1:
            self.board = move_piece(self.board, leaving_square, target_square)
            self.clear_ep_square()
            if leaving_square == single_pos('a1'):
                self.castling_rights &= WHITE_KINGSIDE_CASTLE|BLACK_KINGSIDE_CASTLE|BLACK_QUEENSIDE_CASTLE
            if leaving_square == single_pos('h1'):
                self.castling_rights &= WHITE_QUEENSIDE_CASTLE|BLACK_KINGSIDE_CASTLE|BLACK_QUEENSIDE_CASTLE
            if leaving_square == single_pos('a8'):
                self.castling_rights &= WHITE_KINGSIDE_CASTLE|WHITE_QUEENSIDE_CASTLE|BLACK_KINGSIDE_CASTLE
            if leaving_square == single_pos('h8'):
                self.castling_rights &= WHITE_KINGSIDE_CASTLE|WHITE_QUEENSIDE_CASTLE|BLACK_QUEENSIDE_CASTLE
            success = True
        
        return success
    
    def make_bishop_move(self, move_code):
        success = False
        valid_count = 0
        target_square = single_pos(move_code[-2:])
        
        if len(move_code) == 4:
            filter_squares = get_filter(move_code[1])
        else:
            filter_squares = ALL_SQUARES
        
        for piece_pos in colored_piece_gen(self.board, BISHOP, self.to_move):
            if piece_pos & filter_squares:
                if bishop_moves(piece_pos, self.board, self.to_move) & target_square:
                    valid_count += 1
                    leaving_square = piece_pos
        
        if valid_count == 1:
            self.board = move_piece(self.board, leaving_square, target_square)
            self.clear_ep_square()
            success = True
        
        return success
    
    def make_knight_move(self, move_code):
        success = False
        valid_count = 0
        target_square = single_pos(move_code[-2:])
        
        if len(move_code) == 4:
            filter_squares = get_filter(move_code[1])
        else:
            filter_squares = ALL_SQUARES
        
        for piece_pos in colored_piece_gen(self.board, KNIGHT, self.to_move):
            if piece_pos & filter_squares:
                if knight_moves(piece_pos, self.board, self.to_move) & target_square:
                    valid_count += 1
                    leaving_square = piece_pos
        
        if valid_count == 1:
            self.board = move_piece(self.board, leaving_square, target_square)
            self.clear_ep_square()
            success = True
        
        return success
        
    def remove_castling_rights(self, color):
        if color == WHITE:
            self.castling_rights &= BLACK_KINGSIDE_CASTLE|BLACK_QUEENSIDE_CASTLE
        if color == BLACK:
            self.castling_rights &= WHITE_KINGSIDE_CASTLE|WHITE_QUEENSIDE_CASTLE

    def make_castle_kingside(self):
        if can_castle_kingside(self, self.to_move):
            self.board = castle_kingside(self.board, self.to_move)
            self.remove_castling_rights(self.to_move)
            return True
        return False

    def make_castle_queenside(self):
        if can_castle_queenside(self, self.to_move):
            self.board = castle_queenside(self.board, self.to_move)
            self.remove_castling_rights(self.to_move)
            return True
        return False
    
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
                    FEN_str += '{}'.format(piece_str(piece))
                    empty_sqrs = 0
            if empty_sqrs > 0:
                FEN_str += '{}'.format(empty_sqrs)
            FEN_str += '/'
        FEN_str = FEN_str[:-1] + ' '
        
        if self.to_move == WHITE:
            FEN_str += 'w '
        if self.to_move == BLACK:
            FEN_str += 'b '
            
        if self.castling_rights & WHITE_KINGSIDE_CASTLE:
            FEN_str += 'K'
        if self.castling_rights & WHITE_QUEENSIDE_CASTLE:
            FEN_str += 'Q'
        if self.castling_rights & BLACK_KINGSIDE_CASTLE:
            FEN_str += 'k'
        if self.castling_rights & BLACK_QUEENSIDE_CASTLE:
            FEN_str += 'q'
        if self.castling_rights == 0:
            FEN_str += '-'
        FEN_str += ' '
            
        if self.ep == 0:
            FEN_str += '-'
        else:
            FEN_str += encode_position(self.ep)
        
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
                    rank_pieces.append(piece_code(p))
            self.board.extend(rank_pieces)
        
        to_move_str = FEN_list[1].lower()
        if to_move_str == 'w':
            self.to_move = WHITE
        if to_move_str == 'b':
            self.to_move = BLACK
        
        castling_rights_str = FEN_list[2]
        self.castling_rights = 0
        if castling_rights_str.find('K') >= 0:
            self.castling_rights |= WHITE_KINGSIDE_CASTLE
        if castling_rights_str.find('Q') >= 0:
            self.castling_rights |= WHITE_QUEENSIDE_CASTLE
        if castling_rights_str.find('k') >= 0:
            self.castling_rights |= BLACK_KINGSIDE_CASTLE
        if castling_rights_str.find('q') >= 0:
            self.castling_rights |= BLACK_QUEENSIDE_CASTLE 
        
        ep_str = FEN_list[3]
        if ep_str == '-':
            self.ep = 0
        else:
            self.ep = single_pos(ep_str)
        
        self.halfmove_clock = int(FEN_list[4])
        self.fullmove_number = int(FEN_list[5])

# ==========================



def get_piece(board, bitboard):
    return board[get_index(bitboard)]
        
def get_index(bitboard):
    for i in range(64):
        if bitboard & (0b1 << i):
            return i

def parse_pos(position):
    fille = FILES.index(position[0].lower())
    rank = RANKS.index(position[1])
    return 8*rank + fille

def single_pos(position):
    return 0b1 << parse_pos(position)

def encode_position(bitboard):
    for i in range(64):
        if (bitboard >> i) & 0b1:
            fille = i%8
            rank = int(i/8)
            return '{}{}'.format(FILES[fille], RANKS[rank])

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

def piece_code(string):
    piece_codes = { 'K':WHITE|KING,
                    'Q':WHITE|QUEEN,
                    'R':WHITE|ROOK,
                    'B':WHITE|BISHOP,
                    'N':WHITE|KNIGHT,
                    'P':WHITE|PAWN,
                    'k':BLACK|KING,
                    'q':BLACK|QUEEN,
                    'r':BLACK|ROOK,
                    'b':BLACK|BISHOP,
                    'n':BLACK|KNIGHT,
                    'p':BLACK|PAWN }
    return piece_codes[string]
    
def print_board(board):
    print('')
    for i in range(len(RANKS)):
        rank_str = str(8-i) + ' '
        first = len(board) - 8*(i+1)
        for fille in range(len(FILES)):
            rank_str += '{} '.format(piece_str(board[first+fille]))
        print(rank_str)
    print('  a b c d e f g h')

def print_rotated_board(board):
    r_board = rotate_board(board)
    print('')
    for i in range(len(RANKS)):
        rank_str = str(i+1) + ' '
        first = len(r_board) - 8*(i+1)
        for fille in range(len(FILES)):
            rank_str += '{} '.format(piece_str(r_board[first+fille]))
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

def move_piece(board, leaving_position, arriving_position):
    new_board = deepcopy(board)
    new_board[get_index(arriving_position)] = new_board[get_index(leaving_position)] 
    new_board[get_index(leaving_position)] = EMPTY
    return new_board

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
    return pawn_pushes(moving_piece, game.board, color) | pawn_simple_captures(moving_piece, game.board, color) | pawn_ep_captures(moving_piece, game, color)

def pawn_pushes(moving_piece, board, color):
    return pawn_simple_pushes(moving_piece, board, color) | pawn_double_pushes(moving_piece, board, color)

def pawn_simple_captures(attacking_piece, board, color):
    return pawn_attacks(attacking_piece, board, color) & get_colored_pieces(board, opposing_color(color))

def pawn_ep_captures(attacking_piece, game, color):
    if color == WHITE:
        ep_squares = game.ep & RANK_6
    if color == BLACK:
        ep_squares = game.ep & RANK_3
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

def can_castle_kingside(game, color):
    if color == WHITE:
        return (game.castling_rights & WHITE_KINGSIDE_CASTLE) and \
                game.board[parse_pos('f1')] == EMPTY and \
                game.board[parse_pos('g1')] == EMPTY and \
                (not is_attacked(single_pos('e1'), game.board, opposing_color(color))) and \
                (not is_attacked(single_pos('f1'), game.board, opposing_color(color))) and \
                (not is_attacked(single_pos('g1'), game.board, opposing_color(color)))
    if color == BLACK:
        return (game.castling_rights & BLACK_KINGSIDE_CASTLE) and \
                game.board[parse_pos('f8')] == EMPTY and \
                game.board[parse_pos('g8')] == EMPTY and \
                (not is_attacked(single_pos('e8'), game.board, opposing_color(color))) and \
                (not is_attacked(single_pos('f8'), game.board, opposing_color(color))) and \
                (not is_attacked(single_pos('g8'), game.board, opposing_color(color)))

def castle_kingside(board, color):
    return_board = deepcopy(board)
    if color == WHITE:
        return_board[parse_pos('e1')] = EMPTY
        return_board[parse_pos('f1')] = WHITE|ROOK
        return_board[parse_pos('g1')] = WHITE|KING
        return_board[parse_pos('h1')] = EMPTY
    if color == BLACK:
        return_board[parse_pos('e8')] = EMPTY
        return_board[parse_pos('f8')] = BLACK|ROOK
        return_board[parse_pos('g8')] = BLACK|KING
        return_board[parse_pos('h8')] = EMPTY
    return return_board

def can_castle_queenside(game, color):
    if color == WHITE:
        return (game.castling_rights & WHITE_QUEENSIDE_CASTLE) and \
                game.board[parse_pos('b1')] == EMPTY and \
                game.board[parse_pos('c1')] == EMPTY and \
                game.board[parse_pos('d1')] == EMPTY and \
                (not is_attacked(single_pos('c1'), game.board, opposing_color(color))) and \
                (not is_attacked(single_pos('d1'), game.board, opposing_color(color))) and \
                (not is_attacked(single_pos('e1'), game.board, opposing_color(color)))
    if color == BLACK:
        return (game.castling_rights & BLACK_QUEENSIDE_CASTLE) and \
                game.board[parse_pos('b8')] == EMPTY and \
                game.board[parse_pos('c8')] == EMPTY and \
                game.board[parse_pos('d8')] == EMPTY and \
                (not is_attacked(single_pos('c8'), game.board, opposing_color(color))) and \
                (not is_attacked(single_pos('d8'), game.board, opposing_color(color))) and \
                (not is_attacked(single_pos('e8'), game.board, opposing_color(color)))

def castle_queenside(board, color):
    return_board = deepcopy(board)
    if color == WHITE:
        return_board[parse_pos('e1')] = EMPTY
        return_board[parse_pos('d1')] = WHITE|ROOK
        return_board[parse_pos('c1')] = WHITE|KING
        return_board[parse_pos('a1')] = EMPTY
    if color == BLACK:
        return_board[parse_pos('e8')] = EMPTY
        return_board[parse_pos('d8')] = BLACK|ROOK
        return_board[parse_pos('c8')] = BLACK|KING
        return_board[parse_pos('a8')] = EMPTY
    return return_board

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

def pseudo_legal_moves(game, color): # FIXME: add castling?
    return pawn_moves(get_pawns(game.board, color), game, color)     | \
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
    return material/100


def material_balance(board):
    return material_sum(board, WHITE) - material_sum(board, BLACK)
    
    
    
    
test_board = [ WHITE|ROOK, WHITE|KNIGHT, WHITE|BISHOP, WHITE|QUEEN, EMPTY,       WHITE|BISHOP, WHITE|KNIGHT, WHITE|ROOK,
               WHITE|PAWN, WHITE|PAWN,   WHITE|PAWN,   WHITE|PAWN,  WHITE|PAWN,  WHITE|PAWN,   EMPTY,        EMPTY,
               EMPTY,      BLACK|BISHOP, EMPTY,        EMPTY,       WHITE|KING,  EMPTY,        WHITE|PAWN,   EMPTY,
               EMPTY,      BLACK|KNIGHT, EMPTY,        EMPTY,       EMPTY,       EMPTY,        EMPTY,        WHITE|PAWN,
               EMPTY,      EMPTY,        EMPTY,        EMPTY,       EMPTY,       EMPTY,        EMPTY,        EMPTY,
               EMPTY,      EMPTY,        EMPTY,        BLACK|PAWN,  BLACK|QUEEN, BLACK|PAWN,   EMPTY,        EMPTY,
               BLACK|PAWN, BLACK|PAWN,   BLACK|PAWN,   EMPTY,       EMPTY,       EMPTY,        BLACK|PAWN,   BLACK|PAWN,
               BLACK|ROOK, EMPTY,        EMPTY,        EMPTY,       BLACK|KING,  BLACK|BISHOP, BLACK|KNIGHT, BLACK|ROOK ]

# print_board(test_board)
# print_bitboard(empty_squares(test_board))
# print_bitboard(occupied_squares(test_board))
# print_bitboard(pawn_attacks(get_pawns(test_board, WHITE), test_board, WHITE))
# print_bitboard(pawn_double_attacks(get_pawns(test_board, WHITE), test_board, WHITE))
# print_bitboard(pawn_captures(get_pawns(test_board, WHITE), test_board, WHITE))
# print_bitboard(king_moves(get_king(test_board, BLACK), test_board, BLACK) | pawn_moves(get_pawns(test_board, WHITE), test_board, WHITE))
# print_bitboard(knight_moves(get_knights(test_board, BLACK), test_board, BLACK))
# print_bitboard(get_rooks(test_board, WHITE) | get_bishops(test_board, WHITE))
# print_bitboard(rook_rays(get_queen(test_board, BLACK)))
# print_bitboard(queen_rays(get_queen(test_board, WHITE)))
# print_bitboard(bishop_rays(single_pos('c5')))
# print_bitboard(rook_rays(single_pos('f2')))
# print_bitboard(queen_rays(single_pos('h4')))
# print_bitboard(msb(ALL_SQUARES))
# print_bitboard(lsb(ALL_SQUARES))
# print_bitboard(rook_moves(get_queen(test_board, WHITE), test_board, WHITE))
# print_bitboard(bishop_moves(get_bishops(test_board, WHITE)&black_pieces(test_board), test_board, BLACK))
# print_bitboard(queen_moves(get_queen(test_board, WHITE)&black_pieces(test_board), test_board, BLACK))
# print_bitboard(queen_moves(get_queen(test_board, WHITE), test_board, BLACK))
# print_bitboard(king_moves(get_queen(test_board, WHITE), test_board, WHITE))
# print_bitboard(pseudo_legal_moves(test_board, WHITE)&get_colored_pieces(test_board, BLACK))
# print_bitboard(pseudo_legal_moves(test_board, BLACK)&get_colored_pieces(test_board, WHITE))
# print_bitboard(knight_fill(single_pos('a1'), 2))
# print(knight_distance('a1', 'h8'))
# print_bitboard(pseudo_legal_moves(test_board, BLACK))
# print(is_check(test_board, WHITE))
# print(is_check(test_board, BLACK))
# print_bitboard(pawn_moves(single_pos('d2'), test_board, WHITE))
# print_bitboard(pseudo_legal_moves(test_board, WHITE)&get_colored_pieces(test_board, BLACK))
# print_bitboard(pseudo_legal_moves(test_board, BLACK)&get_colored_pieces(test_board, WHITE))
# print(count_attacks(single_pos('B3'), test_board, WHITE))
# print(count_attacks(single_pos('B3'), test_board, BLACK))
# print(bin(FULL_CASTLING_RIGHTS))
# game = Game('r3kbnr/ppp3pp/3pqp2/8/1n5P/1b2K1P1/PPPPPP2/RNBQ1BNR b KQkq - 0 1')
# print(can_castle_kingside(game, WHITE))
# print(can_castle_queenside(game, WHITE))
# print(can_castle_kingside(game, BLACK))
# print(can_castle_queenside(game, BLACK))
# print(bin(game.castling_rights))
# print(game.make_castle_queenside(WHITE))
# print(game.make_castle_queenside(BLACK))
# print(bin(game.castling_rights))
# print_board(game.board)
# print_board(move_piece(test_board, 'g1', 'f3'))
# print_board(move_piece(test_board, 'e2', 'f3'))
# print(game.to_FEN())
# game = Game('1r1q2k1/B4p1p/4r1p1/3n2P1/b4P2/7P/8/3R2K1 w - - 1 28')
# print_board(game.board)
# print_rotated_board(game.board)
# print(game.to_FEN())
# print(material_sum(game.board, WHITE))
# print(material_sum(game.board, BLACK))
# print(material_balance(game.board))
# print(piece_str(get_piece(game.board, single_pos('a7'))))
# game = Game('1r1q2k1/B4p2/4r1p1/3n2Pp/b4P2/7P/8/3R2K1 w KQ h6 1 28')
# print_board(game.board)
# print(game.to_FEN())
# print(game.make_move('Kf2'))
# print_board(game.board)
# print(game.make_move('Kg7'))
# print_board(game.board)
# game = Game('1r1q2k1/B4p2/4r1p1/3n2Pp/b4P2/7P/8/3R2K1 b - h6 1 28')
# print_board(game.board)
# game.make_move('Ne3')
# print_board(game.board)

game = Game('rnbqkbnr/1pppppp1/8/8/8/Q6Q/1PPPPPP1/RNBQKBNR w KQkq - 0 1')
while True:
    print_board(game.board)
    print(game.to_FEN())
    while not game.make_move(input()):
        print('Invalid move!')