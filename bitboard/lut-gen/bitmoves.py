# Takes in a 8x8 list of 1s and 0s and flattens it to
# a single list of length 64. For any given rank r and file f,
# its value lies at 8*r+f.
def flatten(moves: list[list[int]]) -> list[int]:
    result = []
    for i in range(8):
        for j in range(8):
            result.append(moves[i][j])
    return result

# Takes in a list of length 64 of 1s and 0s (in int form)
# and converts it to a single 64-bit integer.
def to_bits(flattened: list[int]) -> int:
    result = 0
    for i, b in enumerate(flattened):
        if b:
            result |= (1 << i)
    return result

# Takes in a list of length 64 and un-flattens it to a
# list of length 8 of lists of length 8.
def unflatten(flattened: list[int]) -> list[list[int]]:
    result = []
    for i in range(0, 64, 8):
        result.append(flattened[i:i+8])
    return result

# Takes in a 64-bit integer and returns a list of 64
# ints (either 0 or 1).
def from_bits(bits: int) -> list[int]:
    result = []
    for i in range(64):
        result.append((bits >> i) & 1)
    return result
