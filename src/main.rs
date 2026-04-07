use crossterm::{
    terminal::{disable_raw_mode, enable_raw_mode, EnterAlternateScreen, LeaveAlternateScreen},
    event::{self, Event, KeyCode},
    execute,
};
use std::io::{self, Write};
use std::time::{Duration, Instant};
use std::thread;
use rand::Rng;

// Settings
const GRID_SIZE_ROW: usize = 15;
const GRID_SIZE_COL: usize = 17;
const FPS: u32 = 7;

// Symbols
const TL_CORNER: &str = "╔";
const TR_CORNER: &str = "╗";
const BL_CORNER: &str = "╚";
const BR_CORNER: &str = "╝";
const HORIZONTAL_LINE: &str = "═";
const VERTICAL_LINE: &str = "║";

const SNAKE_HEAD_UP: &str = "△ ";
const SNAKE_HEAD_RIGHT: &str = " ▷";
const SNAKE_HEAD_DOWN: &str = "▽ ";
const SNAKE_HEAD_LEFT: &str = "◁ ";
const SNAKE_TAIL: &str = "∎ ";
const APPLE: &str = "🍎";
const EMPTY: &str = "⠀⠀";
const MARK: &str = "❌";

// Texts
const MAIN_TEXT: &str = "Snake in terminal";
const END_TEXT: &str = "you LOST";
const START_PRESS: &str = "Press Enter to start";
const SCORE_TEXT: &str = "Score:";
const STATE_TEXT: &str = "State:";
const LOST_STATE: &str = "lost";
const RUNNING_STATE: &str = "run";

#[derive(Clone, Copy, PartialEq, Eq)]
enum Direction {
    Up,
    Down,
    Left,
    Right,
}

struct GameState {
    snake_row: usize,
    snake_col: usize,
    apple_row: usize,
    apple_col: usize,
    score: usize,
    last_press: Direction,
    last_move: Direction,
    game_state: String,
    tail_pos: Vec<(usize, usize)>,
    mark_row: i32,
    mark_col: i32,
}

impl GameState {
    fn new() -> Self {
        let mut rng = rand::thread_rng();
        GameState {
            snake_row: 5,
            snake_col: 5,
            apple_row: rng.gen_range(0..GRID_SIZE_ROW),
            apple_col: rng.gen_range(0..GRID_SIZE_COL),
            score: 0,
            last_press: Direction::Right,
            last_move: Direction::Right,
            game_state: RUNNING_STATE.to_string(),
            tail_pos: Vec::new(),
            mark_row: -1,
            mark_col: -1,
        }
    }

    fn get_snake_symbol(&self) -> &str {
        match self.last_press {
            Direction::Up => SNAKE_HEAD_UP,
            Direction::Down => SNAKE_HEAD_DOWN,
            Direction::Left => SNAKE_HEAD_LEFT,
            Direction::Right => SNAKE_HEAD_RIGHT,
        }
    }

    fn random_apple(&mut self) {
        let mut rng = rand::thread_rng();
        loop {
            self.apple_row = rng.gen_range(0..GRID_SIZE_ROW);
            self.apple_col = rng.gen_range(0..GRID_SIZE_COL);

            if !self.tail_pos.contains(&(self.apple_row, self.apple_col))
                || (self.apple_row == self.snake_row && self.apple_col == self.snake_col)
            {
                break;
            }
        }
    }

    fn logic_loop(&mut self) {
        let snake_before = (self.snake_row, self.snake_col);

        // Snake move
        match self.last_press {
            Direction::Up => {
                if self.last_move != Direction::Down {
                    self.snake_row = self.snake_row.saturating_sub(1);
                    self.last_move = Direction::Up;
                } else {
                    self.snake_row = self.snake_row.saturating_add(1);
                    self.last_press = self.last_move;
                }
            }
            Direction::Down => {
                if self.last_move != Direction::Up {
                    self.snake_row = self.snake_row.saturating_add(1);
                    self.last_move = Direction::Down;
                } else {
                    self.snake_row = self.snake_row.saturating_sub(1);
                    self.last_press = self.last_move;
                }
            }
            Direction::Left => {
                if self.last_move != Direction::Right {
                    self.snake_col = self.snake_col.saturating_sub(1);
                    self.last_move = Direction::Left;
                } else {
                    self.snake_col = self.snake_col.saturating_add(1);
                    self.last_press = self.last_move;
                }
            }
            Direction::Right => {
                if self.last_move != Direction::Left {
                    self.snake_col = self.snake_col.saturating_add(1);
                    self.last_move = Direction::Right;
                } else {
                    self.snake_col = self.snake_col.saturating_sub(1);
                    self.last_press = self.last_move;
                }
            }
        }

        // Snake tail collision
        if self.tail_pos.contains(&(self.snake_row, self.snake_col)) {
            self.game_state = LOST_STATE.to_string();
        }

        // Wall collision
        if self.snake_row < 0 || self.snake_row >= GRID_SIZE_ROW {
            self.game_state = LOST_STATE.to_string();
        }
        if self.snake_col < 0 || self.snake_col >= GRID_SIZE_COL {
            self.game_state = LOST_STATE.to_string();
        }

        // Apple collision + tail count
        if self.snake_row == self.apple_row && self.snake_col == self.apple_col {
            self.random_apple();
            self.score += 1;
            self.tail_pos.push(snake_before);
        } else {
            // Remove tail
            if !self.tail_pos.is_empty() {
                self.tail_pos.push(snake_before);
                self.tail_pos.remove(0);
            }
        }
    }
}

fn clear_screen() {
    print!("\x1B[2J\x1B[H");
    io::stdout().flush().unwrap();
}

fn menu_print() {
    let mut output = String::new();

    // Top border
    output.push_str(TL_CORNER);
    output.push_str(&HORIZONTAL_LINE.repeat(GRID_SIZE_COL * 2));
    output.push_str(TR_CORNER);
    output.push('\n');

    // Middle
    for r in 0..GRID_SIZE_ROW {
        let row_string = if r == 1 {
            let text = MAIN_TEXT;
            let padding = GRID_SIZE_COL - text.len() / 2;
            format!("{}{}", " ".repeat(padding), text)
        } else {
            " ".to_string()
        };

        let padded = format!(
            "{}{}",
            row_string,
            " ".repeat((GRID_SIZE_COL * 2).saturating_sub(row_string.len()))
        );

        output.push_str(VERTICAL_LINE);
        output.push_str(&padded);
        output.push_str(VERTICAL_LINE);
        output.push('\n');
    }

    // Bottom border
    output.push_str(BL_CORNER);
    output.push_str(&HORIZONTAL_LINE.repeat(GRID_SIZE_COL * 2));
    output.push_str(BR_CORNER);
    output.push('\n');

    print!("{}", output);
    io::stdout().flush().unwrap();
}

fn board_print(game: &GameState) {
    let mut output = String::new();

    // Top border
    output.push_str(TL_CORNER);
    output.push_str(&HORIZONTAL_LINE.repeat(GRID_SIZE_COL * 2));
    output.push_str(TR_CORNER);
    output.push('\n');

    // Middle
    for r in 0..GRID_SIZE_ROW {
        output.push_str(VERTICAL_LINE);
        for c in 0..GRID_SIZE_COL {
            let pix = if r == game.snake_row && c == game.snake_col {
                game.get_snake_symbol()
            } else if game.tail_pos.contains(&(r, c)) {
                SNAKE_TAIL
            } else if r == game.apple_row && c == game.apple_col {
                APPLE
            } else if r == game.mark_row as usize && c == game.mark_col as usize {
                MARK
            } else {
                EMPTY
            };
            output.push_str(pix);
        }
        output.push_str(VERTICAL_LINE);
        output.push('\n');
    }

    // Bottom border
    output.push_str(BL_CORNER);
    output.push_str(&HORIZONTAL_LINE.repeat(GRID_SIZE_COL * 2));
    output.push_str(BR_CORNER);
    output.push('\n');
    output.push_str(&format!(
        "{} {} | {} {}\n",
        SCORE_TEXT, game.score, STATE_TEXT, game.game_state
    ));
    output.push_str(&format!("Tail: {:?}\n", game.tail_pos));

    print!("{}", output);
    io::stdout().flush().unwrap();
}

fn end_screen_print(game: &GameState) {
    let mut output = String::new();

    // Top border
    output.push_str(TL_CORNER);
    output.push_str(&HORIZONTAL_LINE.repeat(GRID_SIZE_COL * 2));
    output.push_str(TR_CORNER);
    output.push('\n');

    // Middle
    for r in 0..GRID_SIZE_ROW {
        let row_string = match r {
            1 => {
                let text = END_TEXT;
                let padding = GRID_SIZE_COL - text.len() / 2;
                format!("{}{}", " ".repeat(padding), text)
            }
            2 => format!("Score: {}", game.score),
            _ => " ".to_string(),
        };

        let padded = format!(
            "{}{}",
            row_string,
            " ".repeat((GRID_SIZE_COL * 2).saturating_sub(row_string.len()))
        );

        output.push_str(VERTICAL_LINE);
        output.push_str(&padded);
        output.push_str(VERTICAL_LINE);
        output.push('\n');
    }

    // Bottom border
    output.push_str(BL_CORNER);
    output.push_str(&HORIZONTAL_LINE.repeat(GRID_SIZE_COL * 2));
    output.push_str(BR_CORNER);
    output.push('\n');

    print!("{}", output);
    io::stdout().flush().unwrap();
}

fn main() -> io::Result<()> {
    let mut game = GameState::new();
    
    // Setup terminal
    enable_raw_mode()?;
    let mut stdout = io::stdout();
    execute!(stdout, EnterAlternateScreen)?;

    clear_screen();
    menu_print();

    // Wait for Enter
    loop {
        if event::poll(Duration::from_millis(100))? {
            if let Event::Key(key) = event::read()? {
                if key.code == KeyCode::Enter {
                    break;
                }
            }
        }
    }

    // Game loop
    clear_screen();
    let frame_time = Duration::from_millis(1000 / FPS as u64);
    let mut last_frame = Instant::now();

    loop {
        game.logic_loop();

        print!("\x1B[H");
        board_print(&game);

        if game.game_state == LOST_STATE {
            break;
        }

        // Handle input (non-blocking)
        while event::poll(Duration::from_millis(10))? {
            if let Event::Key(key) = event::read()? {
                match key.code {
                    KeyCode::Char('w') | KeyCode::Up => game.last_press = Direction::Up,
                    KeyCode::Char('s') | KeyCode::Down => game.last_press = Direction::Down,
                    KeyCode::Char('a') | KeyCode::Left => game.last_press = Direction::Left,
                    KeyCode::Char('d') | KeyCode::Right => game.last_press = Direction::Right,
                    KeyCode::Esc | KeyCode::Char('q') => {
                        game.game_state = LOST_STATE.to_string();
                        break;
                    }
                    _ => {}
                }
            }
        }

        // Frame rate control
        let elapsed = last_frame.elapsed();
        if elapsed < frame_time {
            thread::sleep(frame_time - elapsed);
        }
        last_frame = Instant::now();
    }

    // End screen
    clear_screen();
    game.logic_loop();
    end_screen_print(&game);
    println!("Press enter to exit");

    // Wait for Enter
    loop {
        if event::poll(Duration::from_millis(100))? {
            if let Event::Key(key) = event::read()? {
                if key.code == KeyCode::Enter {
                    break;
                }
            }
        }
    }

    // Cleanup
    disable_raw_mode()?;
    execute!(stdout, LeaveAlternateScreen)?;

    Ok(())
}
