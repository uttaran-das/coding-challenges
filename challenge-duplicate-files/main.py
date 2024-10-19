import argparse
import os

def list_files_recursively(directory):
    """
    Recursively lists all files in the given directory.
    
    :param directory: The directory to scan.
    """
    try:
        # Iterate over all items in the directory
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            
            if os.path.isfile(item_path):
                # If the item is a file, print its path
                print(item_path)
            elif os.path.isdir(item_path):
                # If the item is a directory, recursively list its files
                list_files_recursively(item_path)
    except Exception as e:
        print(f"Error accessing directory {directory}: {e}")

def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Recursively list all files in a directory.")
    
    # Add the directory path argument
    parser.add_argument("directory", help="The directory to scan.")
    
    # Parse the command-line arguments
    args = parser.parse_args()
    
    # Check if the provided path is a valid directory
    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a valid directory.")
        return
    
    # List all files recursively
    list_files_recursively(args.directory)

if __name__ == "__main__":
    main()