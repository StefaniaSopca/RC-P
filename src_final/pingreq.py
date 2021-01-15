from pachet import MQTTPacket, FixedHeader,PacketIdVariableHeader
from packettype import PINGREQ

class PingreqPacket(MQTTPacket):
    VARIABLE_HEADER = None
    PAYLOAD = None

    def __init__(self, fixed: FixedHeader=None):
        if fixed is None:
            header = FixedHeader(PINGREQ, 0x00)
        else:
            if fixed.packet_type is not PINGREQ:
                raise Exception("Invalid fixed packet type for PingReqPacket init")
            header = fixed
        super().__init__(header)
        self.variable_header = None
        self.payload = None