
from pachet import *
from encode_decode import *
from packettype import UNSUBSCRIBE

class UnsubscribePayload(Payload):


    def __init__(self, topics=[]):
        super().__init__()
        self.topics = topics

    def to_bytes(self, fixed_header: FixedHeader, variable_header: VariableHeader):
        out = b''
        for topic in self.topics:
            out += encode_string(topic)
        return out

    def from_stream(cls, reader: asyncio.StreamReader, fixed_header: FixedHeader,
                    variable_header: VariableHeader):
        topics = []
        payload_length = fixed_header.remaining_length - variable_header.bytes_length
        read_bytes = 0
        while read_bytes < payload_length:
           
                topic = yield from decode_string(reader)
                topics.append(topic)
                read_bytes += 2 + len(topic.encode('utf-8'))
           
        return cls(topics)


class UnsubscribePacket(MQTTPacket):
    VARIABLE_HEADER = VariableHeader
    PAYLOAD = UnsubscribePayload

    def __init__(self, fixed: FixedHeader=None, variable_header: VariableHeader=None, payload=None):
        if fixed is None:
            header = FixedHeader(UNSUBSCRIBE, 0x02) 
        else:
            if fixed.packet_type is not UNSUBSCRIBE:
                raise Exception("Invalid fixed packet type %s for UnsubscribePacket init")
            header = fixed

        super().__init__(header)
        self.variable_header = variable_header
        self.payload = payload

    def build(cls, topics, packet_id):
        v_header = VariableHeader(packet_id)
        payload = UnsubscribePayload(topics)
        return UnsubscribePacket(variable_header=v_header, payload=payload)

