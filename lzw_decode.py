import os
import sys
from struct import *

file_path = "abracadabra.lzw"

with open(file_path, "rb") as file:
    compressed_data = file.read()

    maximum_table_size = 4096
    dictionary_size = 256
    dictionary = {i: chr(i) for i in range(dictionary_size)}

    string = chr(compressed_data[0])
    output = [string]

    code_size = 8
    next_code = 256

    buffer = 0
    buffer_length = 0

    i = 1
    while i < len(compressed_data):
        code = compressed_data[i]

        buffer |= code << buffer_length
        buffer_length += 8
        i += 1

        while buffer_length >= code_size:
            current_code = buffer & ((1 << code_size) - 1)
            buffer >>= code_size
            buffer_length -= code_size

            if current_code == 256:
                code_size = 8
                next_code = 256
                continue

            if current_code in dictionary:
                entry = dictionary[current_code]
            elif current_code == next_code:
                entry = string + string[0]
            else:
                raise ValueError('Bad compressed code')

            output.append(entry)

            if next_code < maximum_table_size:
                dictionary[next_code] = string + entry[0]
                next_code += 1

            string = entry

    decompressed_data = ''.join(output)

    print("Decompressed data:", decompressed_data)
