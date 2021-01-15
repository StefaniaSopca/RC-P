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
from pachet import *
from encode_decode import *
from remainingdecode import *


def bytes_to_string(bit: bytes) -> str:
    s = ''
    for i in bit:
        a = int(i)
        out = ""
        for index in range(7, -1, -1):
            if (a & (1 << index)) > 0:
                out += '1'
            else:
                out += '0'
        s += str(out) + ' (' + str(a) + ', ' + chr(a) + ')' + '\n'
    return s


class SenderReceiver:
    def __init__(self, conn):
        self.conn = conn

    def sendpacket(self, packet: MQTTPacket):
        # sent_bytes=self.conn.send(mesaj.encode('utf-8'))
        # sent_bytes=self.conn.send(str(packet.fixedheader))
        header = packet.fixed_header
        variable = packet.variable_header
        payload = packet.payload

        out = header.to_bytes()
        if variable is not None:
            out.extend(variable.to_bytes())
        if payload is not None:
            out.extend(payload.to_bytes(header, variable))

        # print('header:' + str(header.packet_type))
        # print('packet:' + str(packet.fixed_header.packet_type))
        # sent_bytes=self.conn.send(int_to_bytes_str(header.packet_type))
        # print(bytes_to_string(packet.to_bytes()))
        # print('conversie:' + str(int_to_bytes_str(packet.fixed_header.packet_type)))
        print(str(bytes_to_string(out)))
        sent_bytes = self.conn.send(out)
        # sent_bytes = 0

        # int_to_bytes_str

        # print('s-a trimis ' + str(sent_bytes))
        # text = self.encoder.encode(package)
        # sent_bytes = self.conn.send(str(text))
        return sent_bytes

    def receivepacket(self):
        # text=self.conn.recv(64)
        # return text.decode('utf-8')
        header_content = bytearray()
        flags = self.conn.recv(1)
        header_content.extend(flags)
        # # read remaining length
        completeRem = bytearray()
        remLength = self.conn.recv(1)
        header_content.extend(remLength)
        completeRem.extend(remLength)
        while (remLength[0] & (1 << 7)) > 0:
            remLength = self.conn.recv(1)
            header_content.extend(remLength)
            completeRem.extend(remLength)

        completeRem = RemainingLength.decode(completeRem)
        # receive variable part + payload
        remLength = self.conn.recv(completeRem)
        header_content.extend(remLength)

        return header_content


if __name__ == "__main__":
    biti = bytes([23, 15])
    print(str(biti))
    print(bytes_to_string(biti))
