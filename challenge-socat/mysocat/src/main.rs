use std::{env, fs::File, io::{self, Read, Write}, net::TcpStream, process, str::FromStr};

fn main() -> io::Result<()> {
    // Parse the command line arguments
    let arguments: Vec<String> = env::args().collect();
    if arguments.len() != 3 {
        eprintln!("Usage: {} <mode> <target>", arguments[0]);
        eprintln!("Modes:");
        eprintln!("  -u STDIO FILE:<filename>,create - Write stdin to a file");
        eprintln!("  - TCP4:<host>:<port> - Forward stdin to a remote TCP connection");
        process::exit(1);
    }

    let mode = &arguments[1];
    let target = &arguments[2];

    match mode.as_str() {
        "-u" => {
            // Handle file writing mode
            if !target.starts_with("FILE:") {
                eprintln!("Invalid target for file mode. Use FILE:<filename>,create");
                process::exit(1);
            }

            // Extract filename from target
            let filename = target
                .strip_prefix("FILE:")
                .and_then(|s| s.strip_suffix(",create"))
                .unwrap_or_else(|| {
                    eprintln!("Invalid target format. Use FILE:<filename>,create");
                    process::exit(1);
                });

            // Create or open the file for writing
            let mut file = File::create(filename)?;
            println!("Writing stdin to file: {}", filename);

            // Read from stdin and write to the file
            let mut buffer = [0; 1024];
            loop {
                let bytes_read = io::stdin().read(&mut buffer)?;
                if bytes_read == 0 {
                    break; // EOF
                }
                file.write_all(&buffer[..bytes_read])?;
            }

            println!("File write complete.");
        }
        _ => {
            // Handle TCP forwarding mode
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
        }
    }

    Ok(())
}
