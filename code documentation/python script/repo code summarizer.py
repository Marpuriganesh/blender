import re
import os
import csv
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import git

# initialize the Git repository object
repo = git.Repo('.')

# Regular expressions to match different elements in a C/C++ file
class_regex = r'class\s+(\w+)\s*\{'
function_regex = r'\w+\s+(\w+)\(.*\)'
enum_regex = r'enum\s+(\w+)\s*\{'
struct_regex = r'struct\s+(\w+)\s*\{'
macro_regex = r'#define\s+(\w+)'
include_regex = r'#include\s+[<"](.*)[>"]'

# Function to parse the given file and return the required information
def parse_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        contents = f.read()

    # Extract classes
    classes = re.findall(class_regex, contents, re.MULTILINE)

    # Extract functions
    functions = re.findall(function_regex, contents)

    # Extract enums
    enums = re.findall(enum_regex, contents)

    # Extract structs
    structs = re.findall(struct_regex, contents)

    # Extract macros
    macros = re.findall(macro_regex, contents)

    # Extract included files
    includes = re.findall(include_regex, contents)

    # Get last modified file date and time
    last_modified = os.path.getmtime(file_path)
    last_modified_time = datetime.fromtimestamp(last_modified).strftime('%Y-%m-%d %H:%M:%S')

    return file_path, classes, functions, enums, structs, macros, includes, last_modified_time

# Get a list of all C/C++ files in the current directory
# Set the directory path to start the search from
directory_path = '.'

# Initialize a list to store the C/C++ files found
cpp_files = []

# Walk through the directory tree and look for C/C++ files
for root, dirs, files in os.walk(directory_path):
    for file in files:
        if file.endswith('.c') or file.endswith('.cpp') or file.endswith('.h') or file.endswith('.hpp') or  file.endswith('.cc') or  file.endswith('.hh'):
            # Add the file path to the list of C/C++ files found
            cpp_files.append(os.path.join(root, file))

# Create a CSV file to store the parsed information
csv_file_path = 'code documentation/parsed_data.csv'

# Check if the CSV file already exists
csv_file_exists = os.path.isfile(csv_file_path)

with open(csv_file_path, 'a', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)

    # Write the header row if the CSV file was just created
    if not csv_file_exists:
        writer.writerow(['File Name', 'Classes', 'Functions', 'Enums', 'Structs', 'Macros', 'Included Files', 'Last Modified'])

        with ThreadPoolExecutor(max_workers=4) as executor:
        # Loop through all C/C++ files and parse their contents
            for file_data in tqdm(executor.map(parse_file, cpp_files), total=len(cpp_files),desc='Parsing files', ncols=80,dynamic_ncols=True):
                file_name, classes, functions, enums, structs, macros, includes, last_modified = file_data
                
                # Write the parsed data to the CSV file
                writer.writerow([file_name, ', '.join(classes), ', '.join(functions), ', '.join(enums), ', '.join(structs), ', '.join(macros), ', '.join(includes), last_modified])
    # searching for modified files
    modified_files = [item.a_path for item in repo.index.diff(None)]
    # checking if we have any modified files and reparsing them
    if len(modified_files)!=0:
        with ThreadPoolExecutor(max_workers=4) as executor:
        # Loop through all C/C++ files and parse their contents
            for file_data in tqdm(executor.map(parse_file, modified_files), total=len(modified_files),desc='Parsing files', ncols=80,dynamic_ncols=True):
                file_name, classes, functions, enums, structs, macros, includes, last_modified = file_data

                # Write the parsed data to the CSV file
                writer.writerow([file_name, ', '.join(classes), ', '.join(functions), ', '.join(enums), ', '.join(structs), ', '.join(macros), ', '.join(includes), last_modified])
    else:
        print("----- your good to go no files are modified")
    
    print("----- completed parsing the files")
