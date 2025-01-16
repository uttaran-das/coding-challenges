use std::{env, fs::{File, OpenOptions}, io::{self, Read, Write}, net::{TcpListener, TcpStream}, process, str::FromStr, sync::{Arc, Mutex}};
use std::thread;

fn main() -> io::Result<()> {
    // Parse the command line arguments
    let arguments: Vec<String> = env::args().collect();
    if arguments.len() != 3 {
        eprintln!("Usage: {} <mode> <target>", arguments[0]);
        eprintln!("Modes:");
        eprintln!("  -u STDIO FILE:<filename>,create - Write stdin to a file");
        eprintln!("  -u TCP4-LISTEN:<port>,reuseaddr,fork OPEN:<filename>,create,append - Listen for TCP connections and append data to a file");
        eprintln!("  - TCP4:<host>:<port> - Forward stdin to a remote TCP connection");
        process::exit(1);
    }

    let mode = &arguments[1];
    let target = &arguments[2];

    match mode.as_str() {
        "-u" => handle_unidirectional_mode(target)?,
        _ => handle_tcp_forwarding_mode(target)?,
    }

    Ok(())
}

/// Handles the unidirectional mode (-u).
fn handle_unidirectional_mode(target: &str) -> io::Result<()> {
    if target.starts_with("TCP4-LISTEN:") {
        let (tcp_config, file_config) = parse_tcp_listener_target(target)?;
        let port = parse_tcp_listener_config(&tcp_config)?;
        let filename = parse_file_config(&file_config)?;

        // Start the TCP listener
        start_tcp_listener(port, filename)?;
    } else if target.starts_with("FILE:") {
        let filename = parse_file_create_config(target)?;

        // Write stdin to the file
        write_stdin_to_file(&filename)?;
    } else {
        eprintln!("Invalid target for -u mode. Use TCP4-LISTEN:<port>,reuseaddr,fork OPEN:<filename>,create,append or FILE:<filename>,create");
        process::exit(1);
    }

    Ok(())
}

/// Parses the TCP listener target into TCP config and file config.
fn parse_tcp_listener_target(target: &str) -> io::Result<(&str, &str)> {
    let parts: Vec<&str> = target.splitn(2, ' ').collect();
    if parts.len() != 2 {
        eprintln!("Invalid target format. Use TCP4-LISTEN:<port>,reuseaddr,fork OPEN:<filename>,create,append");
        process::exit(1);
    }

    Ok((parts[0], parts[1]))
}

/// Parses the TCP listener configuration and returns the port.
fn parse_tcp_listener_config(tcp_config: &str) -> io::Result<u16> {
    let tcp_parts: Vec<&str> = tcp_config
        .strip_prefix("TCP4-LISTEN:")
        .unwrap()
        .split(',')
        .collect();
    if tcp_parts.len() < 3 || tcp_parts[1] != "reuseaddr" || tcp_parts[2] != "fork" {
        eprintln!("Invalid TCP listener format. Use TCP4-LISTEN:<port>,reuseaddr,fork");
        process::exit(1);
    }

    let port = u16::from_str(tcp_parts[0]).expect("Invalid port number");
    Ok(port)
}

/// Parses the file configuration and returns the filename.
fn parse_file_config(file_config: &str) -> io::Result<&str> {
    if !file_config.starts_with("OPEN:") || !file_config.ends_with(",create,append") {
        eprintln!("Invalid file format. Use OPEN:<filename>,create,append");
        process::exit(1);
    }

    let filename = file_config
        .strip_prefix("OPEN:")
        .and_then(|s| s.strip_suffix(",create,append"))
        .unwrap_or_else(|| {
            eprintln!("Invalid file format. Use OPEN:<filename>,create,append");
            process::exit(1);
        });

    Ok(filename)
}

/// Starts a TCP listener on the specified port and appends data to the file.
fn start_tcp_listener(port: u16, filename: &str) -> io::Result<()> {
    let listener = TcpListener::bind(("0.0.0.0", port))?;
    println!("Listening on port {}...", port);

    // Allow address reuse
    listener.set_nonblocking(false)?;

    // Open the log file for appending
    let file = OpenOptions::new()
        .create(true)
        .append(true)
        .open(filename)?;

    // Wrap the file in an `Arc<Mutex<File>>` for thread-safe access
    let log_file = Arc::new(Mutex::new(file));

    // Accept incoming connections
    for stream in listener.incoming() {
        match stream {
            Ok(stream) => {
                println!("New connection from: {}", stream.peer_addr()?);

                // Clone the log file handle for the new thread
                let log_file = Arc::clone(&log_file);

                // Spawn a new thread to handle the connection
                thread::spawn(move || {
                    if let Err(e) = handle_connection(stream, log_file) {
                        eprintln!("Error handling connection: {}", e);
                    }
                });
            }
            Err(e) => {
                eprintln!("Failed to accept connection: {}", e);
            }
        }
    }

    Ok(())
}

/// Handles an incoming TCP connection and appends data to the file.
fn handle_connection(mut stream: TcpStream, log_file: Arc<Mutex<File>>) -> io::Result<()> {
    let mut buffer = [0; 1024];
    loop {
        let bytes_read = stream.read(&mut buffer)?;
        if bytes_read == 0 {
            break; // EOF
        }

        // Append the received data to the log file
        let mut file = log_file.lock().unwrap();
        file.write_all(&buffer[..bytes_read])?;
    }

    println!("Connection closed: {}", stream.peer_addr()?);
    Ok(())
}

/// Parses the file create configuration and returns the filename.
fn parse_file_create_config(target: &str) -> io::Result<&str> {
    if !target.ends_with(",create") {
        eprintln!("Invalid target for file mode. Use FILE:<filename>,create");
        process::exit(1);
    }

    let filename = target
        .strip_prefix("FILE:")
        .and_then(|s| s.strip_suffix(",create"))
        .unwrap_or_else(|| {
            eprintln!("Invalid target format. Use FILE:<filename>,create");
            process::exit(1);
        });

    Ok(filename)
}

/// Writes data from stdin to a file.
fn write_stdin_to_file(filename: &str) -> io::Result<()> {
    let mut file = OpenOptions::new()
        .create(true)
        .write(true)
        .open(filename)?;
    println!("Writing stdin to file: {}", filename);

    let mut buffer = [0; 1024];
    loop {
        let bytes_read = io::stdin().read(&mut buffer)?;
        if bytes_read == 0 {
            break; // EOF
        }
        file.write_all(&buffer[..bytes_read])?;
    }

    println!("File write complete.");
    Ok(())
}

/// Handles the TCP forwarding mode.
fn handle_tcp_forwarding_mode(target: &str) -> io::Result<()> {
    if !target.starts_with("TCP4:") {
        eprintln!("Invalid target for TCP mode. Use TCP4:<host>:<port>");
        process::exit(1);
    }

    // Extract host and port from target
    let parts: Vec<&str> = target.strip_prefix("TCP4:").unwrap().split(':').collect();
    if parts.len() != 2 {
        eprintln!("Invalid target format. Use TCP4:<host>:<port>");
        process::exit(1);
    }

    let host = parts[0];
    let port = u16::from_str(parts[1]).expect("Invalid port number");

    // Connect to the remote host and port
    let mut stream = TcpStream::connect((host, port))?;
    println!("Connected to {}:{}", host, port);

    // Send a valid HTTP GET request
    let request = format!(
        "GET /get HTTP/1.1\r\nHost: {}\r\nAccept: */*\r\n\r\n",
        host
    );
    stream.write_all(request.as_bytes())?;
    println!("Sent HTTP request:\n{}", request);

    // Read the response from the server
    let mut response = Vec::new();
    stream.read_to_end(&mut response)?;
    let response_str = String::from_utf8_lossy(&response);

    println!("Received response:\n{}", response_str);

    Ok(())
}