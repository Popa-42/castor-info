import socket
import _thread
from terminal_colors import *
import argparse

parser = argparse.ArgumentParser(description="Castor Server")

parser.add_argument("-c", "--color", help="Uses colored terminal outputs. Terminal must support colors.", action="store_true")

args = parser.parse_args()

colored_terminal: bool = args.color

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
    while len(clients) < max_clients:
        # Versuche eine Verbindung herzustellen
        recv_data, addr = discovery_sock.recvfrom(2048)
        client_ip = addr[0]

        if colored_terminal: print(f"{GREEN}Received UDP packet from {CYAN}{client_ip}:{addr[1]}{RESET}")
        else: print(f"Received UDP packet from {client_ip}:{addr[1]}")

        address = (client_ip, 10001)
        return_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        return_socket.sendto("Castor Server".encode(), address)
        return_socket.close()

        if colored_terminal: print(f"{GREEN}Sent UDP return packet to {CYAN}{client_ip}{RESET}")
        else: print(f"Sent UDP return packet to {client_ip}")

        (conn, addr) = sock.accept()
        clients.append((conn, addr))
        _thread.start_new_thread(threaded_client, (conn, addr))

        if colored_terminal: print(f"{GREEN_BACKGROUND}{BLACK}TCP Connected to {DARK_YELLOW_BACKGROUND}{client_ip}{RESET}\n\n"
              f"{BLUE}Number of connected Clients: {BOLD}{YELLOW}{len(clients)}{RESET_WEIGHT}{DARK_YELLOW}/{max_clients}{RESET}\n")
        else: print(f"TCP Connected to {client_ip}\n\n"
              f"Number of connected Clients: {len(clients)}/{max_clients}\n")


def new_server():
    global sock, discovery_sock
    # TCP Connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_port = 9999
    server_name = ''
    server_address = (server_name, server_port)
    sock.bind(server_address)
    sock.listen()

    if colored_terminal: print(f"{GREEN}Started Castor server on port {BOLD}{DARK_YELLOW}{server_port}{RESET}\n")
    else: print(f"Started Castor server on port {server_port}\n")

    # SERVER DISCOVERY
    discovery_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    discovery_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    discovery_sock.bind(("", 10000))


def start_server(max_clients, tick_function):
    # Create a new server
    new_server()
    # Search for connecting clients
    search_connections(max_clients)

    if colored_terminal: print(f"{GREEN_BACKGROUND}{BLACK} Starting the game... {RESET}\n")
    else: print(f"Starting the game...\n")
    # MAIN LOOP: The game function
    while True:
        try:
            tick_function()
        except KeyboardInterrupt:
            if colored_terminal: print(f"\n{RED_BACKGROUND}{BLACK} Server stopped due to keyboard interrupt. {RESET}")
            else: print(f"\nServer stopped due to keyboard interrupt.")
            break


if __name__ == '__main__':
    start_server(4, lambda: ...)
