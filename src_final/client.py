import socket
import threading

from SenderReceiver import *
from connack import ConnackVariable
from connect import ConnectVariable, ConnectPayload
from suback import SubackPayload
import time



class Client:
    def __init__(self, address):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect(address)
        self.SR = SenderReceiver(self.conn)

    # def connect(self):
    #     connectr=ConnectPacket(ConnectVariable(),ConnectPayload())
    #     self.SR.sendpacket(connectr)

    def send(self):
        pubrec_packet = PubrecPacket(fixed=FixedHeader(PUBREC, 0, 2), variable_header=PacketIdVariableHeader(34))
        print("Sending Pubrec ...")
        self.SR.sendpacket(pubrec_packet)
        time.sleep(3)

        pubrel_packet = PubrelPacket(fixed=FixedHeader(PUBREL, 0, 2), variable_header=PacketIdVariableHeader(300))
        print("Sending Pubrel ...")
        self.SR.sendpacket(pubrel_packet)
        time.sleep(3)

        suback_packet = SubackPacket(fixed=FixedHeader(SUBACK, 0, 6), variable_header=PacketIdVariableHeader(4),
                                     payload=SubackPayload([0, 2, 1, 2]))
        print("Sending Suback ...")
        self.SR.sendpacket(suback_packet)
        time.sleep(3)

        disconnect_packet = DisconnectPacket(FixedHeader(DISCONNECT, 0, 0))
        print("Sending Disconnect ...")
        self.SR.sendpacket(disconnect_packet)
        time.sleep(3)

        connack_packet = ConnackPacket(fixed=FixedHeader(CONNACK, 0, 2), variable=ConnackVariable(1, 5))
        print("Sending Connack ...")
        self.SR.sendpacket(connack_packet)
        time.sleep(3)

        unsuback_packet = UnsubackPacket(fixed=FixedHeader(UNSUBACK, 0, 2), variable_header=PacketIdVariableHeader(10))
        print("Sending Unsuback ...")
        self.SR.sendpacket(unsuback_packet)
        time.sleep(3)

        pubcomp_packet = PubcompPacket(fixed=FixedHeader(PUBCOMP, 0, 2), variable_header=PacketIdVariableHeader(22))
        print("Sending Pubcomp ...")
        self.SR.sendpacket(pubcomp_packet)
        time.sleep(3)

        pingreq_packet = PingreqPacket(FixedHeader(PINGREQ, 0, 0))
        print("Sending Pingreq ...")
        self.SR.sendpacket(pingreq_packet)
        time.sleep(3)

        pingresp_packet = PingrespPacket(FixedHeader(PINGRESP, 0, 0))
        print("Sending Pingresp ...")
        self.SR.sendpacket(pingresp_packet)
        time.sleep(3)




if __name__ == "__main__":
    ip = socket.gethostbyname(socket.gethostname())
    port = 1883
    address = (ip, port)
    client = Client(address)
    client.send()
