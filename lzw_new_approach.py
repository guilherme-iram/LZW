from typing import Dict, List, Tuple
from io import TextIOWrapper
from struct import pack
import numpy as np
import matplotlib.pyplot as plt
import time

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
        
        # current_bytes = encoded_message.pop(0)
        
        bits_array = "".join(encoded_message)

        while len(bits_array) >= ONE_BYTE:
            bits_to_write = bits_array[: ONE_BYTE]
            to_write = int(bits_to_write, 2)
            output_file.write(pack("B", to_write))
            bits_array = bits_array[ONE_BYTE:]

        if len(bits_array) > 0:
            bits_to_write = bits_array
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
        n = []

        for i, char in enumerate(message):
            dict_bits_size: int = dict_size.bit_length()
            char = chr(char)
            chars_to_add: str = found_chars + char
            if chars_to_add in dictionary:
                found_chars = chars_to_add
            else:
                sum_bit += dict_bits_size
                n.append(dictionary[found_chars])
                result.append(to_bin(dictionary[found_chars], dict_bits_size))
                str_debug += found_chars
                bits_of_each_symbol.append(dict_bits_size)

                if dict_size < self.maximum_table_size:
                    dict_size += 1
                    dictionary[chars_to_add] = dict_size
                found_chars = char
                
            moving_avg_list.append(sum_bit / (i + 1))

        if len(found_chars) > 0:
            n.append(dictionary[found_chars])
            result.append(to_bin(dictionary[found_chars], dict_bits_size))
            str_debug += found_chars
            bits_of_each_symbol.append(dict_bits_size)

        print(dict_size)
        with open("debug_enco.txt", "w") as f:
            f.write(str(dictionary))
        with open("debug_enco_n.txt", "w") as f:
            f.write(str(n))
            

        return result, bits_of_each_symbol, moving_avg_list, dictionary

    def decode(self, encoded_message: List[str]) -> str:
        dict_size: int = 256
        dictionary: dict = {i: chr(i) for i in range(dict_size)}

        chars = chr(to_int(encoded_message.pop(0)))
        result = chars

        current_decode_bytes = ""
        i = len(encoded_message)
        while len(encoded_message) > 0:
            dict_bits_size: int = dict_size.bit_length()
            
            while len(current_decode_bytes) < dict_bits_size and len(encoded_message) > 0:
                i -= 1
                current_decode_bytes += encoded_message.pop(0)

            if (i == 0):
                print("Fim do arquivo")

            code = to_int(current_decode_bytes[:dict_bits_size])
            current_decode_bytes = current_decode_bytes[dict_bits_size:]

            entry: str = dictionary[code] if code in dictionary else chars + chars[0]
            result += entry
            if (i < 10):
                print(i)
                print("=================")
                print("encoded_message ", encoded_message)
                print("dict_bits_size ", dict_bits_size)
                print("current_decode_bytes ", current_decode_bytes)                
                print("len(encoded_message) ", len(encoded_message))
                print("code ", code)
                print("entry", entry)
                print("=================")
                

            if dict_size < (self.maximum_table_size + 1):
                dictionary[dict_size] = chars + entry[0]
                dict_size += 1
            chars = entry

        print(dict_size)
        with open("debug_deco.txt", "w") as f:
            f.write(str(dictionary))

        return result

MAX_LEN_DICT = [4096, 32768, 262144, 2097152]

l = LZW(MAX_LEN_DICT[0], 1)
io = IOHandler("republic")

start_encode = time.time()
m = io.read_file_to_encode()
r, b, moving_avg_list, dict_ = l.encode(m)
import pandas as pd 

# ENTROPIA
P = pd.Series(r).value_counts(normalize=True)
log2_P = P.apply(lambda x: np.log2(1/x))
entropy = np.sum(P * log2_P)
print(entropy)

with open("r.txt", "w") as f:
    f.write(str(r))
io.write_file_to_encode(r)
end_encode = time.time()

delta_time_encode = end_encode - start_encode

print(f"Tempo de execução do encode: {delta_time_encode}")

print("Lendo arquivo codificado")
start_decode = time.time()
r_e = io.read_file_to_decode()

with open("r_e", "w") as f:
    f.write(str(r_e))

print("Decodificando ...")
r_d = l.decode(r_e)
print("Escrevendo arquivo decodificado...")

io.write_file_to_decode(r_d)
end_decode = time.time()
delta_time_decode = end_decode - start_decode
print(f"Tempo de execução do encode: {delta_time_decode}")
print("FIM")

# # plt.plot(moving_avg_list)
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