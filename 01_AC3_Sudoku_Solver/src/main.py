import sys
import os

# Add the parent directory to sys.path so 'src' can be imported easily
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.gui import mode_selection_gui

if __name__ == "__main__":
    mode_selection_gui()
