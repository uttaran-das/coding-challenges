use std::{env, io::{self, Read, Write}, net::TcpStream, process, str::FromStr};

fn main() -> io::Result<()> {
    // Parse the command line arguments
    let arguments: Vec<String> = env::args().collect();
    if arguments.len() != 3 {
        eprintln!("Usage: {} <host> <port>", arguments[0]);
        process::exit(1);
    }

    let host: &str = &arguments[1];
    let port = u16::from_str(&arguments[2]).expect("Invalid port number");

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
