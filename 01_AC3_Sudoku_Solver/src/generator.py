import random

def generate_random_sudoku(difficulty: str) -> list[int]:
    """Generates a random solvable Sudoku board of a given difficulty."""
    def is_valid(board, num, row, col):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True

    def solve(board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    random.shuffle(numbers)
                    for num in numbers:
                        if is_valid(board, num, row, col):
                            board[row][col] = num
                            if solve(board):
                                return True
                            board[row][col] = 0
                    return False
        return True

    def remove_numbers(board, clues):
        count = 81 - clues
        while count > 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if board[row][col] != 0:
                board[row][col] = 0
                count -= 1

    clues_dict = {
        "easy": 35,
        "medium": 31,
        "hard": random.randint(22, 27),
        "expert": 17
    }

    if difficulty.lower() not in clues_dict:
        raise ValueError("Invalid difficulty level. Choose from 'easy', 'medium', 'hard', or 'expert'.")

    clues = clues_dict[difficulty.lower()]

    board = [[0 for _ in range(9)] for _ in range(9)]
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    solve(board)
    remove_numbers(board, clues)

    return [cell for row in board for cell in row]
