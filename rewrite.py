from pathlib import Path
import os
import random
import sys
from pathlib import Path
import json

# Testovací režim
test_mode = "--test-mode" in sys.argv

if not test_mode:
    try:
        import pynput
    except ImportError:
        print("Knihovna pynput nenalezena. Spouštím v omezeném režimu.")
else:
    print("Running in test mode - pynput skip.")

class Snake:
    def __init__(self):
        self.cfg_folder = "cfg"
        # Ujistíme se, že složka existuje, aby program nespadl
        if not os.path.exists(self.cfg_folder):
            os.makedirs(self.cfg_folder)

        self.texts = {
            "Main_text": "Snake in terminal",
            "End_text": "you LOST",
            "Start_press": "Press Enter to start",
            "Score": "Score:",
            "State": "State:",
            "Position": "Position:",
            "Lost": "lost",
            "Running": "run"
        }
        
        self.field_border = {
            "TL_corner": "╔",
            "TR_corner": "╗",
            "BL_corner": "╚",
            "BR_corner": "╝",
            "Horizontal_line": "═",
            "Vertical_line": "║"
        }

    def load_settings(self, file):
        try:
            with open(file, "r", encoding="utf-8") as f:
                cfg = f.read()
                cfg = cfg.splitlines()
                return cfg
        except Exception as e:
            return []

    def show_settings(self):
        files = os.listdir(self.cfg_folder)
        return files if files else "Složka cfg je prázdná."

    def main_loop(self):
        pass


if __name__ == "__main__":
    sn = Snake()
    sn.main_loop()