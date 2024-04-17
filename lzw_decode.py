import os
import sys
from sys import argv
from struct import *

file_path = "texto.lzw"

with open(file_path, "rb") as file:
    
    silesia_concat = file.read()

# max size = 4096, 32768, 262144, 2097152
maximum_table_size = 4096
dictionary_size = 256

dictionary = {i:chr(i) for i in range(dictionary_size)}    
string = ""             # String is null.
descompressed_data = ""    # variable to store the compressed data.

length = len(silesia_concat)

todos_os_bytes = []
for i, symbol in enumerate(silesia_concat):
    if (i % 10000 == 0):
        print(f"Progress reading: {i / length * 100:.2f}%")    
    todos_os_bytes.append(format(symbol, '08b'))

string = ""
p = 9
bytes_atuais = "".join(todos_os_bytes[0])
todos_os_bytes.pop(0)

all_bytes_int = []

while True:
    if (dictionary_size == 264):
        print("aqui")
    p = (dictionary_size).bit_length()
    #'0011101'
    while len(bytes_atuais) < p and len(todos_os_bytes) > 0:
        bytes_atuais += "".join(todos_os_bytes[0])
        todos_os_bytes.pop(0)

    key_dict = int(bytes_atuais[:p], 2)
    bytes_atuais = bytes_atuais[p:]

    all_bytes_int.append(key_dict)

    symbol = dictionary[key_dict]
    string_plus_symbol = string + symbol

    if string_plus_symbol in dictionary.values(): 
        # descompressed_data += dictionary[key_dict]
        string = string_plus_symbol
    else:
        descompressed_data += string # dictionary[key_dict]
        if(len(dictionary) <= maximum_table_size):
            dictionary[dictionary_size] = string_plus_symbol
            dictionary_size += 1
        string = symbol
    
    # print("len:", len(todos_os_bytes))

    if len(todos_os_bytes) < 1 and len(bytes_atuais) < p:
        break

print(all_bytes_int)

with open("dict_decoder.txs", "w") as file:
    for key, value in dictionary.items():
        if key > 255:
            file.write(f"{value}:{key}\n")

output_file = open(file_path.split('.')[0] + "_descompressed", "wb")
for i, char in enumerate(descompressed_data):
    if (i % 100000 == 0):
        print(f"Progress write binary: {i / len(descompressed_data) * 100:.2f}%")

    output_file.write(pack('B', ord(char)))

output_file.close()
