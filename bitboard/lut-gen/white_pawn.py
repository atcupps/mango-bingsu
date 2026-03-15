from bitmoves import *
from format import format_hex_array

# Generates a 8x8 array of boolean integers representing pseudo-legal 
# non-capture moves for a white pawn on a given rank and file.
def moves_arr_for_position(rank: int, file: int) -> list[list[int]]:
    board = [[0 for _ in range(8)] for _ in range(8)]
    
    # Pawns cannot be on the first or last rank.
    if rank <= 0 or rank >= 7:
        return board
    
    # Single push
    if rank + 1 < 8:
        board[rank + 1][file] = 1
        
    # Double push (only from the starting rank 1)
    if rank == 1:
        board[rank + 2][file] = 1
        
    return board

# Generates bitmove integer for any given rank and file
def bitmoves_for_position(rank: int, file: int) -> int:
    return to_bits(flatten(moves_arr_for_position(rank, file)))

# Generates a 8x8 array of bitmoves and prints
bitmoves = []
for r in range(8):
    bitmoves.append([])
    for f in range(8):
        bitmoves[r].append(bitmoves_for_position(r, f))
print(format_hex_array(bitmoves))