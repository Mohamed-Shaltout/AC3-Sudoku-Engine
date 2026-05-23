def is_solved(board: list[int]) -> bool:
    """Check if the given Sudoku board is completely and correctly solved."""
    if 0 in board:
        return False
    
    for i in range(9):
        # Check row
        row = board[i * 9:(i + 1) * 9]
        if len(set(row)) != 9:  
            return False
        
        # Check column
        col = [board[j * 9 + i] for j in range(9)]
        if len(set(col)) != 9: 
            return False
        
        # Check 3x3 box
        box_row, box_col = (i // 3) * 3, (i % 3) * 3
        box = [board[box_row * 9 + box_col], board[box_row * 9 + box_col + 1], board[box_row * 9 + box_col + 2],
               board[(box_row + 1) * 9 + box_col], board[(box_row + 1) * 9 + box_col + 1], board[(box_row + 1) * 9 + box_col + 2],
               board[(box_row + 2) * 9 + box_col], board[(box_row + 2) * 9 + box_col + 1], board[(box_row + 2) * 9 + box_col + 2]]
        if len(set(box)) != 9:  
            return False
    
    return True

def valid(board: list[int], num: int, pos: tuple[int, int]) -> bool:
    """Check if placing `num` at `pos` (row, col) is valid in the current board."""
    row, col = pos
    # Check row
    for i in range(9):
        if board[row * 9 + i] == num and col != i:
            return False
    # Check col
    for i in range(9):
        if board[i * 9 + col] == num and row != i:
            return False
    # Check box
    box_row, box_col = row // 3 * 3, col // 3 * 3
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i * 9 + j] == num and (i, j) != (row, col):
                return False
    return True

def print_board(board: list[int]):
    """Print the board in a standard format to console."""
    for i in range(9):
        row = board[i * 9:(i + 1) * 9]
        print(" ".join(str(x) if x != 0 else "." for x in row))
    print("\n")

def neighbors(cell: tuple[int, int]) -> set[tuple[int, int]]:
    """Get all neighbor cells for a given cell (row, col)."""
    row, col = cell
    neighbors_set = set()
    neighbors_set.update((row, c) for c in range(9) if c != col)
    neighbors_set.update((r, col) for r in range(9) if r != row)
    box_row, box_col = row // 3 * 3, col // 3 * 3
    neighbors_set.update((r, c) for r in range(box_row, box_row + 3) for c in range(box_col, box_col + 3) if (r, c) != cell)
    return neighbors_set

NEIGHBORS_CACHE = {cell: neighbors(cell) for cell in [(r, c) for r in range(9) for c in range(9)]}
