import os
import sys
from sys import argv
from struct import *

file_path = "data/silesia_concat/concat_file"
file_out = "data/silesia_concat/concat_file"

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
            print(f"Progress encoding: {i / length * 100:.2f}%")

        string_plus_symbol = string + symbol # get input symbol.
        if string_plus_symbol in dictionary: 
            string = string_plus_symbol
        else:
            compressed_data.append(dictionary[string])
            if(len(dictionary) <= maximum_table_size):
                dictionary[string_plus_symbol] = dictionary_size
                dictionary_size += 1
            string = symbol
        


    output_file = open(file_out + ".lzw", "wb")
    
    all_bytes = []

    print("Making bytes: ")
    for i, data in enumerate(compressed_data):
        if (i % 100000 == 0):
            print(f"Progress bytes: {i / len(compressed_data) * 100:.2f}%")
        
        p = data.bit_length()
        all_bytes.append(format(data, f'0{p}b'))

    
    current_bytes = ""

    print("Writing binary: ")
    for i, byte in enumerate(all_bytes):

        if (i % 100000 == 0):
            print(f"Progress write binary: {i / len(compressed_data) * 100:.2f}%")

        current_bytes += byte
        while len(current_bytes) >= 8:
            output_file.write(pack('B', int(current_bytes[:8], 2)))
            current_bytes = current_bytes[8:]

        
    output_file.close()
    file.close()
