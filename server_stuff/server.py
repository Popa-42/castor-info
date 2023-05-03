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


def search_connections(timeout: float, max_clients: int = 4):
    global sock, discovery_sock, clients
    # Ende, wenn mehr als max Clients
    if len(clients) >= max_clients:
        return
    # Timeout
    discovery_sock.settimeout(timeout)
    # Versuche eine Verbindung herzustellen
    try:
        recv_data, addr = discovery_sock.recvfrom(2048)
        client_ip = addr[0]
        print(f"Connection attempt from {client_ip}")

        snd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        snd.connect((addr[0], 10000))
        snd.close()

        print(f"TCP Connected to {client_ip}")
        (conn, addr) = sock.accept()
        clients.append((conn, addr))
        _thread.start_new_thread(threaded_client, (conn, addr))
    # Suche dauerte länger als timeout, fahre mit dem Rest des Codes fort
    except socket.timeout:
        return


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
    address = ('', 10001)
    discovery_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    discovery_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    discovery_sock.bind(address)


def start_server(timeout, max_clients, tick_function):
    new_server()

    # MAIN LOOP
    while True:
        # Suche nach Verbindungen und füge ggf den neuen Client hinzu
        search_connections(timeout, max_clients)
        tick_function()


if __name__ == '__main__':
    start_server(0.1, 4, lambda: ...)
