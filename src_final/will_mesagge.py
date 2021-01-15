#constante:
# QoS=1, will_retain=1
# aux = 1
# keepalive = 50


# connect_function =connect(
#     "id_client", keepalive=keepalive, will_topic="topic/on/unexpected/disconnect",
#     will_qos=1, will_retain=True, will_payload="will message".encode('utf-8'))
#
# sock = create_server_socket()
# client =start_client()
# try:
#     (conn, address) = sock.accept()
#     conn.settimeout(10)
#     if expect_packet(conn, "connect", connect_packet):
#         aux = 0
#     conn.close()
# finally:
#     client.terminate()
#     client.wait()
#     sock.close()
# exit(aux)
