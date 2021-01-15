#daca am fi avut o clasa broker care ar avea asignata o lista de clienti
#am cauta clienti si am verifica daca timpul permis de inactivitatea a fost depasit,in caz adevarat i-am deconecta
# def keepalive(self, sock):
#     if sock in self.clients.keys():
#       client = self.clients[sock]
#       if client.keepalive > 0 and time.time() - client.lastPacket > client.keepalive * 1.5:
#         # keep alive timeout
#         logger.info("keepalive timeout for client %s", client.id)
#         self.disconnect(sock, None, terminate=True)

