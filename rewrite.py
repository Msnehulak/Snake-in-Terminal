# Snake in terminal
import time
import threading
import os
import random
import sys
from pathlib import Path
import json

test_mode = "--test-mode" in sys.argv

if not test_mode:
    import pynput
else:
    print("Running in test mode - pynput skip.")

class snake:
    def __init__(self):
        self.texts = {
            "Main_text": "Snake in terminal",
            "End_text": "you LOST",
            "Start_press": "Press Enter to start",
            "Stop_press": "Press Enter to start",
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
        self.field_border = ""