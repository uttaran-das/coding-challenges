use std::io::{self, Read};

use termios::Termios;

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

    let mut buffer = [0; 1];
    loop {
        match io::stdin().read(&mut buffer) {
            Ok(0) => break, // EOF
            Ok(_) => {
                let input = buffer[0] as char;
                if input == 'q' {
                    break;
                }
            }
            Err(e) => {
                eprintln!("Error reading from stdin: {}", e);
                break;
            }
        }
    }

    // Restoring original settings
    termios::tcsetattr(stdin, termios::TCSANOW, &original_termios).expect("Failed to restore terminal settings");
}