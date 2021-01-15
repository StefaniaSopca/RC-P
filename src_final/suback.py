import asyncio
from pachet import *
from packettype import SUBACK
from adapters import*
from encode_decode import *



class SubackPayload(Payload):

    RETURN_CODE_00 = 0x00
    RETURN_CODE_01 = 0x01
    RETURN_CODE_02 = 0x02
    RETURN_CODE_80 = 0x80

    def __init__(self, return_codes=[]):
        super().__init__()
        self.return_codes = return_codes

    def __repr__(self):
        return type(self).__name__ + '(return_codes={0})'.format(repr(self.return_codes))

    def to_bytes(self, fixed_header: FixedHeader, variable_header:VariableHeader):
        out = b''
        for return_code in self.return_codes:
            out += int_to_bytes(return_code, 1)
        return out

    def from_stream(cls, reader: ReaderAdapter, fixed_header: FixedHeader,
                    variable_header: VariableHeader):
        return_codes = []
        bytes_to_read = fixed_header.remaining_length - variable_header.bytes_length
        for i in range(0, bytes_to_read):
        
                return_code_byte = yield from read_or_raise(reader, 1)
                return_code = bytes_to_int(return_code_byte)
                return_codes.append(return_code)
           
    
        return cls(return_codes)


class SubackPacket(MQTTPacket):
    VARIABLE_HEADER = PacketIdVariableHeader
    PAYLOAD = SubackPayload

    def __init__(self, fixed: FixedHeader=None, variable_header: PacketIdVariableHeader=None, payload=None):
        if fixed is None:
            header = FixedHeader(SUBACK, 0x00)
        else:
            if fixed.packet_type is not SUBACK:
                raise Exception("Invalid fixed packet type %s for SubackPacket init" )
            header = fixed

        super().__init__(header)
        self.variable_header = variable_header
        self.payload = payload

    def build(cls, packet_id, return_codes):
        variable_header = cls.VARIABLE_HEADER(packet_id)
        payload = cls.PAYLOAD(return_codes)
        return cls(variable_header=variable_header, payload=payload)

