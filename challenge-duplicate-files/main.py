import argparse
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

def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Recursively find potential duplicate files in a directory based on file size.")
    
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

    for key, value in files_by_size.items():
        if len(value) > 1:
            print(f"Potential Duplicate Files: {value}")

if __name__ == "__main__":
    main()