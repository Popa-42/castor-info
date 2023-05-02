import socket
import _thread

address = ('<broadcast>', 10001)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

data = "Castor Client"
client_socket.sendto(data.encode(), address)
client_socket.close()

rec_addr = ("", 10002)
recieve_ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recieve_ip.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
recieve_ip.bind(rec_addr)

while True:
    recv_data, addr = recieve_ip.recvfrom(2048)
    server_ip = addr[0]
    print("Server found: ", server_ip)
    recieve_ip.close()
    break


def recieve_thread(conn):
    while True:
        data = conn.recv(2048)
        print(data.decode())


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, 9999))
_thread.start_new_thread(recieve_thread, (client,))

while True:
    pass
