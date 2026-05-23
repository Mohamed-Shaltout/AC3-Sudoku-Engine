import tkinter as tk
from tkinter import messagebox, ttk
import time
from src.solver import solve_with_ac3
from src.generator import generate_random_sudoku
from src.utils import is_solved, valid

def show_arc_tree_gui(root, arcs):
    tree_window = tk.Toplevel(root)
    tree_window.title("Arc Consistency Tree")
    
    tree = ttk.Treeview(tree_window, columns=("Arc", "Domains"), show="headings")
    tree.heading("Arc", text="Arc")
    tree.heading("Domains", text="Domains")
    
    for arc, domain in arcs.items():
        tree.insert("", "end", values=(str(arc), str(domain)))
    
    tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

def create_gui(board, mode):
    root = tk.Tk()
    root.title("Sudoku Solver")

    def validate_input(value):
        return value.isdigit() and 1 <= int(value) <= 9 or value == ""

    validate_cmd = root.register(validate_input)

    grid_frame = tk.Frame(root, bg="#333", bd=2)
    grid_frame.grid(row=0, column=0, columnspan=9, padx=20, pady=20)

    # Column Labels
    for j in range(9):
        lbl = tk.Label(grid_frame, text=str(j+1), font=("Arial", 14, "bold"), bg="#333", fg="white")
        lbl.grid(row=0, column=j+1, pady=2)

    row_labels = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]

    cells = []
    for i in range(9):
        row = []
        
        # Row Label
        lbl = tk.Label(grid_frame, text=row_labels[i], font=("Arial", 14, "bold"), bg="#333", fg="white")
        lbl.grid(row=i+1, column=0, padx=5)
        
        for j in range(9):
            padx = (1, 1)
            pady = (1, 1)
            if j % 3 == 0 and j != 0:
                padx = (4, 1)
            if i % 3 == 0 and i != 0:
                pady = (4, 1)

            entry = tk.Entry(
                grid_frame, width=4, font=("Arial", 18), justify="center", borderwidth=0, relief="solid",
                validate="key", validatecommand=(validate_cmd, "%P")
            )
            entry.grid(row=i+1, column=j+1, padx=padx, pady=pady, ipady=5)

            if mode == "interactive":
                entry.bind("<Return>", lambda e, r=i, c=j: check_interactive_input(r, c))

            row.append(entry)
        cells.append(row)

    def initialize_gui(board_data):
        for i in range(9):
            for j in range(9):
                value = board_data[i * 9 + j]
                cells[i][j].delete(0, tk.END)
                cells[i][j].config(bg="white", state="normal")
                if value != 0:
                    cells[i][j].insert(0, str(value))
                    if mode == "interactive":
                        cells[i][j].config(state="disabled", disabledforeground="black")

    def get_board():
        return [int(cell.get()) if cell.get().isdigit() else 0 for row in cells for cell in row]

    def check_interactive_input(row, col):
        value = cells[row][col].get()
        if value.isdigit():
            num = int(value)
            current_board = get_board()
            # Temporarily clear the cell to check validity of placing `num`
            current_board[row * 9 + col] = 0
            if valid(current_board, num, (row, col)):
                cells[row][col].config(bg="lightgreen")
            else:
                messagebox.showerror("Invalid Entry", f"Number {value} violates Sudoku constraints!")
                cells[row][col].delete(0, tk.END)
                cells[row][col].config(bg="pink")
        else:
            cells[row][col].config(bg="white")

        current_board = get_board()
        if is_solved(current_board):
            messagebox.showinfo("Puzzle Solved!", "Congratulations! You have solved the puzzle.")
            for r in cells:
                for c in r:
                    c.config(state="disabled")  

    def update_gui(current_board, row, col, value, action):
        bg_color = "lightgreen" if action == "forward" else "pink"
        cells[row][col].delete(0, tk.END)
        if value != 0:
            cells[row][col].insert(0, str(value))
        cells[row][col].config(bg=bg_color)
        root.update_idletasks()
        root.update()

    def update_gui_tree(arcs):
        show_arc_tree_gui(root, arcs)

    def start_solver():
        timer_label = tk.Label(root, text="Time: 0s", font=("Arial", 14), bg="lightblue")
        timer_label.grid(row=2, column=0, columnspan=9, pady=10)
        start_time = time.time()
        current_board = get_board()
        
        # Validate current board first
        for r in range(9):
            for c in range(9):
                val = current_board[r * 9 + c]
                if val != 0:
                    current_board[r * 9 + c] = 0
                    if not valid(current_board, val, (r, c)):
                        messagebox.showerror("Invalid Board", "The current board is invalid. Please fix conflicts.")
                        return
                    current_board[r * 9 + c] = val
                    
        if solve_with_ac3(current_board, update_gui, update_gui_tree):
            end_time = time.time()
            elapsed_time = end_time - start_time
            timer_label.config(text=f"Time: {elapsed_time:.2f}s")
            messagebox.showinfo("Sudoku Solver", f"Sudoku solved successfully in {elapsed_time:.2f} seconds!")
        else:
            messagebox.showerror("Sudoku Solver", "The Sudoku puzzle is unsolvable!")

    def restart_game():
        initialize_gui(board)

    if mode == "solve":
        solve_button = tk.Button(root, text="Solve", command=start_solver, font=("Arial", 14))
        solve_button.grid(row=1, column=0, columnspan=4, pady=10)

    tk.Button(root, text="Restart", command=restart_game, font=("Arial", 14)).grid(row=1, column=4, columnspan=5, pady=10)

    initialize_gui(board)
    root.mainloop()

def mode_selection_gui():
    root = tk.Tk()
    root.title("Select Mode")

    window_width = 400
    window_height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = (screen_height // 2) - (window_height // 2)
    position_right = (screen_width // 2) - (window_width // 2)
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
    root.resizable(False, False)

    frame = tk.Frame(root, bg="lightblue", padx=20, pady=20)
    frame.pack(expand=True, fill=tk.BOTH)

    info_label = tk.Label(frame, text="Choose a mode to start the Sudoku Solver:", font=("Arial", 12, "bold"), bg="lightblue")
    info_label.pack(pady=20)

    button_style = {
        "font": ("Arial", 14),
        "width": 20,  
        "height": 2,  
        "relief": "raised",
        "bd": 2,
        "highlightthickness": 0
    }

    def on_hover(event):
        event.widget.config(bg="lightblue")

    def on_leave(event):
        event.widget.config(bg=event.widget.default_bg)

    def select_input_mode():
        root.destroy()
        board = [0] * 81  
        create_gui(board, mode="solve")

    def select_solve_mode():
        def start_game():
            difficulty = difficulty_var.get().lower()
            difficulty_root.destroy()
            board = generate_random_sudoku(difficulty)  
            create_gui(board, mode="solve")

        root.destroy()
        difficulty_root = tk.Tk()
        difficulty_root.title("Select Difficulty")
        difficulty_root.geometry("400x200")

        tk.Label(difficulty_root, text="Choose Difficulty Level:", font=("Arial", 14, "bold")).pack(pady=20)

        difficulty_var = tk.StringVar(value="Easy")
        difficulties = ["Easy", "Medium", "Hard", "Expert"]
        for diff in difficulties:
            tk.Radiobutton(difficulty_root, text=diff, variable=difficulty_var, value=diff, font=("Arial", 12)).pack(anchor="w")

        tk.Button(difficulty_root, text="Start Game", command=start_game, **button_style).pack(pady=20)

        difficulty_root.mainloop()

    def select_mode3():
        def generate_random_board(difficulty):
            root2.destroy()
            random_board = generate_random_sudoku(difficulty)  
            create_gui(random_board, mode="interactive")

        def input_custom_board():
            root2.destroy()
            user_board = [0] * 81
            create_gui(user_board, mode="interactive")

        root.destroy()
        root2 = tk.Tk()
        root2.title("Interactive Mode - Board Selection")
        root2.geometry("400x350")  

        tk.Label(root2, text="Select a Board Source:", font=("Arial", 14, "bold")).pack(pady=20)

        difficulty_frame = tk.Frame(root2)
        difficulty_frame.pack(pady=10)

        def start_game_with_difficulty(difficulty):
            generate_random_board(difficulty)  

        difficulties = ["Easy", "Medium", "Hard", "Expert"]
        for diff in difficulties:
            tk.Button(difficulty_frame, text=diff, command=lambda d=diff: start_game_with_difficulty(d),
                    font=("Arial", 12), width=20, height=2, relief="raised", bd=2).pack(pady=5)

        input_button = tk.Button(root2, text="Empty Board", command=input_custom_board, **button_style)
        input_button.default_bg = "lightcoral"
        input_button.config(bg="lightcoral")
        input_button.pack(pady=10)
        input_button.bind("<Enter>", on_hover)
        input_button.bind("<Leave>", on_leave)

        root2.mainloop()

    input_button = tk.Button(frame, text="Input Mode", command=select_input_mode, **button_style)
    input_button.default_bg = "lightcoral"
    input_button.config(bg="lightcoral")
    input_button.pack(pady=10)
    input_button.bind("<Enter>", on_hover)
    input_button.bind("<Leave>", on_leave)

    solve_button = tk.Button(frame, text="Solve Mode", command=select_solve_mode, **button_style)
    solve_button.default_bg = "lightgreen"
    solve_button.config(bg="lightgreen")
    solve_button.pack(pady=10)
    solve_button.bind("<Enter>", on_hover)
    solve_button.bind("<Leave>", on_leave)

    mode3_button = tk.Button(frame, text="Interactive Mode", command=select_mode3, **button_style)
    mode3_button.default_bg = "lightblue"
    mode3_button.config(bg="lightblue")
    mode3_button.pack(pady=10)
    mode3_button.bind("<Enter>", on_hover)
    mode3_button.bind("<Leave>", on_leave)

    root.mainloop()
