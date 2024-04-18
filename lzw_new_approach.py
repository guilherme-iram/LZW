from typing import Dict, List, Tuple
from io import TextIOWrapper
from struct import pack

ONE_BYTE = 8

class IOHandler:
    def __init__(self, path) -> None:
        self.read_path = f"./data_test/{path}"
        self.write_path = f"./data_test/{path}.lzw"

    def read_file_to_encode(self) -> str:
        with open(self.read_path, "r") as f:
            file = f.read()
        return file
    
    def write_file_to_encode(self, message: List[str]) -> None:
        output_file: TextIOWrapper = open(self.write_path, "wb")        
        while len(message) > 8:
            bits_to_write = message[:ONE_BYTE]
            to_write = int(bits_to_write, 2)
            print(bits_to_write, to_write)
            output_file.write(pack('B', to_write))
            message = message[ONE_BYTE:]

        if len(message) > 0:
            bits_to_write = message
            to_write = int(bits_to_write, 2)
            output_file.write(pack('B', to_write))
        
        output_file.close()

def to_bin(integer: int, number_of_bits):
    return format(integer, f'0{number_of_bits}b')

class LZW:
    def encode(self, message: str) -> Tuple[str, List[int]]: 
        dict_size: int = 255
        dictionary: dict = {chr(i): i for i in range(dict_size + 1)}

        found_chars: str = ""
        result: str = ""
        bits_of_each_symbol: List[int] = []
        for char in message:
            dict_bits_size: int = dict_size.bit_length()
            chars_to_add: str = found_chars + char
            if chars_to_add in dictionary:
                found_chars = chars_to_add
            else:
                result += to_bin(dictionary[found_chars], dict_bits_size)
                bits_of_each_symbol.append(dict_bits_size)
                dict_size += 1
                dictionary[chars_to_add] = dict_size
                found_chars = char
            
        if len(found_chars) > 0:
            result += to_bin(dictionary[found_chars], dict_bits_size)
            bits_of_each_symbol.append(dict_bits_size)
            
        return result, bits_of_each_symbol
    
    def decode(self, encoded_message: List[int]) -> str:
        dict_size: int = 256 
        dictionary: dict = {i: chr(i) for i in range(dict_size)}

        chars = chr(encoded_message[0])
        result = chars
        encoded_message.pop(0)

        for code in encoded_message:
            entry: str = dictionary[code] if code in dictionary else chars + chars[0]
            result += entry

            dictionary[dict_size] = chars + entry[0]
            dict_size += 1
            chars = entry 

        return result


l = LZW()
io = IOHandler("john_1")
m = io.read_file_to_encode()
r, b = l.encode(m)
io.write_file_to_encode(r)
# r_d = l.decode(r)
# print(r_d)
# print(m == r_d)
