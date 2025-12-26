# Snake in terminal
import time
import threading
import pynput
import os
import random

# Definice nastavení
settings = {
    "GRID_SIZE_ROW": 15,
    "GRID_SIZE_COL": 17, 
    "FPS": 7,
    "KEYS": {
        "UP": "w",
        "DOWN": "s",
        "LEFT": "a",
        "RIGHT": "d"
    },
    "start_row": 5,
    "start_col": 5
}

SYMBOLS = {
    "Texts": {
        "Score": "Score:",
        "State": "State:",
        "Position": "Position:",
        "lost": "lost",
        "running": "run"
    },
    "Border": {
        "TL_corner": "╔",
        "TR_corner": "╗",
        "BL_corner": "╚",
        "BR_corner": "╝",
        "Horizontal_line": "═",
        "Vertical_line": "║"
    },
    "Snake": {
        "T_head": "△ ",
        "R_head": " ▷",
        "B_head": "▽ ",
        "L_head": "◁ "
    },
    "Tail" : "∎ ",
    "Apple": "🍎",
    "Empty": "⠀⠀",
    "Mark":  "❌"
    #        "▷ "
}
TEXTS = SYMBOLS["Texts"]
GRID_SIZE_ROW = settings["GRID_SIZE_ROW"]
GRID_SIZE_COL = settings["GRID_SIZE_COL"]
FPS = settings["FPS"]
KEYS = settings["KEYS"]
KEYS_LIST = [KEYS["UP"], KEYS["DOWN"], KEYS["LEFT"], KEYS["RIGHT"]]

last_press = "d"
last_move = ""
game_state = TEXTS["running"]

snake_row = settings["start_row"]
snake_col = settings["start_col"]

tail_pos = [[-1,-1]]

apple_row = random.randint(0, GRID_SIZE_ROW - 1)
apple_col = random.randint(0, GRID_SIZE_COL - 1)

mark_row = -1
mark_col = -1

score = 0

def get_snake_symbol():
    if last_press == KEYS["UP"]:
        return SYMBOLS["Snake"]["T_head"]
    elif last_press == KEYS["DOWN"]:
        return SYMBOLS["Snake"]["B_head"]
    elif last_press == KEYS["LEFT"]:
        return SYMBOLS["Snake"]["L_head"]
    elif last_press == KEYS["RIGHT"]:
        return SYMBOLS["Snake"]["R_head"]
    return SYMBOLS["Snake"]["R_head"]

def board_print():
    BORDER = SYMBOLS["Border"]
    
    # top print
    print(BORDER["TL_corner"] + BORDER["Horizontal_line"] * (GRID_SIZE_COL * 2) + BORDER["TR_corner"])

    for r in range(GRID_SIZE_ROW):
        row_string = ""
        for c in range(GRID_SIZE_COL):
            if r == snake_row and c == snake_col:
                pix = get_snake_symbol()
            elif r == apple_row and c == apple_col:
                pix = SYMBOLS["Apple"]
            elif r == mark_row and c == mark_col:
                pix = SYMBOLS["Mark"]
            elif [r,c] in tail_pos:
                pix = SYMBOLS["Tail"]
            else:
                pix = SYMBOLS["Empty"]
            
            row_string += pix

        print(BORDER["Vertical_line"] + row_string + BORDER["Vertical_line"])

    # bottom print
    print(BORDER["BL_corner"] + BORDER["Horizontal_line"] * (GRID_SIZE_COL * 2) + BORDER["BR_corner"])
    print(f"{TEXTS['Score']} {score} | {TEXTS['State']} {game_state}") # | Pozice: [{snake_row},{snake_col}]
    # print(f"Tail: {tail_pos}")

def logic_loop():
    global snake_col, snake_row, apple_row, apple_col, score, last_move, last_press, game_state

    # Snake move
    if last_press == KEYS["UP"]:
        if last_move != KEYS["DOWN"]:
            snake_row -= 1
            last_move = last_press
            
        else:
            snake_row += 1
            last_press = last_move

    elif last_press == KEYS["DOWN"]:
        if last_move != KEYS["UP"]:
            snake_row += 1
            last_move = last_press
        else:
            snake_row -= 1
            last_press = last_move

    elif last_press == KEYS["LEFT"]:
        if last_move != KEYS["RIGHT"]:
            snake_col -= 1
            last_move = last_press
        else:
            snake_col += 1
            last_press = last_move
            
    elif last_press == KEYS["RIGHT"]:
        if last_move != KEYS["LEFT"]:
            snake_col += 1
            last_move = last_press
        else:
            snake_col -= 1
            last_press = last_move

    # wall colide
    if snake_row < 0:
        snake_row = GRID_SIZE_ROW - 1
        game_state = TEXTS["lost"]

    elif snake_row >= GRID_SIZE_ROW:
        snake_row = 0
        game_state = TEXTS["lost"]
        
    elif snake_col < 0:
        snake_col = GRID_SIZE_COL - 1
        game_state = TEXTS["lost"]

    elif snake_col >= GRID_SIZE_COL:
        snake_col = 0
        game_state = TEXTS["lost"]

    # apple colide + tail count
    if snake_row == apple_row and snake_col == apple_col:
        # random apple
        apple_row = random.randint(0, GRID_SIZE_ROW - 1)
        apple_col = random.randint(0, GRID_SIZE_COL - 1)
        score += 1
        tail_pos.append([snake_row, snake_col])
    else:
        # remove tail
        tail_pos.pop(0)
        tail_pos.append([snake_row, snake_col])
    


def game_loop():
    os.system("")
    print("\033[2J", end="")

    while True:
        print("\033[H", end="")
        logic_loop()
        board_print()
        time.sleep(1/FPS)

def input_loop():
    global last_press
    with pynput.keyboard.Events() as events:
        for event in events:
            if isinstance(event, pynput.keyboard.Events.Press):
                try:
                    key_char = event.key.char
                    if key_char in KEYS_LIST:

                        last_press = key_char
                except AttributeError:
                    pass

if __name__ == "__main__":
    input_thread = threading.Thread(target=input_loop, daemon=True)
    input_thread.start()
    
    try:
        game_loop()
    except KeyboardInterrupt:
        print("\nHra ukončena.")