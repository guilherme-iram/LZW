from typing import Dict, List, Tuple
from io import TextIOWrapper
from struct import pack
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import time
import os

ONE_BYTE = 8
class IOHandler:
    def _init_(self, path, debug_mode=True, sufix="") -> None:
        
        prefix = "data_test" if debug_mode else "data/silesia_corpus"
        
        self.read_path = f"./{prefix}/{path}"
        self.write_path = f"./{prefix}/{path}{sufix}.lzw"
        self.write_decoded_path = f"./{prefix}/{path}{sufix}.lzw.decoded"

    def read_file_to_encode(self) -> str:
        with open(self.read_path, "rb") as f:
            file = f.read()
        return file

    def write_file_to_encode(self, encoded_message):
        output_file: TextIOWrapper = open(self.write_path, "wb")
        
        print("START - WRITE FILE TO ENCODE")
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
            for i, bits in enumerate(decoded_message):
                f.write(pack("B", ord(bits)))
                

def to_bin(integer: int, number_of_bits: int) -> str:
    return format(integer, f"0{number_of_bits}b")


def to_int(bin_formated: str) -> int:
    return int(bin_formated, 2)

class LZW:
    def _init_(self, maximum_table_size: int, dict_strategy: int) -> None:
        self.maximum_table_size = maximum_table_size
        self.dict_strategy = dict_strategy

    def _set_dict_encode(self, dict_size: int) -> dict:
        return {chr(i): i for i in range(dict_size + 1)}
    
    def _set_dict_decode(self, dict_size: int) -> dict:
        return {i: chr(i) for i in range(dict_size)}
    
    def _is_descending(self, moving_avg_list: List[float], threshold: int = 30) -> bool:
        count_descending = 0
        count_stable_or_ascending = 0
        
        for i in range(len(moving_avg_list) - min(threshold, len(moving_avg_list)), len(moving_avg_list) - 1):
            diff = moving_avg_list[i] > moving_avg_list[i + 1]
            if diff:
                count_descending += 1
            else:
                count_stable_or_ascending += 1  
        
        return count_descending > count_stable_or_ascending
    
    def encode(self, message: str) -> Tuple[str, List[int]]:
        dict_size: int = 255
        dictionary: dict = self._set_dict_encode(dict_size)

        found_chars: str = ""
        result = []
        
        moving_avg_list = []
        sum_bit = ONE_BYTE
        for i, char in enumerate(message):
            dict_bits_size: int = dict_size.bit_length()
            char = chr(char)
            chars_to_add: str = found_chars + char
            if chars_to_add in dictionary:
                found_chars = chars_to_add
            else:
                sum_bit += dict_bits_size
                result.append(to_bin(dictionary[found_chars], dict_bits_size))

                if dict_size < self.maximum_table_size:
                    dict_size += 1
                    dictionary[chars_to_add] = dict_size
                else:
                    if self.dict_strategy == 2:    
                        if dict_size == self.maximum_table_size:
                            dict_size: int = 255
                            dictionary: dict = self._set_dict_encode(dict_size)

                            dict_size += 1
                            dictionary[chars_to_add] = dict_size
                            
                    elif self.dict_strategy == 3:
                        if self._is_descending(moving_avg_list):
                            dict_size: int = 255
                            dictionary: dict = self._set_dict_encode(dict_size)
                            
                            dict_size += 1
                            dictionary[chars_to_add] = dict_size
                        
                found_chars = char
                
            moving_avg_list.append(sum_bit / (i + 1))

        if len(found_chars) > 0:
            result.append(to_bin(dictionary[found_chars], dict_bits_size))
        
        # print("Len dictionary encode: ", len(dictionary))
        # print("Total resets: ", total_resets)
        # print("len mensagem: ", len(message))
        return result, moving_avg_list

    def decode(self, encoded_message: List[str], moving_avg_list: list[float]) -> str:
        dict_size: int = 256
        dictionary: dict = self._set_dict_decode(dict_size)
        # print("encoded len: ", len(encoded_message))
        chars = chr(to_int(encoded_message.pop(0)))
        result = chars
        sum_bit = ONE_BYTE
        # moving_avg_list = []
        i = 1
        current_decode_bytes = ""
        while len(encoded_message) > 0:

            if dict_size == (self.maximum_table_size + 1):
                if self.dict_strategy == 2:    
                    dict_size: int = 256
                    dictionary: dict = self._set_dict_decode(dict_size)
                if self.dict_strategy == 3:
                    if self._is_descending(moving_avg_list):
                        dict_size: int = 256
                        dictionary: dict = self._set_dict_decode(dict_size)


            dict_bits_size: int = dict_size.bit_length()
            
            while len(current_decode_bytes) < dict_bits_size and len(encoded_message) > 0:
                current_decode_bytes += encoded_message.pop(0)

            code = to_int(current_decode_bytes[:dict_bits_size])
            current_decode_bytes = current_decode_bytes[dict_bits_size:]

            entry: str = dictionary[code] if code in dictionary else chars + chars[0]
            result += entry
            # sum_bit += dict_bits_size
            
            if dict_size < (self.maximum_table_size + 1):
                dictionary[dict_size] = chars + entry[0]
                dict_size += 1
            
            chars = entry
            # moving_avg_list.append(sum_bit / (i + 1))
            i += 1

        # print("Len dictionary decode: ", len(dictionary))
        # print("Total resets: ", total_resets)

        return result

MAX_LEN_DICT = [4096, 32768, 262144, 2097152]

strategies = {
    # 1: "ED",
    # 2: "RD",
    3: "RD-MD"
}

def get_entropy(r):
    P = pd.Series(r).value_counts(normalize=True)
    log2_P = P.apply(lambda p_i: np.log2(1/p_i))
    return np.sum(P * log2_P)

table_params = {
    "dict_length": [],
    "strategy": [],
    "entropy": [],
    "compress_rate": [],
    "encode_time": [],
    "decode_time": [],
    "moving_avg_list": []
}

def get_compress_rate(encoded_data, original_data):
    return os.stat(encoded_data).st_size / os.stat(original_data).st_size

INPUT_FILE = "republic"

for dict_length in MAX_LEN_DICT[:1]:
    for i, strategy_name in strategies.items():
        io = IOHandler(INPUT_FILE, debug_mode=True, sufix=f"{dict_length}{strategy_name}")
        l = LZW(dict_length, i)

        start_encode = time.time()
        m = io.read_file_to_encode()
        r, moving_avg_list = l.encode(m)
        io.write_file_to_encode(r)
        end_encode = time.time()
        delta_time_encode = end_encode - start_encode
        print("Lendo arquivo codificado")
        start_decode = time.time()
        r_e = io.read_file_to_decode()
        print("Decodificando ...")
        r_d = l.decode(r_e, moving_avg_list)
        print("Escrevendo arquivo decodificado...")
        io.write_file_to_decode(r_d)
        end_decode = time.time()
        delta_time_decode = end_decode - start_decode
        print("FIM\n\n")
        entropy = get_entropy(r)
        
        cr = get_compress_rate(io.write_path, io.read_path)
        
        table_params["dict_length"].append(dict_length)
        table_params["strategy"].append(strategy_name)
        table_params["entropy"].append(entropy)
        table_params["compress_rate"].append(cr)
        table_params["encode_time"].append(delta_time_encode)
        table_params["decode_time"].append(delta_time_decode)
        table_params["moving_avg_list"].append(moving_avg_list)
                
        table = pd.DataFrame(table_params)
        table.to_csv(f"table_{dict_length}{strategy_name}.csv", index=False)