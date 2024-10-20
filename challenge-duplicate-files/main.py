import argparse
import hashlib
import os

def find_potential_duplicates(directory, files_by_size, min_file_size):
    """
    Recursively finds potential duplicate files in the given directory based on file size.
    
    :param directory: The directory to scan.
    :param files_by_size: Dictionary to store the size and corresponding files
    :param min_file_size: Minimum file size to consider.
    """
    try:
        # Iterate over all items in the directory
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            
            if os.path.isfile(item_path):
                # Get the size of the file
                file_size = os.path.getsize(item_path)

                # Check if the file size meets the minimum size requirement
                if file_size >= min_file_size:
                    # Check if this size is not recorded
                    if file_size not in files_by_size:
                        files_by_size[file_size] = set()

                    # Add the file in the file_size set
                    files_by_size[file_size].add(item_path)
            elif os.path.isdir(item_path):
                # If the item is a directory, recursively find potential duplicates
                find_potential_duplicates(item_path, files_by_size, min_file_size)
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


def are_files_identical(file1, file2, block_size=2**20):
    """
    Compare two files byte by byte to determine if they are identical.
    
    :param file1: Path to the first file.
    :param file2: Path to the second file.
    :param block_size: Size of the block to read at a time.
    :return: True if files are identical, False otherwise.
    """
    try:
        with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
            while True:
                block1 = f1.read(block_size)
                block2 = f2.read(block_size)
                if block1 != block2:
                    return False
                if not block1:
                    return True
    except Exception as e:
        print(f"Error comparing files {file1} and {file2}: {e}")
        return False


def is_file_in_groups(file_path, identical_groups):
    """
    Check if a file is already in any of the groups.
    
    :param file_path: Path to the file to check.
    :param identical_groups: List of lists where each sublist contains identical files.
    :return: True if the file is in any group, False otherwise.
    """
    for group in identical_groups:
        if file_path in group:
            return True
    return False


def group_files(files_list, identical_groups):
    """
    Group files from a list into identical groups.
    
    :param files_list: List of file paths to group.
    :param identical_groups: List of lists where each sublist contains identical files.
    """
    for i in range(len(files_list)):
        if not is_file_in_groups(files_list[i], identical_groups):
            new_group = [files_list[i]]
            for j in range(i + 1, len(files_list)):
                if are_files_identical(files_list[i], files_list[j]):
                    new_group.append(files_list[j])
            identical_groups.append(new_group)


def group_identical_files(files_by_md5):
    """
    Group identical files together.
    
    :param files_by_md5: Dictionary containing files grouped by MD5 hash.
    :return: List of lists where each sublist contains identical files.
    """
    identical_groups = []
    
    for md5, files in files_by_md5.items():
        if len(files) > 1:
            files_list = list(files)
            group_files(files_list, identical_groups)
    
    return identical_groups


def display_identical_files(group):
    """
    Display the list of identical files with numbered options.
    
    :param group: List of identical file paths.
    """
    print("Identical Files:")
    for i, file_path in enumerate(group, start=1):
        print(f"{i}. {file_path}")


def get_user_choice(group):
    """
    Prompt the user to enter the number of the file to keep.
    
    :param group: List of identical file paths.
    :return: The user's choice (0 to skip, or the number of the file to keep).
    """
    while True:
        try:
            choice = int(input("Enter the number of the file to keep (0 to skip): "))
            if 0 <= choice <= len(group):
                return choice
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def delete_duplicate_files(group, choice):
    """
    Delete all files in the group except the one specified by the user.
    
    :param group: List of identical file paths.
    :param choice: The number of the file to keep.
    """
    file_to_keep = group[choice - 1]
    for file_path in group:
        if file_path != file_to_keep:
            os.remove(file_path)
            print(f"Deleted: {file_path}")

def prompt_user_to_keep_file(group):
    """
    Prompt the user to keep a particular file and delete the rest.
    
    :param group: List of identical file paths.
    """
    if len(group) < 2:
        return
    
    display_identical_files(group)
    choice = get_user_choice(group)
    
    if choice != 0:
        delete_duplicate_files(group, choice)

def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Recursively find potential duplicate files in a directory based on file size and MD5 hash.")
    
    # Add the directory path argument
    parser.add_argument("directory", help="The directory to scan.")

    # Add the optional minimum file size argument
    parser.add_argument("--minsize", type=int, default=0, help="Minimum file size to consider (in bytes).")
    
    # Parse the command-line arguments
    args = parser.parse_args()
    
    # Check if the provided path is a valid directory
    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a valid directory.")
        return
    
    # Dictionary to store the size and corresponding files
    files_by_size = {}

    # Find potential duplicates
    find_potential_duplicates(args.directory, files_by_size, args.minsize)

    # Find duplicate files based on MD5 hash
    files_by_md5 = find_duplicate_files(files_by_size)

    # Group identical files together
    identical_groups = group_identical_files(files_by_md5)

    # Prompt the user to keep a particular file and delete the rest
    for group in identical_groups:
        prompt_user_to_keep_file(group)

if __name__ == "__main__":
    main()