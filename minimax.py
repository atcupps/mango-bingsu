from bulletchess import Board, Move, ROOK, KNIGHT, BISHOP, KING, QUEEN, PAWN
from typing import Callable, Tuple, Optional
from zobrist import get_zobrist_hash

PIECE_VALUES = {
    ROOK: 5.0,
    KNIGHT: 3.0,
    BISHOP: 3.0,
    KING: 100.0,
    QUEEN: 9.0,
    PAWN: 1.0
}

# Transposition Table Constants
EXACT = 0
LOWERBOUND = 1
UPPERBOUND = 2

# TRANSPOSITION_TABLE[hash] = {'depth': d, 'score': s, 'best_move': m, 'flag': f}
TRANSPOSITION_TABLE = {}

def score_move(board: Board, move: Move, tt_best_move: Optional[Move] = None) -> float:
    """
    Assigns a score to a move for ordering purposes.
    Higher scores indicate more promising moves.
    """
    if tt_best_move and move == tt_best_move:
        return 10000.0  # Search the best move from a previous search first

    score = 0.0
    
    # Heuristic: Captures
    if move.is_capture(board):
        captured_piece_type = None
        for pt in [QUEEN, ROOK, BISHOP, KNIGHT, PAWN, KING]:
            if board[pt] & move.destination:
                captured_piece_type = pt
                break
        
        moving_piece_type = None
        for pt in [QUEEN, ROOK, BISHOP, KNIGHT, PAWN, KING]:
            if board[pt] & move.origin:
                moving_piece_type = pt
                break
        
        if captured_piece_type is not None:
            score += 10 * PIECE_VALUES[captured_piece_type]
        if moving_piece_type is not None:
            score -= PIECE_VALUES[moving_piece_type]
            
    # Heuristic: Promotions
    if move.is_promotion() and move.promotion != None:
        score += PIECE_VALUES[move.promotion]

    # Heuristic: Castling
    if move.is_castling(board):
        score += 1.0

    return score

def minimax(current_position: Board, depth: int, is_white_turn: bool, evaluator: Callable[[Board], float], alpha: float, beta: float) -> Tuple[float, Optional[Move]]:
    """
    Finds the best move and its evaluation using minimax with alpha-beta pruning, 
    move ordering, and a transposition table.
    """
    alpha_orig = alpha
    h = get_zobrist_hash(current_position)
    
    # Transposition Table Lookup
    tt_best_move = None
    if h in TRANSPOSITION_TABLE:
        entry = TRANSPOSITION_TABLE[h]
        tt_best_move = entry['best_move']
        if entry['depth'] >= depth:
            if entry['flag'] == EXACT:
                return entry['score'], entry['best_move']
            elif entry['flag'] == LOWERBOUND:
                alpha = max(alpha, entry['score'])
            elif entry['flag'] == UPPERBOUND:
                beta = min(beta, entry['score'])
            
            if alpha >= beta:
                return entry['score'], entry['best_move']

    legal_moves = current_position.legal_moves()
    if depth == 0 or not legal_moves:
        score = evaluator(current_position)
        return score, None

    # Move Ordering
    legal_moves.sort(key=lambda m: score_move(current_position, m, tt_best_move), reverse=True)

    best_move = None
    if is_white_turn:
        max_eval = -float('inf')
        for move in legal_moves:
            current_position.apply(move)
            eval, _ = minimax(current_position, depth - 1, False, evaluator, alpha, beta)
            current_position.undo()
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        
        # Store in Transposition Table
        tt_entry = {'depth': depth, 'score': max_eval, 'best_move': best_move}
        if max_eval <= alpha_orig:
            tt_entry['flag'] = UPPERBOUND
        elif max_eval >= beta:
            tt_entry['flag'] = LOWERBOUND
        else:
            tt_entry['flag'] = EXACT
        TRANSPOSITION_TABLE[h] = tt_entry
        
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in legal_moves:
            current_position.apply(move)
            eval, _ = minimax(current_position, depth - 1, True, evaluator, alpha, beta)
            current_position.undo()
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        
        # Store in Transposition Table
        tt_entry = {'depth': depth, 'score': min_eval, 'best_move': best_move}
        if min_eval <= alpha_orig:
            tt_entry['flag'] = UPPERBOUND
        elif min_eval >= beta:
            tt_entry['flag'] = LOWERBOUND
        else:
            tt_entry['flag'] = EXACT
        TRANSPOSITION_TABLE[h] = tt_entry
        
        return min_eval, best_move
