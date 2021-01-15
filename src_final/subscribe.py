import asyncio
from pachet import *
from encode_decode import *
from packettype import SUBSCRIBE


class SubscribePayload(Payload):


    def __init__(self, topics=[]):
        super().__init__()
        self.topics = topics

    def to_bytes(self, fixed_header: FixedHeader, variable_header: VariableHeader):
        out = b''
        for topic in self.topics:
            out += encode_string(topic[0])
            out += int_to_bytes(topic[1], 1)
        return out

    def from_stream(cls, reader: asyncio.StreamReader, fixed_header: FixedHeader,
                    variable_header: VariableHeader):
        topics = []
        payload_length = fixed_header.remaining_length - variable_header.bytes_length
        read_bytes = 0
        while read_bytes < payload_length:
            
                topic = yield from decode_string(reader)
                qos_byte = yield from read_or_raise(reader, 1)
                qos = bytes_to_int(qos_byte)
                topics.append((topic, qos))
                read_bytes += 2 + len(topic.encode('utf-8')) + 1
          
        return cls(topics)

    def __repr__(self):
        return type(self).__name__ + '(topics={0!r})'.format(self.topics)


class SubscribePacket(MQTTPacket):
    VARIABLE_HEADER = PacketIdVariableHeader
    PAYLOAD = SubscribePayload

    def __init__(self, fixed: FixedHeader=None, variable_header: PacketIdVariableHeader=None, payload=None):
        if fixed is None:
            header = FixedHeader(SUBSCRIBE, 0x02)
        else:
            if fixed.packet_type is not SUBSCRIBE:
                raise Exception("Invalid fixed packet type %s for SubscribePacket init")
            header = fixed

        super().__init__(header)
        self.variable_header = variable_header
        self.payload = payload

    def build(cls, topics, packet_id):
        v_header = PacketIdVariableHeader(packet_id)
        payload = SubscribePayload(topics)
        return SubscribePacket(variable_header=v_header, payload=payload)

