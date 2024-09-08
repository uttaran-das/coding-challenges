import argparse
import locale
import sys

def count_bytes(input_stream):
    return len(input_stream.read())

def count_lines(input_stream):
    return sum(1 for _ in input_stream)

def count_words(input_stream):
    return sum(len(line.split()) for line in input_stream)

def count_characters(input_stream):
        return sum(len(line)+1 for line in input_stream)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Simple version of wc command to count the number of bytes, lines, or words in a file.")
    parser.add_argument('-c', '--bytes', action='store_true', help="Count the number of bytes in the file.")
    parser.add_argument('-l', '--lines', action='store_true', help="Count the number of lines in the file.")
    parser.add_argument('-w', '--words', action='store_true', help="Count the number of words in the file.")
    parser.add_argument('-m', '--characters', action='store_true', help="Count the number of characters in the file.")
    parser.add_argument('file', type=str, nargs='?', help="Path to the file. If not provided, read from standard input.")
    args = parser.parse_args()

    # Determining the input stream
    if args.file:
        try:
            input_stream = open(args.file, 'r')
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found.")
            return
    else:
        input_stream = sys.stdin

    # Determining which counts to perform
    count_all = not (args.bytes or args.lines or args.words or args.characters)

    # Checking if the -c option is provided
    if args.bytes or count_all:
        byte_count = count_bytes(input_stream.buffer if args.file else input_stream)
        print(f"byte count: {byte_count}")
    
    # Resetting the input stream if reading from a file
    if args.file:
        input_stream.seek(0)

    # Checking if the -l option is provided
    if args.lines or count_all:
        line_count = count_lines(input_stream)
        print(f"line count: {line_count}")

    # Resetting the input stream if reading from a file
    if args.file:
        input_stream.seek(0)

    # Check if the -w option is provided
    if args.words or count_all:
        word_count = count_words(input_stream)
        print(f"word count: {word_count}")
    
    # Resetting the input stream if reading from a file
    if args.file:
        input_stream.seek(0)
    
    # Check if the -m option is provided
    if args.characters:
        char_count = count_characters(input_stream)
        print(f"character count: {char_count}")

    # Closing the file if it was opened
    if input_stream is not sys.stdin:
        input_stream.close()

if __name__ == "__main__":
    main()