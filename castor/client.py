import socket
import _thread

server_ip = ""

address = ('<broadcast>', 10001)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

data = "Castor Client"
client_socket.sendto(data.encode(), address)
client_socket.close()


def get_server_ip():
    return server_ip


def recieve_thread(conn):
    while True:
        data = conn.recv(2048)
        print(data.decode())


def send_to_server(data):
    client.send(data.encode())


rec = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
rec.bind(("", 10000))
rec.listen()
(cn, addr) = rec.accept()
rec.close()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((addr[0], 9999))
print("Connected to server")
server_ip = addr[0]

_thread.start_new_thread(recieve_thread, (client,))

while True:
    pass
