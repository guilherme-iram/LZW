import os
import sys
from sys import argv
from struct import *

file_path = "texto"

with open(file_path, "rb") as file:
    
    silesia_concat = file.read()

    # max size = 4096, 32768, 262144, 2097152
    maximum_table_size = 4096

    dictionary_size = 256

    dictionary = {chr(i): i for i in range(dictionary_size)}    
    string = ""             

    length = len(silesia_concat)

    all_bytes = []
    all_bytes_str = []
    all_bytes_keydict = []

    for i, symbol in enumerate(silesia_concat):
        
        symbol = chr(symbol)
        
        if (i % 100000 == 0):
            print(f"Progress encoding: {i / length * 100:.2f}%")

        string_plus_symbol = string + symbol 
        
        if string_plus_symbol in dictionary: 
            string = string_plus_symbol
        else:

            p = (dictionary_size).bit_length()
            all_bytes.append(format(dictionary[string], f'0{p}b'))
            all_bytes_str.append(string)

            if(len(dictionary) <= maximum_table_size):
                dictionary[string_plus_symbol] = dictionary_size
                dictionary_size += 1
            
            string = symbol
            
        if i == length - 1:
            p = (dictionary_size).bit_length()
            all_bytes.append(format(dictionary[string], f'0{p}b'))
            all_bytes_str.append(string)


    # convert in int
    all_bytes_int = [int(byte, 2) for byte in all_bytes]
    print(all_bytes_int)


    print(all_bytes_str)

    with open("dict_encoder.txs", "w") as file:
        for key, value in dictionary.items():
            if value > 255:
                file.write(f"{key}:{value}\n")

    output_file = open(file_path + ".lzw", "wb")
    
    current_bytes = ""

    print("Writing binary: ")

    for i, byte in enumerate(all_bytes):

        current_bytes += byte

        while len(current_bytes) >= 8:
            
            bits_to_write = current_bytes[:8]
            to_write = int(bits_to_write, 2)
            output_file.write(pack('B', to_write))
            current_bytes = current_bytes[8:]

            if i == len(all_bytes) - 1:
                diff = 8 - len(current_bytes)
                to_write_eof =   current_bytes + ('0' * diff) 
                output_file.write(pack('<B', int(to_write_eof, 2)))
                
            
    output_file.close()
    file.close()
