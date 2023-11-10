import os

# Define the root directory to start traversal from
root_dir = 'evaluations'

# Define the code file extensions to look for
code_file_extensions = ('.py', '.js', '.java', '.c')

# Define the output file
output_file = 'folder_structure_and_code.txt'

prompt = "Extract all of the information you need from this file in order to help create a readme for the overall project."

# Initialize a list to hold the folder structure and file contents
folder_structure = []

# Function to traverse the directory and process files
def process_directory(directory):
    for entry in os.scandir(directory):
        if entry.is_dir(follow_symlinks=False):
            # Add directory path to the folder structure
            folder_structure.append(f'(Directory) {entry.path}\n')
            # Recursively process the subdirectory
            process_directory(entry.path)
        elif entry.is_file() and entry.name.endswith(code_file_extensions):
            # Add file path to the folder structure
            folder_structure.append(f'(Code File) {entry.path}\n')
            # Read and store the file content with delimiters
            with open(entry.path, 'r', encoding='utf-8') as file:
                content = file.read()
                delimiter = f'\n\n========== START OF {entry.path} ==========\n\n'
                folder_structure.append(delimiter)
                folder_structure.append(content)
                folder_structure.append(f'\n\n========== END OF {entry.path} ==========\n\n')

# Start processing from the root directory
process_directory(root_dir)

# Write the folder structure and file contents to the output file
with open(output_file, 'w', encoding='utf-8') as file:
    file.writelines(folder_structure)

print(f'Folder structure and code files have been written to {output_file}')
