import os
import sys
from sys import argv
from struct import *

file_path = "data_test/texto.lzw"

with open(file_path, "rb") as file:
    
    silesia_concat = file.read()

# max size = 4096, 32768, 262144, 2097152
maximum_table_size = 4096
dictionary_size = 256

dictionary = {i:chr(i) for i in range(dictionary_size)}    
string = ""             
descompressed_data = ""   

length = len(silesia_concat)

todos_os_bytes = []


i_byte = 0
string = ""
p = 9
bytes_atuais = ""

all_bytes_int = []

while True:

    p = (dictionary_size).bit_length()

    while len(bytes_atuais) < p and (length) > i_byte:
        bytes_atuais += "".join(format(silesia_concat[i_byte], '08b'))
        i_byte += 1

        if (i_byte % 100000 == 0):
            print(f"(p = {p}) Progress decoding: {i_byte / length * 100:.2f}%")
            
        
    

    code = int(bytes_atuais[:p], 2)
    bytes_atuais = bytes_atuais[p:]


    if not (code in dictionary):
        dictionary[code] = string + (string[0])

    descompressed_data += dictionary[code]

    if not(len(string) == 0):
        dictionary[dictionary_size] = string + (dictionary[code][0])
        dictionary_size += 1
    
    string = dictionary[code]

    if (length) == i_byte:
        print(bytes_atuais)
        break


output_file = open(file_path.split('.')[0] + "_descompressed", "wb")
for i, char in enumerate(descompressed_data):
    if (i % 100000 == 0):
        print(f"Progress write binary: {i / len(descompressed_data) * 100:.2f}%")

    output_file.write(pack('B', ord(char)))

output_file.close()
