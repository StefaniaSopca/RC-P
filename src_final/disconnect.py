from pachet import MQTTPacket, FixedHeader
from packettype import DISCONNECT


class DisconnectPacket(MQTTPacket):
    VARIABLE_HEADER = None
    PAYLOAD = None
 #NU ARE PAYLOAD SI NICI VARIABLE HEADER

    def __init__(self, fixed: FixedHeader=None):
        if fixed is None:
            header = FixedHeader(DISCONNECT, 0x00)
        else:
            if fixed.packet_type is not DISCONNECT:
                raise Exception("Invalid fixed packet type  for DisconnectPacket init")
            header = fixed
        super().__init__(header)
        self.variable_header = None
        self.payload = None