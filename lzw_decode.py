import os
import sys
from sys import argv
from struct import *

file_path = "abracadabra.lzw"

with open(file_path, "rb") as file:
    
    silesia_concat = file.read()

# max size = 4096, 32768, 262144, 2097152
maximum_table_size = 4096
print(maximum_table_size)
dictionary_size = 256

dictionary = {i:chr(i) for i in range(dictionary_size)}    
string = ""             # String is null.
compressed_data = []    # variable to store the compressed data.

length = len(silesia_concat)
# add EOF to the end of the file
# silesia_concat += b'EOF'

todos_os_bytes = ''
for i, symbol in enumerate(silesia_concat):
    print(symbol)
    
    todos_os_bytes += format(symbol, '08b')
    
    
    symbol = chr(symbol)

print(todos_os_bytes)   

string_bit = b'0'
c = 8
j = 0

while True:
    symbol_bit = int(todos_os_bytes[:c], 2)
    
    symbol = dictionary[symbol_bit]
    # if j > 0:
    #     ch1 = dictionary[int(string, 2)] # get the string value from the dictionary
    # ch2 = dictionary[int(symbol, 2)] # get the symbol value from the dictionary
    string_plus_symbol = string + symbol # get input symbol.
    string_plus_symbol_bit = bin(int(string_bit, 2) + symbol_bit)

    if (i % 100000 == 0):
        print(f"Progress encoding: {i / length * 100:.2f}%")

    if string_plus_symbol in dictionary.values(): 
        string = string_plus_symbol
        string_bit = string_plus_symbol_bit
        # condition to get the EOF
        # if i == length - 1:
        #     compressed_data.append(dictionary[string])
    else:
        #length -= len(string)
        compressed_data.append(dictionary[int(string_bit, 2)])
        if(len(dictionary) <= maximum_table_size):
            dictionary[dictionary_size] = string_plus_symbol
            dictionary_size += 1
        string = symbol
        string_bit = bin(symbol_bit)
        
    c = int(string_plus_symbol_bit, 2).bit_length()
    
    if c < 8:
        c = 8
    j += 1
    
    todos_os_bytes = todos_os_bytes[c:]
        
    # print(compressed_data)
    # print(dictionary)

    # output_file = open(file_path + ".lzw", "wb")
    
    # all_bytes = []

    # print("Making bytes: ")
    # for i, data in enumerate(compressed_data):
    #     if (i % 100000 == 0):
    #         print(f"Progress bytes: {i / len(compressed_data) * 100:.2f}%")
        
    #     p = data.bit_length() + 1
    #     all_bytes.append(format(data, f'0{p}b'))
    
    # current_bytes = ""

    # print(all_bytes)
    # print("Writing binary: ")
    # for i, byte in enumerate(all_bytes):

    #     if (i % 100000 == 0):
    #         print(f"Progress write binary: {i / len(compressed_data) * 100:.2f}%")

    #     current_bytes += byte
    #     print(current_bytes)
    #     while len(current_bytes) >= 8:
    #         bits_to_write = current_bytes[:8]
    #         to_write = int(bits_to_write, 2)
    #         output_file.write(pack('B', to_write))
    #         current_bytes = current_bytes[8:]
    #         if i == len(all_bytes) - 1:
    #             diff = 8 - len(current_bytes)
    #             to_write_eof =  ('0' * diff) + current_bytes
    #             output_file.write(pack('B', int(to_write_eof, 2)))
                
            
    # output_file.close()
    # file.close()
