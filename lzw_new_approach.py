from typing import Dict, List, Tuple
from io import TextIOWrapper
from struct import pack

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

    def write_file_to_encode(self, encoded_message: List[str]) -> None:
        output_file: TextIOWrapper = open(self.write_path, "wb")
        i = 0
        while len(encoded_message) > ONE_BYTE:
            bits_to_write = encoded_message[:ONE_BYTE]
            to_write = int(bits_to_write, 2)
            output_file.write(pack("B", to_write))
            encoded_message = encoded_message[ONE_BYTE:]
            print(i)

            i += 1

        if len(encoded_message) > 0:
            bits_to_write = encoded_message
            diff = ONE_BYTE - len(bits_to_write)
            bits_to_write = bits_to_write + ("0" * diff)
            to_write = int(bits_to_write, 2)
            output_file.write(pack("B", to_write))

        output_file.close()

    def read_file_to_decode(self) -> str:
        with open(self.write_path, "rb") as f:
            file = f.read()
        return [format(symbol, f"0{ONE_BYTE}b") for symbol in file]
    
    def write_file_to_decode(self, decoded_message: str) -> None:
        with open(self.write_decoded_path, "wb") as f:
            last_char = len(decoded_message) - 1
            for i, bits in enumerate(decoded_message):
                # corner case last char 
                if i != last_char:
                    f.write(pack("B", ord(bits)))
        


def to_bin(integer: int, number_of_bits: int) -> str:
    return format(integer, f"0{number_of_bits}b")

def to_int(bin_formated: str) -> int:
    return int(bin_formated, 2)


class LZW:
    def encode(self, message: str) -> Tuple[str, List[int]]:
        dict_size: int = 255
        dictionary: dict = {chr(i): i for i in range(dict_size + 1)}

        found_chars: str = ""
        result: str = ""
        bits_of_each_symbol: List[int] = []
        for char in message:
            dict_bits_size: int = dict_size.bit_length()
            char = chr(char)
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

            dictionary[dict_size] = chars + entry[0]
            dict_size += 1
            chars = entry

            encoded_message_in_bits = encoded_message_in_bits[dict_bits_size:]

        return result


l = LZW()
io = IOHandler("xml")
m = io.read_file_to_encode()
r, b = l.encode(m)
io.write_file_to_encode(r)
r_e = io.read_file_to_decode()
r_d = l.decode(r_e)
io.write_file_to_decode(r_d)

# original = ""
# has_error = False
# for i, j in zip(m, r_d):
#     original += chr(i)
#     if chr(i) != j:
#         print(chr(i), j, chr(i) == j)
#         has_error = True

# if not has_error:
#     print("DEU CERTO!")
