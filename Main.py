# Snake in terminal
import time
import threading
import os
import random
import sys

test_mode = "--test-mode" in sys.argv

if not test_mode:
    import pynput
else:
    print("Running in test mode - pynput skip.")

# Definie settings
settings = {
    "GRID_SIZE_ROW": 10,
    "GRID_SIZE_COL": 5, 
    "Fps": 7,
    "Keys": {
        "UP": "w",
        "DOWN": "s",
        "LEFT": "a",
        "RIGHT": "d"
    },
    "Start_row": 5,
    "Start_col": 5
}

SYMBOLS = {
    "Texts": {
        "Main_text": "Snake in terminal",
        "End_text": "you LOST",
        "Start_press": "Press Enter to start",
        "Stop_press": "Press Enter to start",
        "Score": "Score:",
        "State": "State:",
        "Position": "Position:",
        "Lost": "lost",
        "Running": "run",
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
FPS = settings["Fps"]
KEYS = settings["Keys"]
KEYS_LIST = [KEYS["UP"], KEYS["DOWN"], KEYS["LEFT"], KEYS["RIGHT"]]

# game
last_press = "d"
last_move = ""
game_state = TEXTS["Running"]
end_time = 0
elapsed_time = 0

# snake
snake_row = settings["Start_row"]
snake_col = settings["Start_col"]
snake_before = [snake_row, snake_col]

tail_pos = []

# apple
apple_row = random.randint(0, GRID_SIZE_ROW - 1)
apple_col = random.randint(0, GRID_SIZE_COL - 1)

# mark
mark_row = -1
mark_col = -1

score = 0

def value_control():
    if settings["GRID_SIZE_COL"] <= settings["Start_col"]:
        print("GRID_SIZE_COL and Start_col problem")
    elif settings["GRID_SIZE_ROW"] <= settings["Start_row"]:
        print("GRID_SIZE_ROW and Start_row problem")
    else:
        return True
    return False

def get_snake_symbol():
    if last_press == KEYS["UP"]: return SYMBOLS["Snake"]["T_head"]
    elif last_press == KEYS["DOWN"]: return SYMBOLS["Snake"]["B_head"]
    elif last_press == KEYS["LEFT"]: return SYMBOLS["Snake"]["L_head"]
    elif last_press == KEYS["RIGHT"]: return SYMBOLS["Snake"]["R_head"]
    return SYMBOLS["Snake"]["R_head"]

def menu_print():
    BORDER = SYMBOLS["Border"]
    
    full_print = ""

    # top print
    full_print += BORDER["TL_corner"] + BORDER["Horizontal_line"] * (GRID_SIZE_COL * 2) + BORDER["TR_corner"] + "\n"

    # midle
    for r in range(GRID_SIZE_ROW):
        if False:
            pass
        elif r == 1:
            text = TEXTS["Main_text"]
            out = " " * int(GRID_SIZE_COL - len(text)/2) + str(text)
        else:
            out = " "

        row_string = out + " " * (GRID_SIZE_COL*2 - len(out))

        full_print += BORDER["Vertical_line"] + row_string + BORDER["Vertical_line"] + "\n"

    # bottom print
    full_print += BORDER["BL_corner"] + BORDER["Horizontal_line"] * (GRID_SIZE_COL * 2) + BORDER["BR_corner"] + "\n"

    print(full_print)

def board_print():
    BORDER = SYMBOLS["Border"]
    
    full_print = ""

    # top print
    full_print += BORDER["TL_corner"] + BORDER["Horizontal_line"] * (GRID_SIZE_COL * 2) + BORDER["TR_corner"] + "\n"

    # middle print
    for r in range(GRID_SIZE_ROW):
        row_string = ""
        for c in range(GRID_SIZE_COL):
            if False:
                pass
            elif r == snake_row and c == snake_col:
                pix = get_snake_symbol()
            elif [r,c] in tail_pos:
                pix = SYMBOLS["Tail"]
            elif r == apple_row and c == apple_col:
                pix = SYMBOLS["Apple"]
            elif r == mark_row and c == mark_col:
                pix = SYMBOLS["Mark"]
            else:
                pix = SYMBOLS["Empty"]
            
            row_string += pix

        full_print += BORDER["Vertical_line"] + row_string + BORDER["Vertical_line"] + "\n"

    # bottom print
    full_print += BORDER["BL_corner"] + BORDER["Horizontal_line"] * (GRID_SIZE_COL * 2) + BORDER["BR_corner"] + "\n"
    full_print += f"{TEXTS['Score']} {score} | {TEXTS['State']} {game_state}" + "\n" # | Pozice: [{snake_row},{snake_col}]
    full_print += f"Tail: {tail_pos}" + "\n"

    print(full_print)

def end_screen_print():
    BORDER = SYMBOLS["Border"]
    
    full_print = ""

    # top print
    full_print += BORDER["TL_corner"] + BORDER["Horizontal_line"] * (GRID_SIZE_COL * 2) + BORDER["TR_corner"] + "\n"

    # middle print
    for r in range(GRID_SIZE_ROW):
        if False:
            pass
        elif r == 1:
            text = TEXTS["End_text"]
            out =  " " * int(GRID_SIZE_COL - len(text)/2) + str(text)
        elif r == 2:
            out = f"Score: {score}"
        else:
            out = " "
        
        row_string = str(out) + " " * (GRID_SIZE_COL*2 - len(out))


        full_print += BORDER["Vertical_line"] + row_string + BORDER["Vertical_line"] + "\n"

    # bottom print
    full_print += BORDER["BL_corner"] + BORDER["Horizontal_line"] * (GRID_SIZE_COL * 2) + BORDER["BR_corner"] + "\n"

    print(full_print)

def random_apple():
    global apple_row, apple_col

    while True:
        apple_row = random.randint(0, GRID_SIZE_ROW - 1)
        apple_col = random.randint(0, GRID_SIZE_COL - 1)

        if [apple_row, apple_col] in tail_pos and [apple_row, apple_col] != [snake_row, snake_col]:
            print("problem")
        else:
            return apple_row, apple_col

def logic_loop():
    global snake_col, snake_row, apple_row, apple_col, score, last_move, last_press, game_state

    snake_before = [snake_row, snake_col]

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

    # snake tail colide
    if [snake_row, snake_col] in tail_pos:
        game_state = TEXTS["Lost"]

    # wall colide
    if False:
        pass
    elif snake_row < 0:
        snake_row = 0
        game_state = TEXTS["Lost"]

    elif snake_row >= GRID_SIZE_ROW:
        snake_row = GRID_SIZE_ROW - 1
        game_state = TEXTS["Lost"]
        
    elif snake_col < 0:
        snake_col = 0
        game_state = TEXTS["Lost"]

    elif snake_col >= GRID_SIZE_COL:
        snake_col = GRID_SIZE_COL - 1
        game_state = TEXTS["Lost"]

    # apple colide + tail count
    if snake_row == apple_row and snake_col == apple_col:
        # random apple
        random_apple()
        score += 1
        tail_pos.append(snake_before)
    else:
        # remove tail
        if len(tail_pos) > 0:
            tail_pos.append(snake_before)
            tail_pos.pop(0)

def menu_logic():
    menu_print()
    input(TEXTS["Start_press"])

def game_loop():
    os.system("")
    print("\033[2J", end="")

    if test_mode:
        menu_print()
        logic_loop()
        board_print()
        end_screen_print()
        print("Test Run ok.")
        return

    elif value_control():
        print("\033[H", end="")
        logic_loop()
        menu_logic()

        print("\033[H", end="")
        board_print()
        time.sleep(1)

        while game_state == TEXTS["Running"]:
            logic_loop()
           
            print("\033[H", end="")
            board_print()

            time.sleep(1 / FPS)
        time.sleep(1)

        print("\033[H", end="")
        logic_loop()
        end_screen_print()
        time.sleep(1)
        input("Press enter to exit")

def input_loop():
    global last_press
    if test_mode: return

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