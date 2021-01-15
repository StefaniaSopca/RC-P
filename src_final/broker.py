import socket
import threading

from SenderReceiver import *
import main


class Broker:
    def __init__(self, address):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.bind(address)

        self.active_clients = []

    def listen(self):
        self.conn.listen()

        while True:
            conn, addr = self.conn.accept()
            conn.settimeout(10)
            thread = threading.Thread(target=self.run_client, args=[conn])
            self.active_clients.append(thread)
            thread.start()

    def run_client(self, conn):
        senderReceiver = SenderReceiver(conn)

        # receve from client
        while True:
            try:
                packet = senderReceiver.receivepacket()
                if packet is not None:
                    type = (packet[0] >> 4)
                    print("\nWe received[" + str(main.packet_dictionary[type].__name__) + "]:")
                    print(bytes_to_string(packet))
            except:
                pass




if __name__ == "__main__":
    ip = socket.gethostbyname(socket.gethostname())
    port = 1883
    address = (ip, port)
    broker = Broker(address)

    broker.listen()
