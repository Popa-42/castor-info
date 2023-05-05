import socket
import _thread


clients = []
sock: socket.socket = ...
discovery_sock: socket.socket = ...


def send_to_client(conn, data: str):
    conn.send(data.encode())


def send_to_all_clients(data: str):
    global clients
    for cl in clients:
        cl[0].send(data.encode)


def threaded_client(conn, addr):
    while True:
        # data = conn.recv(2048)
        pass


def search_connections(max_clients: int = 4):
    global sock, discovery_sock, clients
    # Ende, wenn mehr als max Clients
    while len(clients) <= max_clients:
        # Versuche eine Verbindung herzustellen
        recv_data, addr = discovery_sock.recvfrom(2048)
        client_ip = addr[0]
        print(f"UDP packet from {client_ip}")

        address = (client_ip, 10001)
        return_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        return_socket.sendto("Castor Server".encode(), address)
        return_socket.close()
        print(f"Sent UDP return packet to {client_ip}")

        (conn, addr) = sock.accept()
        print(f"TCP Connected to {client_ip}")
        clients.append((conn, addr))
        _thread.start_new_thread(threaded_client, (conn, addr))


def new_server():
    global sock, discovery_sock
    # TCP Connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_port = 9999
    server_name = ''
    server_address = (server_name, server_port)
    sock.bind((server_name, server_port))
    sock.listen()
    print(f"Started Castor server on port {server_port}.")

    # SERVER DISCOVERY
    discovery_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    discovery_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    discovery_sock.bind(("", 10000))


def start_server(max_clients, tick_function):
    new_server()

    search_connections(max_clients)

    tick_function()


if __name__ == '__main__':
    start_server(4, lambda: ...)
