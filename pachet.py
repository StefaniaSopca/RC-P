from struct import *


class FixedHeader:
    def __init__(self, packet_type, flags=0, remaining_length=0):
        self.packet_type = packet_type
        self.remaining_length = remaining_length
        self.flags = flags

    def to_bytes(self):
        def encode_remaining_length(X: int) -> bytes:
            rez = bytearray()
            while X > 0:
                encodedByte = X % 128
                X = X // 128
                if X > 0:
                    encodedByte = encodedByte or 128
                rez += struct.pack("!B", encodedByte)
            return rez

        out = bytearray()
        packet_type = 0
        try:
            packet_type = (self.packet_type << 4) | self.flags
            out.append(packet_type)
        except OverflowError:
            raise Exception(
                'packet_type encoding exceed 1 byte length: value=%d',
                packet_type)

        encoded_length = encode_remaining_length(self.remaining_length)
        out.extend(encoded_length)

        return out

    def bytes_length(self):
        return len(self.to_bytes())

    def decode_remaining_length(info: bytes) -> int:
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
            if index > len(info):  #sa nu depaseasca lungimea sirului
                break
            if (encodedByte & 128 == 0):
                break

    def __repr__(self):
        return type(self).__name__ + '(length={0}, flags={1})'.\
            format(self.remaining_length, hex(self.flags))


class VariableHeader:
    def __init__(self):
        pass

    def to_bytes(self) -> bytes:
        """
        Serialize header data to a byte array conforming to MQTT protocol
        :return: serialized data
        """

    @property
    def bytes_length(self):
        return len(self.to_bytes())


class PacketIdVariableHeader(VariableHeader):

    __slots__ = ('packet_id', )

    def __init__(self, packet_id):
        super().__init__()
        self.packet_id = packet_id

    def int_to_bytes(x: int) -> bytes:
        return x.to_bytes((x.bit_length() + 7) // 8, 'big')

    def to_bytes(self):
        out = b''
        ## out += int_to_bytes(self.packet_id, 2)
        out += self.packet_id.to_bytes(2, byteorder='big')
        return out

    def __repr__(self):
        return type(self).__name__ + '(packet_id={0})'.format(self.packet_id)


class Payload:
    def __init__(self):
        pass

    def to_bytes(self, fixed_header: FixedHeader,
                 variable_header: VariableHeader):
        pass


class MQTTPacket:

    FIXED_HEADER = FixedHeader
    VARIABLE_HEADER = None
    PAYLOAD = None

    def __init__(self,
                 fixed: FixedHeader,
                 variable_header: VariableHeader = None,
                 payload: Payload = None):
        self.fixed_header = fixed
        self.variable_header = variable_header
        self.payload = payload
        self.protocol_ts = None

    def to_bytes(self) -> bytes:
        if self.variable_header:
            variable_header_bytes = self.variable_header.to_bytes()
        else:
            variable_header_bytes = b''
        if self.payload:
            payload_bytes = self.payload.to_bytes(self.fixed_header,
                                                  self.variable_header)
        else:
            payload_bytes = b''

        self.fixed_header.remaining_length = len(variable_header_bytes) + len(
            payload_bytes)
        fixed_header_bytes = self.fixed_header.to_bytes()

        return fixed_header_bytes + variable_header_bytes + payload_bytes

    def bytes_length(self):
        return len(self.to_bytes())

    def __repr__(self):
        return type(self).__name__ + '(ts={0!s}, fixed={1!r}, variable={2!r}, payload={3!r})'.\
            format(self.protocol_ts, self.fixed_header, self.variable_header, self.payload)

    def packet_id(self):
        pass

    def set_packet_id(self, val: int):
        pass

    def build(cls, packet_id: int):
        pass
