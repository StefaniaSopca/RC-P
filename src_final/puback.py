from pachet import MQTTPacket, FixedHeader,PacketIdVariableHeader
from packettype import PUBACK
class PubackPacket(MQTTPacket):
    VARIABLE_HEADER = PacketIdVariableHeader
    PAYLOAD = None

  #NU ARE PAYLOAD SI NICI VARIABLE HEADER

    def __init__(self, fixed: FixedHeader=None, variable_header: PacketIdVariableHeader=None):
        if fixed is None:
            header = FixedHeader(PUBACK, 0x00)
        else:
            if fixed.packet_type is not PUBACK:
                raise Exception("Invalid fixed packet type for PubackPacket init" )
            header = fixed
        super().__init__(header)
        self.variable_header = variable_header
        self.payload = None

   
    def build(cls, packet_id: int):
        v_header = PacketIdVariableHeader(packet_id)
        packet = PubackPacket(variable_header=v_header)
        return packet