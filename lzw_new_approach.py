from typing import List

class LZW:
    def encode(self, message: str) -> List[int]: 
        dict_size: int = 256 
        dictionary: dict = {chr(i): i for i in range(dict_size)}

        found_chars: str = ""
        result: List[int] = []
        for char in message:
            chars_to_add: str = found_chars + char
            if chars_to_add in dictionary:
                found_chars = chars_to_add
            else:
                result.append(dictionary[found_chars])
                dictionary[chars_to_add] = dict_size
                dict_size += 1
                found_chars = char
            
        if len(found_chars) > 0:
            result.append(dictionary[found_chars])

        return result
    
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

m =  """1 That which was from the beginning, which we have heard, which we have seen with our eyes, which we have looked at and our hands have touchedthis we proclaim concerning the Word of life. 2 The life appeared; we have seen it and testify to it, and we proclaim to you the eternal life, which was with the Father and has appeared to us. 3 We proclaim to you what we have seen and heard, so that you also may have fellowship with us. And our fellowship is with the Father and with his Son, Jesus Christ. 4 We write this to make our[a] joy complete.
Light and Darkness, Sin and Forgiveness
5 This is the message we have heard from him and declare to you: God is light; in him there is no darkness at all. 6 If we claim to have fellowship with him and yet walk in the darkness, we lie and do not live out the truth. 7 But if we walk in the light, as he is in the light, we have fellowship with one another, and the blood of Jesus, his Son, purifies us from all[b] sin.
8 If we claim to be without sin, we deceive ourselves and the truth is not in us. 9 If we confess our sins, he is faithful and just and will forgive us our sins and purify us from all unrighteousness. 10 If we claim we have not sinned, we make him out to be a liar and his word is not in us."""

r = l.encode(m)
print(r)
r_d = l.decode(r)
print(r_d)
