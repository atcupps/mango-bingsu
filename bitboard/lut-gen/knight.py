from bitmoves import *
from format import format_hex_array

# Generates a 8x8 array of boolean integers representing pseudo-legal moves
# for a knight on a given rank and file.
def moves_arr_for_position(rank: int, file: int) -> list[list[int]]:
    board = [[0 for _ in range(8)] for _ in range(8)]
    knight_moves = [
        (1, 2), (1, -2), (-1, 2), (-1, -2),
        (2, 1), (2, -1), (-2, 1), (-2, -1)
    ]
    for dr, df in knight_moves:
        r, f = rank + dr, file + df
        if 0 <= r < 8 and 0 <= f < 8:
            board[r][f] = 1
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
