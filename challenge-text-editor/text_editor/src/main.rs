use std::io::{self, Read, Write};
use termios::Termios;

enum Mode {
    Control,
    Editor,
}

fn main() {
    let stdin = 0; // file descriptor for stdin
    let mut termios = Termios::from_fd(stdin).expect("Failed to get terminal settings");

    // Saving the original terminal settings
    let original_termios = termios.clone();

    // Disable canonical mode (unbuffered input)
    termios.c_lflag &= !(termios::ICANON);

    // Disable echo
    termios.c_lflag &= !(termios::ECHO);

    // Disable output processing
    termios.c_lflag &= !(termios::OPOST);

    // Disable special handling of CTRL-C, CTRL-Z, CTRL-M, CTRL-S, CTRL-Q, CTRL-V
    termios.c_lflag &= !(termios::ISIG | termios::IEXTEN);

    // Applying the new terminal settings
    termios::tcsetattr(stdin, termios::TCSANOW, &termios).expect("Failed to set terminal attributes");

    // Clear the screen
    print!("\x1b[2J");
    io::stdout().flush().expect("Failed to flush stdout");

    // Draw a vertical line of characters down the left-hand side of the screen
    let screen_height = 24; // Assuming a standard terminal height of 24 lines
    for i in 0..screen_height {
        print!("\x1b[{};1H~", i + 1);
        io::stdout().flush().expect("Failed to flush stdout");
    }

    // Position the cursor at the top left
    print!("\x1b[H");
    io::stdout().flush().expect("Failed to flush stdout");

    let mut cursor_row = 1;
    let mut cursor_col = 1;
    let mut mode = Mode::Control;
    let mut lines: Vec<String> = vec![String::new(); screen_height];

    let mut buffer = [0; 1];
    loop {
        match io::stdin().read(&mut buffer) {
            Ok(0) => break, // EOF
            Ok(_) => {
                let input = buffer[0] as char;
                match mode {
                    Mode::Control => {
                        match input {
                            'h' => {
                                if cursor_col > 1 {
                                    cursor_col -= 1;
                                }
                            }
                            'j' => {
                                if cursor_row < screen_height {
                                    cursor_row += 1;
                                }
                            }
                            'k' => {
                                if cursor_row > 1 {
                                    cursor_row -= 1;
                                }
                            }
                            'l' => {
                                cursor_col += 1;
                            }
                            '\x1b' => {
                                mode = Mode::Editor;
                                continue;
                            }
                            'q' => break,
                            _ => continue,
                        }
                    }
                    Mode::Editor => {
                        match input {
                            '\x1b' => {
                                mode = Mode::Control;
                                continue;
                            }
                            '\n' => {
                                if cursor_row < screen_height {
                                    cursor_row += 1;
                                    cursor_col = 1;
                                }
                            }
                            '\x7f' => { // Backspace
                                if cursor_col > 1 {
                                    cursor_col -= 1;
                                    lines[cursor_row - 1].remove(cursor_col - 1);
                                }
                            }
                            _ => {
                                lines[cursor_row - 1].insert(cursor_col - 1, input);
                                cursor_col += 1;
                            }
                        }
                    }
                }

                // Move the cursor to the new position
                print!("\x1b[2J\x1b[H");
                for i in 0..screen_height {
                    print!("\x1b[{};1H~", i + 1);
                    print!("{}", lines[i]);
                }
                print!("\x1b[{};{}H", cursor_row, cursor_col);
                io::stdout().flush().expect("Failed to flush stdout");
            }
            Err(e) => {
                eprintln!("Error reading from stdin: {}", e);
                break;
            }
        }
    }

    // Clear the screen and position the cursor at the top left before exiting
    print!("\x1b[2J\x1b[H");
    io::stdout().flush().expect("Failed to flush stdout");

    // Restoring original settings
    termios::tcsetattr(stdin, termios::TCSANOW, &original_termios).expect("Failed to restore terminal settings");
}