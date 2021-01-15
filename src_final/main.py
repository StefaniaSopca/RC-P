from packettype import (
    CONNECT, CONNACK, PUBLISH, PUBACK, PUBREC, PUBREL, PUBCOMP, SUBSCRIBE,
    SUBACK, UNSUBSCRIBE, UNSUBACK, PINGREQ, PINGRESP, DISCONNECT)
from pachet import FixedHeader
from connack import ConnackPacket
from connect import ConnectPacket
from disconnect import DisconnectPacket
from pingreq import PingreqPacket
from pingresp import PingrespPacket
from puback import PubackPacket
from pubcomp import PubcompPacket
from publish import PublishPacket
from pubrec import PubrecPacket
from pubrel import PubrelPacket
from suback import SubackPacket
from subscribe import SubscribePacket
from unsuback import UnsubackPacket
from unsubscribe import UnsubscribePacket

#in total sunt 14 elemente in dictionar ce trebuiesc implementate
packet_dictionary = {
    CONNECT:ConnectPacket, #1
    CONNACK:ConnackPacket,  #2
    PUBLISH:PublishPacket,  #3
    PUBACK: PubackPacket,   #4
    PUBREC:PubrecPacket,    #5
    PUBCOMP:PubcompPacket,  #6
    PUBREL: PubrelPacket,   #7
    SUBSCRIBE:SubscribePacket,  #8
    SUBACK:SubackPacket,     #9
    UNSUBSCRIBE:UnsubscribePacket,  #10
    UNSUBACK: UnsubackPacket,     #11
    PINGREQ:PingreqPacket,      #12
    PINGRESP:PingrespPacket,    #13
    DISCONNECT: DisconnectPacket  #14
}


def packet_class(fixed_header: FixedHeader):
    try:
        cls = packet_dictionary[fixed_header.packet_type]
        return cls
    except KeyError:
        raise Exception("Unexpected packet Type '%s'" % fixed_header.packet_type)
def show(fixed_header: FixedHeader):
  print("packet_type: "+ str(fixed_header.packet_type))
  print("flags: "+str(fixed_header.flags))
  print("remaining_length: "+str(fixed_header.remaining_length))

  

if __name__ == '__main__':
  header = FixedHeader(PUBREL, 0x02)  
  print(packet_class(header))
  show(header)
