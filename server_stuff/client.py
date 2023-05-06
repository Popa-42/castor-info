import socket
import _thread
from terminal_colors import *

server_ip = ""
client = ...
active = True


def get_server_ip():
    return server_ip


def receive_thread(conn):
    global active
    while True:
        try:
            data = conn.recv(2048)
            # print(data.decode())
        except ConnectionResetError:
            print(f"{RED_BACKGROUND}{BLACK}Lost connection to the server.{RESET}")
            active = False
            break


def send_to_server(data: str):
    client.send(data.encode())


def start_client():
    global server_ip, client
    print(f"{DARK_YELLOW}Searching for server in your network...{RESET}\n")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.SOL_UDP)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    address = ('<broadcast>', 10000)
    data = b"Castor Client"
    client_socket.sendto(data, address)
    client_socket.close()

    return_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return_sock.bind(('', 10001))

    return_sock.settimeout(5)
    try:
        recv_data, addr = return_sock.recvfrom(2048)
        print(f"{GREEN}Found a Castor server at {BOLD}{CYAN}{addr[0]}:{addr[1]}{RESET}")
        return_sock.close()
    except TimeoutError:
        print(f"{RED}Could not find a Castor server in your network.{RESET}")
        return_sock.close()
        return

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((addr[0], 9999))
    server_ip = addr[0]
    print(f"{GREEN}Connected to server {DARK_YELLOW_BACKGROUND}{BLACK}{server_ip}{RESET}\n")

    _thread.start_new_thread(receive_thread, (client,))

    try:
        while active:
            pass
    except KeyboardInterrupt:
        print(f"{RED_BACKGROUND}{BLACK}Keyboard interrupt.{RESET}")

    print(f"{RED}Stopped Client.{RESET}")


if __name__ == '__main__':
    start_client()
