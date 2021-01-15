from pachet import MQTTPacket, FixedHeader, PacketIdVariableHeader
from packettype import UNSUBACK
class UnsubackPacket(MQTTPacket):
    VARIABLE_HEADER = PacketIdVariableHeader
    PAYLOAD = None
    #NU ARE PAYLOAD

    def packet_id(self):
        return self.variable_header.packet_id

    def set_packet_id(self, val: int):
        self.variable_header.packet_id = val

    def __init__(self, fixed: FixedHeader=None, variable_header: PacketIdVariableHeader=None, payload=None):
        if fixed is None:
            header = FixedHeader(UNSUBACK, 0x00)
        else:
            if fixed.packet_type is not UNSUBACK:
                raise Exception("Invalid fixed packet type for UnsubackPacket init")
            header = fixed

        super().__init__(header)
        self.variable_header = variable_header
        self.payload = payload


    def build(cls, packet_id):
        variable_header = PacketIdVariableHeader(packet_id)
        return cls(variable_header=variable_header)