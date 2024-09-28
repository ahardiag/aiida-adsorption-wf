import os
import re
import shutil

def check_filenames(directory):
    # Regex pattern to find non-alphanumeric and non-underscore characters
    pattern = re.compile(r'[^a-zA-Z0-9_]')

    # Variable to track if any invalid filenames are found
    warning_flag = False
    count_warn = 0

    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Get the filename without the extension
            filename_without_extension = os.path.splitext(file)[0]

            # Search for non-alphanumeric or underscore characters
            if pattern.search(filename_without_extension):
                # Print a warning message with the filename
                print(f"Warning: Invalid filename found - {file}")
                warning_flag = True
                count_warn+=1

    # If no invalid filenames found, print all clear message
    if not warning_flag:
        print("All filenames are valid.")
    return count_warn


def copy_and_rename_directory(source_directory, target_directory_suffix='_converted'):
    # Create the target directory with the specified suffix
    target_directory = f"{source_directory}{target_directory_suffix}"
    os.makedirs(target_directory, exist_ok=True)
    print(target_directory)

    # Regex pattern to replace non-alphanumeric or underscore characters
    pattern = re.compile(r'[^a-zA-Z0-9_]')

    count_modif = 0

    # Iterate through all files in the source directory
    for filename in os.listdir(source_directory):
        # Split the filename into name and extension
        file_base, file_extension = os.path.splitext(filename)
        
        # Replace non-alphanumeric or underscore characters in the filename part
        sanitized_filename = pattern.sub('_', file_base) + file_extension

        # Define source and target file paths
        source_file = os.path.join(source_directory, filename)
        target_file = os.path.join(target_directory, sanitized_filename)

        # Copy file from source to target directory
        shutil.copy(source_file, target_file)
        count_modif+=1
        print(f"Copied and renamed {filename} to {sanitized_filename}")

    print(f'Number of filename converted in {source_directory+target_directory_suffix} : {count_modif}')

def main():
    # Directory to check
    source_directory = 'examples/subset-coremof/cif'

    # Check filenames
    count_warn = check_filenames(source_directory)
    print(f'Number of uncorrected formatted text files : {count_warn}')

    # Create new valid directory
    copy_and_rename_directory(source_directory)

if __name__ == '__main__':
    main()
