import argparse

def cut_field(file_path, field_list, delimiter):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                fields = line.strip().split(delimiter);
                extracted_fields = [fields[i - 1] for i in field_list if 1 <= i <= len(fields)]
                print(delimiter.join(extracted_fields))
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description="Extract a specified field from each line of a file with delimiter.")
    parser.add_argument('-f', '--field', type=str, default=1, help='Field number to extract (default is 1). Comma or whitespace separated.')
    parser.add_argument('-d', '--delimiter', type=str, default='\t', help="Delimiter character to use. Default is tab.")
    parser.add_argument('file', help='Path to the tab-separated file')
    args = parser.parse_args()

    field_list = [int(field) for field in args.field.split(',' if ',' in args.field else ' ')]

    cut_field(args.file, field_list, args.delimiter)

if __name__ == "__main__":
    main()