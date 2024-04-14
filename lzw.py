import os
import sys
from sys import argv
from struct import *

file_path = "xml"

with open(file_path, "rb") as file:
    
    silesia_concat = file.read()

    # max size = 4096, 32768, 262144, 2097152
    maximum_table_size = 4096
    # print(maximum_table_size)
    dictionary_size = 256

    dictionary = {chr(i): i for i in range(dictionary_size)}    
    string = ""             # String is null.

    length = len(silesia_concat)
    # add EOF to the end of the file
    # silesia_concat += b'EOF'
    # print(silesia_concat[:1])
    all_bytes = []
    all_bytes_str = []

    for i, symbol in enumerate(silesia_concat):
        
        if i == 9:
            print("qualquer coisa")
        symbol = chr(symbol)
        
        if (i % 100000 == 0):
            print(f"Progress encoding: {i / length * 100:.2f}%")

        # print(symbol)
        string_plus_symbol = string + symbol # get input symbol.
        
        if string_plus_symbol in dictionary: 
            string = string_plus_symbol
            # condition to get the EOF
            
        else:

            p = (dictionary_size).bit_length()
            all_bytes.append(format(dictionary[string], f'0{p}b'))
            all_bytes_str.append(string)
            if(len(dictionary) < maximum_table_size):
                dictionary[string_plus_symbol] = dictionary_size
                dictionary_size += 1
            
            string = symbol
            
        if i == length - 1:
            p = (dictionary_size).bit_length()
            all_bytes.append(format(dictionary[string], f'0{p}b'))
            all_bytes_str.append(string)
    # print(compressed_data)
    # print(dictionary)

    output_file = open(file_path + ".lzw", "wb")
    


    # print("Making bytes: ")
    # for i, data in enumerate(compressed_data):
    #     if (i % 100000 == 0):
    #         print(f"Progress bytes: {i / len(compressed_data) * 100:.2f}%")
        
    #     p = data.bit_length()
    #     if p < 8:
    #         p = 8
    #     # print(data, ": ", p, " - bin: ", format(data, f'0{p}b'))
    #     all_bytes.append(format(data, f'0{p}b'))
    #     # all_bytes.append(format(data, f"{0:p}b"))

    current_bytes = ""

    print("Writing binary: ")
    for i, byte in enumerate(all_bytes):

        # if (i % 100000 == 0):
          #   print(f"Progress write binary: {i / len(compressed_data) * 100:.2f}%")

        current_bytes += byte

        while len(current_bytes) >= 8:
            
            bits_to_write = current_bytes[:8]
            to_write = int(bits_to_write, 2)
            output_file.write(pack('B', to_write))
            current_bytes = current_bytes[8:]

            if i == len(all_bytes) - 1:
                diff = 8 - len(current_bytes)
                to_write_eof =  ('0' * diff) + current_bytes
                output_file.write(pack('B', int(to_write_eof, 2)))
                
            
    output_file.close()
    file.close()
