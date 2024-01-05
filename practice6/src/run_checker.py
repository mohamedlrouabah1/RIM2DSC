import sys
import os

def check_file(file_path):
    try:
        with open(file_path, 'r') as file:
            for line_number, line in enumerate(file, start=1):
                columns = line.strip().split(' ')
                # Check if the line has exactly 7 columns
                if len(columns) != 7:
                    print(f"File: {file_path}, Line: {line_number} - Incorrect number of columns")

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def main(directory_path):
    # Check if the directory exists
    if not os.path.exists(directory_path):
        print(f"Error: Directory '{directory_path}' does not exist.")
        sys.exit(1)

    # Iterate through each file in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        # Check if the item is a file (not a subdirectory)
        if os.path.isfile(file_path):
            check_file(file_path)

if __name__ == "__main__":
    # Check if a directory path is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python check_files.py <directory_path>")
        sys.exit(1)

    directory_path = sys.argv[1]
    main(directory_path)

    print("Done!")