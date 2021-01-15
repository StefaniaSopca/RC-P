from pachet import MQTTPacket, FixedHeader, PacketIdVariableHeader
from packettype import PUBREC


class PubrecPacket(MQTTPacket):
    VARIABLE_HEADER = PacketIdVariableHeader
    PAYLOAD = None
#NU ARE PAYLOAD

    def packet_id(self):
        return self.variable_header.packet_id


    def set_packet_id(self, val: int):
        self.variable_header.packet_id = val

    def __init__(self, fixed: FixedHeader=None, variable_header: PacketIdVariableHeader=None):
        if fixed is None:
            header = FixedHeader(PUBREC, 0x00)
        else:
            if fixed.packet_type is not PUBREC:
                raise Exception("Invalid fixed packet type for PubrecPacket init" )
            header = fixed
        super().__init__(header)
        self.variable_header = variable_header
        self.payload = None


    def build(cls, packet_id: int):
        v_header = PacketIdVariableHeader(packet_id)
        packet = PubrecPacket(variable_header=v_header)
        return packet