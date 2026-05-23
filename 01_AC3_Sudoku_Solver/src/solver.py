from collections import deque
from src.utils import NEIGHBORS_CACHE, valid

def forward_check(domains: dict, cell: tuple[int, int], value: int):
    """Apply forward checking to update domains of neighbor cells."""
    updates = []
    for neighbor in NEIGHBORS_CACHE[cell]:
        if value in domains[neighbor]:
            domains[neighbor].remove(value)
            updates.append((neighbor, value))
            if not domains[neighbor]:  
                return False, updates
    return True, updates

def restore_domains(domains: dict, updates: list):
    """Restore domains from updates after a backtrack."""
    for cell, value in updates:
        domains[cell].add(value)

def arc_consistency(board: list[int], update_gui_tree=None):
    """AC-3 algorithm implementation to enforce arc consistency."""
    domains = {(r, c): set(range(1, 10)) if board[r * 9 + c] == 0 else {board[r * 9 + c]} for r in range(9) for c in range(9)}
    arcs = deque([(cell, neighbor) for cell in domains for neighbor in NEIGHBORS_CACHE[cell]])
    arc_domains = {}
    
    while arcs:
        cell, neighbor = arcs.popleft()
        if revise(domains, cell, neighbor):
            arc_domains[(cell, neighbor)] = (domains[cell].copy(), domains[neighbor].copy())
            if not domains[cell]:
                return None
            for other_neighbor in NEIGHBORS_CACHE[cell]:
                if other_neighbor != neighbor:
                    arcs.append((other_neighbor, cell))
    
    if update_gui_tree:
        update_gui_tree(arc_domains)
        
    return domains

def revise(domains: dict, cell: tuple[int, int], neighbor: tuple[int, int]) -> bool:
    """Revise domain of cell given neighbor's domain."""
    revised = False
    for value in set(domains[cell]):
        if value in domains[neighbor] and len(domains[neighbor]) == 1:
            domains[cell].remove(value)
            revised = True
    return revised

def solve_with_ac3(board: list[int], update_gui=lambda *args: None, update_gui_tree=lambda *args: None) -> bool:
    """Solves the Sudoku using AC-3 followed by Backtracking with Forward Checking."""
    domains = arc_consistency(board, update_gui_tree)
    if domains is None:
        return False
    return backtracking_with_domains(board, domains, update_gui)

def backtracking_with_domains(board: list[int], domains: dict, update_gui) -> bool:
    """Backtracking algorithm to find a solution."""
    empty = find_empty(board, domains)
    if not empty:
        return True

    row, col = empty
    cell = (row, col)
    possible_values = sorted(domains[cell], key=lambda v: count_constraints(board, row, col, v, domains))

    for value in possible_values:
        if valid(board, value, cell):
            board[row * 9 + col] = value
            update_gui(board, row, col, value, "forward")
            
            # Apply forward checking
            success, updates = forward_check(domains, cell, value)
            if success:
                if backtracking_with_domains(board, domains, update_gui):
                    return True

            restore_domains(domains, updates)
            board[row * 9 + col] = 0
            update_gui(board, row, col, 0, "backward")

    return False

def count_constraints(board: list[int], row: int, col: int, value: int, domains: dict) -> int:
    """Count constraints introduced by assigning a value (Degree heuristic)."""
    count = 0
    for r, c in NEIGHBORS_CACHE[(row, col)]:
        if board[r * 9 + c] == 0 and value in domains[(r, c)]:
            count += 1
    return count

def find_empty(board: list[int], domains: dict):
    """Find empty cell with the smallest domain (MRV heuristic)."""
    min_domain_size = float('inf')
    best_cell = None

    for i in range(len(board)):
        if board[i] == 0:  
            row, col = i // 9, i % 9
            domain_size = len(domains[(row, col)])
            if domain_size < min_domain_size:
                min_domain_size = domain_size
                best_cell = (row, col)
    
    return best_cell
