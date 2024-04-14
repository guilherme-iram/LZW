import os
import sys
from sys import argv
from struct import *

file_path = "xml.lzw"

with open(file_path, "rb") as file:
    
    silesia_concat = file.read()

# max size = 4096, 32768, 262144, 2097152
maximum_table_size = 4096
print(maximum_table_size)
dictionary_size = 256

dictionary = {i:chr(i) for i in range(dictionary_size)}    
string = ""             # String is null.
descompressed_data = ""    # variable to store the compressed data.

length = len(silesia_concat)
# add EOF to the end of the file
# silesia_concat += b'EOF'

todos_os_bytes = ''
for i, symbol in enumerate(silesia_concat):
    if (i % 100000 == 0):
        print(f"Progress reading: {i / length * 100:.2f}%")    
    todos_os_bytes += format(symbol, '08b')

# string_bit = b'0'
c = 8
j = 0
string = ""
p = 8
while True:

    p = (dictionary_size).bit_length()
    # all_bytes.append(format(dictionary[string], f'0{p}b'))

    key_dict = int(todos_os_bytes[:p], 2)
    
    symbol = dictionary[key_dict]

    string_plus_symbol = string + symbol

    if string_plus_symbol in dictionary.values(): 
        descompressed_data += dictionary[key_dict]
        string = string_plus_symbol

        # condition to get the EOF
        # if i == length - 1:
          #   compressed_data.append(dictionary[string])
    else:
        #length -= len(string)
        descompressed_data += dictionary[key_dict]
        if(len(dictionary) <= maximum_table_size):
            dictionary[dictionary_size] = string_plus_symbol
            dictionary_size += 1
        string = symbol

    todos_os_bytes = todos_os_bytes[p:]
    print("len:", len(todos_os_bytes))
    if (len(todos_os_bytes) < 8):
        break


output_file = open(file_path.split('.')[0] + "_descompressed.lzw", "wb")
for i, char in enumerate(descompressed_data):
    if (i % 100000 == 0):
        print(f"Progress write binary: {i / len(descompressed_data) * 100:.2f}%")

    output_file.write(pack('B', ord(char)))

output_file.close()
