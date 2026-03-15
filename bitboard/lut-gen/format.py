def format_hex_array(matrix: list[list[int]]):
    """
    Converts an 8x8 matrix into a Python-formatted string 
    with zero-padded 32-bit hex values.
    """
    lines = ["hex_array = ["]
    
    for row in matrix:
        # Format: 0x followed by 16 hex digits, e.g., 0x000000ff
        formatted_row = [f"0x{val:016x}" for val in row]
        # Join values with commas and indent the row
        lines.append(f"    [{', '.join(formatted_row)}],")
        
    lines.append("]")
    return "\n".join(lines)