import os
import sys
from struct import *

# Path to the directory containing Silesia corpus files
corpus_dir = "data/silesia_corpus"

# Path to the output file where all files will be concatenated
output_file_path = "data/silesia_concat/concat_file"


# Function to read a file in binary mode
def read_file_in_binary(file_path):
    with open(file_path, "rb") as file:
        return file.read()


# List all files in the Silesia corpus directory
corpus_files = os.listdir(corpus_dir)

# Open the output file in binary write mode
with open(output_file_path, "wb") as output_file:
    # Iterate through each file in the corpus directory

    total_size = 0

    for file_name in corpus_files:
        file_path = os.path.join(corpus_dir, file_name)
        if os.path.isfile(file_path):

            # print the file name and size
            print(file_name, os.path.getsize(file_path))
            total_size += os.path.getsize(file_path)
            # Read the binary content of the file
            file_content = read_file_in_binary(file_path)
            # Write the content to the output file
            output_file.write(file_content)


print("Concatenation complete. Output file:", output_file_path)
print("Total size:", os.path.getsize(output_file_path), "bytes")
print("Total size of the files:", total_size, "bytes")
