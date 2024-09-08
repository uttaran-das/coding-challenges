import argparse
import sys

def cut_field(input_stream, field_list, delimiter):
    for line in input_stream:
        fields = line.strip().split(delimiter)
        extracted_fields = [fields[i - 1] for i in field_list if 1 <= i <= len(fields)]
        print(delimiter.join(extracted_fields))

def main():
    parser = argparse.ArgumentParser(description="Extract a specified field from each line of a file with delimiter or standard input.")
    parser.add_argument('-f', '--field', type=str, default=1, help="Field number to extract (default is 1). Comma or whitespace separated.")
    parser.add_argument('-d', '--delimiter', type=str, default='\t', help="Delimiter character to use. Default is tab.")
    parser.add_argument('file', type=str, nargs='?', default='-',  help="Path to the file. Use '-' to read from standard input.")
    args = parser.parse_args()

    # Determining the input stream
    if args.file == '-':
        input_stream = sys.stdin
    else:
        try:
            input_stream = open(args.file, 'r')
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found.")
            return

    field_list = [int(field) for field in args.field.split(',' if ',' in args.field else ' ')]

    cut_field(input_stream, field_list, args.delimiter)

    # Closing the file if it was opened
    if input_stream is not sys.stdin:
        input_stream.close()

if __name__ == "__main__":
    main()