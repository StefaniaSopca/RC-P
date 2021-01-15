import struct


# algorithm luat de la pagina 19 din mqtt version 3.1.1
class RemainingLength:
    @staticmethod
    def encode(X: int) -> bytes:
        rez = bytearray()
        while X > 0:
            encodedByte = X % 128
            X = X // 128
            if X > 0:
                encodedByte = encodedByte or 128
            rez += struct.pack("!B", encodedByte)
        return rez

    @staticmethod
    def decode(info: bytes) -> int:
        multiplier = 1
        value = 0
        index = 0
        while True:
            encodedByte = info[index]
            value = value + (encodedByte & 127) * multiplier
            if multiplier > 128 * 128 * 128:
                raise ValueError("Malformed Remaining Lenght")
            multiplier = multiplier * 128
            index += 1
            if index > len(info):  # sa nu depaseasca lungimea sirului
                break
            if (encodedByte & 128 == 0):
                break
        return value
