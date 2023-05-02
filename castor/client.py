import socket
import _thread

address = ('<broadcast>', 10001)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

data = "Castor Client"
client_socket.sendto(data.encode(), address)
client_socket.close()


def recieve_thread(conn):
    print("Connected to remote server.")
    while True:
        pass


rec = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
rec.bind(("", 10000))
rec.listen()
(cn, addr) = rec.accept()
rec.close()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((addr[0], 9999))
print("Connected to server")
#_thread.start_new_thread(recieve_thread, (conn,))

while True:
    pass
