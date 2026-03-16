import random
from bulletchess import Board, WHITE, BLACK, ROOK, KNIGHT, BISHOP, KING, QUEEN, PAWN

# Zobrist Hashing Constants
PIECE_TYPES = [PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING]
COLORS = [WHITE, BLACK]
SQUARES = range(64)

# Seed the random number generator for reproducibility (optional but common)
random.seed(42)

# ZOBRIST_TABLE[square][piece_type][color]
ZOBRIST_TABLE = [[[random.getrandbits(64) for _ in COLORS] for _ in PIECE_TYPES] for _ in SQUARES]

# ZOBRIST_TURN
ZOBRIST_TURN = random.getrandbits(64)

# ZOBRIST_CASTLING[castling_rights_string]
# Since castling rights is a string, we can hash the string or use its components.
# A simpler way is to pre-generate some random numbers for each possible right.
# For simplicity, we can just hash the string itself if it's small,
# but for a true Zobrist implementation, we'd use fixed bits.
ZOBRIST_CASTLING = {
    'K': random.getrandbits(64),
    'Q': random.getrandbits(64),
    'k': random.getrandbits(64),
    'q': random.getrandbits(64)
}

# ZOBRIST_EP[file]
ZOBRIST_EP = [random.getrandbits(64) for _ in range(8)]

def get_zobrist_hash(board: Board) -> int:
    """
    Computes the Zobrist hash for a given board from scratch.
    """
    h = 0
    
    # Pieces
    for square_idx in SQUARES:
        square_bit = 1 << square_idx
        for pt_idx, pt in enumerate(PIECE_TYPES):
            if int(board[pt]) & square_bit:
                color_idx = 0 if int(board[WHITE]) & square_bit else 1
                h ^= ZOBRIST_TABLE[square_idx][pt_idx][color_idx]
    
    # Turn
    if board.turn == BLACK:
        h ^= ZOBRIST_TURN
        
    # Castling Rights
    rights = board.castling_rights
    for char, bits in ZOBRIST_CASTLING.items():
        if char in str(rights):
            h ^= bits
            
    # En Passant
    ep_square = board.en_passant_square
    if ep_square is not None:
        # Assuming en_passant_square is a Square object/int that can give us the file
        # If it's an int, we can get the file with % 8
        file = int(ep_square.bb()) % 8
        h ^= ZOBRIST_EP[file]
        
    return h
