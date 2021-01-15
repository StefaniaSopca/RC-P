from pachet import MQTTPacket, FixedHeader, PacketIdVariableHeader
from packettype import PUBREL
class PubrelPacket(MQTTPacket):
    VARIABLE_HEADER = PacketIdVariableHeader
    PAYLOAD = None
#NU ARE PAYLOAD
    
    def packet_id(self):
        return self.variable_header.packet_id

    def set_packet_id(self, val: int):
        self.variable_header.packet_id = val

    def __init__(self, fixed: FixedHeader=None, variable_header: PacketIdVariableHeader=None):
        if fixed is None:
            header = FixedHeader(PUBREL, 0x02)  #pachetul de control si flagurile acestuia (0010)
        else:
            if fixed.packet_type is not PUBREL:
                raise Exception("Invalid fixed packet type for PubrelPacket init" )
            header = fixed
        super().__init__(header)
        self.variable_header = variable_header
        self.payload = None

    def build(cls, packet_id):
        variable_header = PacketIdVariableHeader(packet_id)
        return PubrelPacket(variable_header=variable_header)