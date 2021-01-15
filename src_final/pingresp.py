from pachet import*
from packettype import PINGRESP



class PingrespPacket(MQTTPacket):
    VARIABLE_HEADER = None
    PAYLOAD = None

    def __init__(self, fixed: FixedHeader=None):
        if fixed is None:
            header = FixedHeader(PINGRESP, 0x00)
        else:
            if fixed.packet_type is not PINGRESP:
                raise Exception("Invalid fixed packet type %s for PingRespPacket init")
            header = fixed
        super().__init__(header)
        self.variable_header = None
        self.payload = None


    def build(cls):
        return cls()

