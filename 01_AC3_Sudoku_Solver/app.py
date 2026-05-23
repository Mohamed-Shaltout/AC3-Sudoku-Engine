import streamlit as st
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.generator import generate_random_sudoku
from src.solver import solve_with_ac3

st.set_page_config(page_title="AC-3 Sudoku Solver", page_icon="🧩")

st.title("🧩 AC-3 Sudoku Solver")
st.markdown("Solve any Sudoku puzzle using the Arc Consistency 3 (AC-3) algorithm and Backtracking with Forward Checking.")

# Session state initialization
if "board" not in st.session_state:
    st.session_state.board = [0] * 81

def sync_board_to_widgets():
    for i in range(9):
        for j in range(9):
            val = st.session_state.board[i * 9 + j]
            st.session_state[f"cell_{i}_{j}"] = str(val) if val != 0 else ""


col1, col2 = st.columns([1, 2])

with col1:
    st.header("Controls")
    difficulty = st.selectbox("Generate Random Sudoku", ["Easy", "Medium", "Hard", "Expert"])
    
    if st.button("Generate"):
        st.session_state.board = generate_random_sudoku(difficulty.lower())
        sync_board_to_widgets()
        st.rerun()
        
    if st.button("Clear Board"):
        st.session_state.board = [0] * 81
        sync_board_to_widgets()
        st.rerun()
        
    if st.button("Solve with AC-3"):
        with st.spinner("Solving..."):
            start_time = time.time()
            board_copy = st.session_state.board.copy()
            if solve_with_ac3(board_copy):
                st.session_state.board = board_copy
                sync_board_to_widgets()
                st.success(f"Solved in {time.time() - start_time:.3f} seconds!")
            else:
                st.error("No solution exists for this configuration.")

with col2:
    st.header("Sudoku Board")
    
    st.markdown("""
    <style>
    div[data-testid="stTextInput"] input {
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        padding: 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    layout_ratio = [0.5, 1, 1, 1, 0.2, 1, 1, 1, 0.2, 1, 1, 1]
    
    # Column headers
    header_cols = st.columns(layout_ratio)
    col_idx = 1
    for b in range(3):
        for j in range(3):
            header_cols[col_idx].markdown(f"<div style='text-align: center; font-weight: bold; color: #888;'>{b*3 + j + 1}</div>", unsafe_allow_html=True)
            col_idx += 1
        if b < 2: col_idx += 1  # skip gap
            
    row_labels = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
    
    for i in range(9):
        # Add horizontal divider for 3x3 blocks
        if i % 3 == 0 and i != 0:
            st.markdown("<hr style='margin: 0px; padding: 0px; border-top: 3px solid #666;'>", unsafe_allow_html=True)
            
        cols = st.columns(layout_ratio)
        
        # Row label
        cols[0].markdown(f"<div style='text-align: center; font-weight: bold; color: #888; padding-top: 10px;'>{row_labels[i]}</div>", unsafe_allow_html=True)
        
        col_idx = 1
        for b in range(3):
            for j in range(3):
                actual_j = b * 3 + j
                idx = i * 9 + actual_j
                val = st.session_state.board[idx]
                display_val = str(val) if val != 0 else ""
                
                # Using unique keys for each text input
                new_val = cols[col_idx].text_input(
                    label=f"cell_{i}_{actual_j}",
                    value=display_val,
                    label_visibility="collapsed",
                    key=f"cell_{i}_{actual_j}"
                )
                
                if new_val.isdigit() and 1 <= int(new_val) <= 9:
                    st.session_state.board[idx] = int(new_val)
                elif new_val == "":
                    st.session_state.board[idx] = 0
                    
                col_idx += 1
            
            if b < 2:
                # Vertical divider inside the gap column
                cols[col_idx].markdown("<div style='border-left: 3px solid #666; height: 100%; margin-left: 50%; padding-top: 35px;'></div>", unsafe_allow_html=True)
                col_idx += 1
