import socket
import _thread

# TCP Connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_name = ""
server_port = 9999
server_address = (server_name, server_port)
sock.bind((server_name, server_port))
print(f"Started Castor server on port {server_port}")

clients = []


def send_to_client(conn, data):
    conn.send(data.encode())


def send_to_all_clients(data):
    for cl in clients:
        cl[0].send(data.encode)


def threaded_client(conn, addr):
    while True:
        #data = conn.recv(2048)
        pass


# SERVER DISCOVERY
address = ('', 10001)
discovery_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
discovery_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
discovery_sock.bind(address)

while True:
    recv_data, addr = discovery_sock.recvfrom(2048)
    client_ip = addr[0]
    print(f"Connection attempt from {client_ip}")

    conn = sock.connect((client_ip, 10000))
    print(f"TCP Connected to {client_ip}")
    _thread.start_new_thread(threaded_client, (conn, addr))