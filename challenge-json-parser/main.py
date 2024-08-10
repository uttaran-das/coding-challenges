import argparse
import sys


def read_file_content(filepath):
    with open(filepath, 'r') as file:
        content = file.read()
        file.close()
        return content


def check_json_validity(content):
    if len(content) == 0:
        sys.exit(1)
    stack = []
    for char in content:
        if char == '}':
            found = False
            while len(stack) != 0:
                last_elem = stack.pop()
                if last_elem == '{':
                    found = True
                    break
            if not found:
                sys.exit(1)
        else:
            stack.append(char)
    if len(stack) != 0:
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath")
    args = parser.parse_args()
    fileContent = read_file_content(args.filepath)
    check_json_validity(fileContent)
    sys.exit(0)


if __name__ == "__main__":
    main()