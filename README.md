# 🧩 AC3-Sudoku-Engine

> A powerful, interactive Sudoku solver powered by the Arc Consistency 3 (AC-3) algorithm and Backtracking with Forward Checking. 

Welcome to the **AC3-Sudoku-Engine**! This repository houses a fully-featured, production-ready Sudoku engine. It provides a robust backend implementation of Constraint Satisfaction Problem (CSP) algorithms to solve Sudoku boards instantly. It also includes an interactive Desktop GUI (Tkinter) and a modern Web UI (Streamlit) for generating, solving, and visualizing Sudoku puzzles.

---

## 🗂️ Lab Index

| Lab / Project | Description | Stack |
| --- | --- | --- |
| **`01_AC3_Sudoku_Solver`** | The core Sudoku solver utilizing the AC-3 algorithm for constraint propagation. Features a puzzle generator, a Streamlit web app, and a Tkinter desktop app that visualizes the Arc Consistency Tree. | Python, Tkinter, Streamlit |

*(More modules and algorithms can be added here in the future)*

---

## 🚀 Features

- **AC-3 Algorithm**: Efficient constraint propagation to drastically reduce the search space.
- **Backtracking & Forward Checking**: Fast, robust puzzle solving.
- **Puzzle Generator**: Generate guaranteed-solvable Sudoku puzzles at Easy, Medium, Hard, and Expert difficulties.
- **Multiple Interfaces**: Choose between a lightweight **Web App** (Streamlit) or a feature-rich **Desktop App** (Tkinter) with real-time visualization of the arc consistency tree.

---

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/AC3-Sudoku-Engine.git
   cd AC3-Sudoku-Engine
   ```

2. **Set up a virtual environment (Optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🎯 Quick Start

### 🌐 Option 1: Streamlit Web App (Recommended)
Run the clean, lightweight web interface right in your browser!

```bash
streamlit run 01_AC3_Sudoku_Solver/app.py
```
This will open the app locally at `http://localhost:8501`.

### 💻 Option 2: Tkinter Desktop App
Run the full desktop GUI with deep visualization features (like the Arc Consistency Tree).

```bash
python 01_AC3_Sudoku_Solver/src/main.py
```

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
