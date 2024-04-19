from typing import Dict, List, Tuple
from io import TextIOWrapper
from struct import pack
import numpy as np
import matplotlib.pyplot as plt

ONE_BYTE = 8

class IOHandler:
    def __init__(self, path) -> None:
        self.read_path = f"./data_test/{path}"
        self.write_path = f"./data_test/{path}.lzw"
        self.write_decoded_path = f"./data_test/{path}.lzw.decoded"

    def read_file_to_encode(self) -> str:
        with open(self.read_path, "rb") as f:
            file = f.read()
        return file

    def write_file_to_encode(self, encoded_message):
        output_file: TextIOWrapper = open(self.write_path, "wb")
        
        i = 0
        print("START - WRITE FILE TO ENCODE")
        
        current_bytes = encoded_message.pop(0)

        while len(encoded_message) > 0:

            if len(current_bytes) < ONE_BYTE:
                current_bytes += encoded_message.pop(0) 

            bits_to_write = current_bytes[:ONE_BYTE]
            to_write = int(bits_to_write, 2)
            output_file.write(pack("B", to_write))
            current_bytes = current_bytes[ONE_BYTE:]

        if len(current_bytes) > 0:
            bits_to_write = current_bytes
            diff = ONE_BYTE - len(bits_to_write)
            bits_to_write = bits_to_write + ("0" * diff)
            to_write = int(bits_to_write, 2)
            output_file.write(pack("B", to_write))

        output_file.close()
        print("DONE - WRITE FILE TO ENCODE")

    def read_file_to_decode(self) -> str:
        with open(self.write_path, "rb") as f:
            file = f.read()
        return [format(symbol, f"0{ONE_BYTE}b") for symbol in file]
    
    def write_file_to_decode(self, decoded_message: str) -> None:
        with open(self.write_decoded_path, "wb") as f:
            last_char = len(decoded_message) - 1
            for i, bits in enumerate(decoded_message):
                # if i != last_char:
                f.write(pack("B", ord(bits)))


def to_bin(integer: int, number_of_bits: int) -> str:
    return format(integer, f"0{number_of_bits}b")


def to_int(bin_formated: str) -> int:
    return int(bin_formated, 2)


class LZW:

    def __init__(self, maximum_table_size: int, dict_strategy: int) -> None:
        self.maximum_table_size = maximum_table_size
        self.dict_strategy = dict_strategy

    def encode(self, message: str) -> Tuple[str, List[int]]:
        dict_size: int = 255
        dictionary: dict = {chr(i): i for i in range(dict_size + 1)}

        found_chars: str = ""
        result = []
        bits_of_each_symbol: List[int] = []
        
        moving_avg_list = []
        sum_bit = 8

        str_debug = ""

        for i, char in enumerate(message):
            dict_bits_size: int = dict_size.bit_length()
            char = chr(char)
            chars_to_add: str = found_chars + char
            if chars_to_add in dictionary:
                found_chars = chars_to_add
            else:
                sum_bit += dict_bits_size
                result.append(to_bin(dictionary[found_chars], dict_bits_size))
                str_debug += found_chars
                bits_of_each_symbol.append(dict_bits_size)

                if dict_size < self.maximum_table_size:
                    dict_size += 1
                    dictionary[chars_to_add] = dict_size
                
                found_chars = char
                

            moving_avg_list.append(sum_bit / (i + 1))

        if len(found_chars) > 0:
            result.append(to_bin(dictionary[found_chars], dict_bits_size))
            str_debug += found_chars
            bits_of_each_symbol.append(dict_bits_size)

        print(dict_size)

        return result, bits_of_each_symbol, moving_avg_list

    def decode(self, encoded_message: List[str]) -> str:
        dict_size: int = 256
        dictionary: dict = {i: chr(i) for i in range(dict_size)}

        chars = chr(to_int(encoded_message[0]))
        result = chars

        encoded_message.pop(0)
        encoded_message_in_bits: str = "".join(encoded_message)

        while len(encoded_message_in_bits) > 0:
            dict_bits_size: int = dict_size.bit_length()
            code = to_int(encoded_message_in_bits[:dict_bits_size])

            entry: str = dictionary[code] if code in dictionary else chars + chars[0]
            result += entry

            if dict_size < (self.maximum_table_size + 2):
                dictionary[dict_size] = chars + entry[0]
                dict_size += 1
            chars = entry

            encoded_message_in_bits = encoded_message_in_bits[dict_bits_size:]

        print(dict_size)

        return result

MAX_LEN_DICT = [4096, 32768, 262144, 2097152]

l = LZW(MAX_LEN_DICT[0], 1)
io = IOHandler("republic")
m = io.read_file_to_encode()
r, b, moving_avg_list = l.encode(m)

io.write_file_to_encode(r)
print("Lendo arquivo codificado")
r_e = io.read_file_to_decode()
print("Decodificando ...")
r_d = l.decode(r_e)
print("Escrevendo arquivo decodificado...")
io.write_file_to_decode(r_d)
print("FIM")

# plt.plot(moving_avg_list)
# plt.show()

# original = ""
# has_error = False
# for i, j in zip(m, r_d):
#     original += chr(i)
#     if chr(i) != j:
#         print(chr(i), j, chr(i) == j)
#         has_error = True

# if not has_error:
#     print("DEU CERTO!")
