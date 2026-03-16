from bulletchess import Board, Move
from typing import Callable, Tuple, Optional

def find_best_move(current_position: Board, depth: int, is_white_turn: bool, evaluator: Callable[[Board], float], alpha: float, beta: float) -> Tuple[float, Optional[Move]]:
    """
    Finds the best move and its evaluation using minimax with alpha-beta pruning.

    **Params:**
    - `current_position`: A `Board` object representing the current board position.
    - `depth`: The desired maximum depth to search from the current position.
    - `is_white_turn`: A boolean value representing whether or not the current board
    position is white or black's move
    - `evaluator`: A callable function to numerically evaluate a board position.
    The function should take a `Board` object and return a `float` representing an evaluation
    of that board position, where more strongly positive numbers indicate a stronger position for
    white, and more strongly negative numbers indicate a stronger position for black.
    - `alpha`: The current alpha value for pruning (best value for white).
    - `beta`: The current beta value for pruning (best value for black).

    **Returns:**
    - A tuple `(score, move)` where `score` is the evaluation of the best position
    found, and `move` is the `Move` object that leads to that position.
    """
    legal_moves = current_position.legal_moves()
    if depth == 0 or not legal_moves:
        return evaluator(current_position), None

    best_move = None
    if is_white_turn:
        max_eval = -float('inf')
        for move in legal_moves:
            current_position.apply(move)
            eval, _ = find_best_move(current_position, depth - 1, False, evaluator, alpha, beta)
            current_position.undo()
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in legal_moves:
            current_position.apply(move)
            eval, _ = find_best_move(current_position, depth - 1, True, evaluator, alpha, beta)
            current_position.undo()
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move
