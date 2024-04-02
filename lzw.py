import os
import sys
from sys import argv
from struct import *

file_path = "xml"
file_out = "xml"

with open(file_path, "rb") as file:
    
    silesia_concat = file.read()

    # max size = 4096, 32768, 262144, 2097152
    maximum_table_size = 4096
    print(maximum_table_size)
    dictionary_size = 256

    dictionary = {chr(i): i for i in range(dictionary_size)}    
    string = ""             # String is null.
    compressed_data = []    # variable to store the compressed data.

    length = len(silesia_concat)

    for i, symbol in enumerate(silesia_concat):
        
        symbol = chr(symbol)
        
        if (i % 100000 == 0):
            print(f"Progress: {i / length * 100:.2f}%")

        string_plus_symbol = string + symbol # get input symbol.
        if string_plus_symbol in dictionary: 
            string = string_plus_symbol
        else:
            compressed_data.append(dictionary[string])
            if(len(dictionary) <= maximum_table_size):
                dictionary[string_plus_symbol] = dictionary_size
                dictionary_size += 1
            string = symbol
        

    if string in dictionary:
        compressed_data.append(dictionary[string])

    output_file = open(file_out + ".lzw", "wb")


    for data in compressed_data:

        total_bytes = data.bit_length() // 8 + 1
        
        if total_bytes <= 1:
            output_file.write(pack('>B', data))
        elif total_bytes <= 2:
            output_file.write(pack('>H',  data))
        elif total_bytes <= 4:
            output_file.write(pack('>I', data))
        elif total_bytes <= 8:
            output_file.write(pack('>Q', data))

        
    output_file.close()
    file.close()
