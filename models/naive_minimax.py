from bulletchess import Board, Move, WHITE
from minimax import minimax, TRANSPOSITION_TABLE
from naive_evaluator import naive_evaluator

SEARCH_DEPTH = 4

def naive_minimax(board: Board) -> Move | None:
    """
    Uses minimax with iterative deepening and a naive evaluator.
    Iterative deepening populates the transposition table to make deeper searches faster.
    """
    # Clear the table for a fresh root-level search
    TRANSPOSITION_TABLE.clear()
    
    is_white_turn = (board.turn == WHITE)
    best_move = None
    
    # Iterative Deepening
    for current_depth in range(1, SEARCH_DEPTH + 1):
        _, current_best_move = minimax(
            current_position=board,
            depth=current_depth,
            is_white_turn=is_white_turn,
            evaluator=naive_evaluator,
            alpha=-float('inf'),
            beta=float('inf')
        )
        if current_best_move:
            best_move = current_best_move
            
    return best_move
