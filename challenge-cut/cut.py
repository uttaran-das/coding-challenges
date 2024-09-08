import argparse

def cut_field(file_path, field_number):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                fields = line.strip().split('\t');
                if len(fields) >= field_number:
                    print(fields[field_number-1])
                else:
                    print("")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"Error: The file '{file_path}' was not found.")

def main():
    parser = argparse.ArgumentParser(description="Extract a specified field from each line of a tab-separated file.")
    parser.add_argument('-f', '--field', type=int, default=1, help='Field number to extract (default is 1)')
    parser.add_argument('file', help='Path to the tab-separated file')
    args = parser.parse_args()

    cut_field(args.file, args.field)

if __name__ == "__main__":
    main()