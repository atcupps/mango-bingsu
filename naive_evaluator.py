from bulletchess import Board, WHITE, BLACK, ROOK, KNIGHT, BISHOP, KING, QUEEN, PAWN, Bitboard

piece_values = {
    ROOK: 5.0,
    KNIGHT: 3.0,
    BISHOP: 3.0,
    KING: 100.0,
    QUEEN: 9.0,
    PAWN: 1.0
}

def num_pieces(locations: Bitboard) -> int:
    """
    Given a bitboard containing 1s for the locations of a given piece,
    returns the number of that piece on the board.
    """
    return int(locations).bit_count()

def evaluate_score(board: Board, side_pieces: Bitboard) -> float:
    score = 0.0
    for piece_type in [ROOK, KNIGHT, BISHOP, KING, QUEEN, PAWN]:
        score += piece_values[piece_type] * num_pieces(side_pieces & board[piece_type])
    return score

def naive_evaluator(board: Board) -> float:
    white_score = evaluate_score(board, board[WHITE])
    black_score = evaluate_score(board, board[BLACK])
    return white_score - black_score