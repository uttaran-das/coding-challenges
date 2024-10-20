import argparse
import hashlib
import os

def find_potential_duplicates(directory, files_by_size):
    """
    Recursively finds potential duplicate files in the given directory based on file size.
    
    :param directory: The directory to scan.
    :param files_by_size: Dictionary to store the size and corresponding files
    """
    try:
        # Iterate over all items in the directory
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            
            if os.path.isfile(item_path):
                # Get the size of the file
                file_size = os.path.getsize(item_path)

                # Check if this size is not recorded
                if file_size not in files_by_size:
                    files_by_size[file_size] = set()

                # Add the file in the file_size set
                files_by_size[file_size].add(item_path)
            elif os.path.isdir(item_path):
                # If the item is a directory, recursively find potential duplicates
                find_potential_duplicates(item_path, files_by_size)
    except Exception as e:
        print(f"Error accessing directory {directory}: {e}")


def calculate_md5(file_path, block_size=2**20):
    """
    Calculate the MD5 hash of a file.
    
    :param file_path: The path to the file.
    :param block_size: The size of the block to read at a time.
    :return: The MD5 hash of the file.
    """
    md5 = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(block_size)
                if not data:
                    break
                md5.update(data)
        return md5.hexdigest()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None


def find_duplicate_files(files_by_size):
    """
    Find duplicate files based on MD5 hash.
    
    :param files_by_size: Dictionary containing files grouped by size.
    :return: Dictionary containing files grouped by MD5 hash.
    """
    files_by_md5 = {}
    
    for size, files in files_by_size.items():
        if len(files) > 1:
            for file_path in files:
                file_md5 = calculate_md5(file_path)
                if file_md5:
                    if file_md5 not in files_by_md5:
                        files_by_md5[file_md5] = set()
                    files_by_md5[file_md5].add(file_path)
    
    return files_by_md5


def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Recursively find potential duplicate files in a directory based on file size and MD5 hash.")
    
    # Add the directory path argument
    parser.add_argument("directory", help="The directory to scan.")
    
    # Parse the command-line arguments
    args = parser.parse_args()
    
    # Check if the provided path is a valid directory
    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a valid directory.")
        return
    
    # Dictionary to store the size and corresponding files
    files_by_size = {}

    # Find potential duplicates
    find_potential_duplicates(args.directory, files_by_size)

    # Find duplicate files based on MD5 hash
    files_by_md5 = find_duplicate_files(files_by_size)

    for md5, files in files_by_md5.items():
        if len(files) > 1:
            print(f"Duplicate Files (MD5: {md5}): {files}")

if __name__ == "__main__":
    main()