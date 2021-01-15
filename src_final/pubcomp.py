from pachet import MQTTPacket, FixedHeader,PacketIdVariableHeader
from packettype import PUBCOMP

class PubcompPacket(MQTTPacket):
    VARIABLE_HEADER = PacketIdVariableHeader
    PAYLOAD = None
    #NU ARE PAYLOAD

    def packet_id(self):
        return self.variable_header.packet_id


    def set_packet_id(self, val: int):
        self.variable_header.packet_id = val

    def __init__(self, fixed: FixedHeader=None, variable_header: PacketIdVariableHeader=None):
        if fixed is None:
            header =FixedHeader(PUBCOMP, 0x00)
        else:
            if fixed.packet_type is not PUBCOMP:
                raise Exception("Invalid fixed packet type for PubcompPacket init" )
            header = fixed
        super().__init__(header)
        self.variable_header = variable_header
        self.payload = None

    def build(cls, packet_id: int):
        v_header = PacketIdVariableHeader(packet_id)
        packet = PubcompPacket(variable_header=v_header)
        return packet