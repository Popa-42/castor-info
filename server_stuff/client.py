import socket
from time import sleep as wait

from terminal_colors import *

server_ip = ""
client: socket.socket = ...


def get_server_ip():
    return server_ip


def send_to_server(data: str):
    global client
    client.send(data.encode())


def gamerunner():
    global client
    while True:
        data: bytes = client.recv(2048)
        data: str = data.decode()
        data: dict = eval(data)

        print(f"Data ist {data}.")
        wait(0.1)

        if data["action"] == "TURN_START":
            print("Spieler ist dran.")
            action = input("Was willst du tun?\n[1] Ablage\n[2] Deck\n > ")
            if action == "1":
                response = {"action": "DRAW_ABLAGE"}
                client.send(str(response).encode())
                wait(0.1)

            response = ...
            response = {"action": "DRAW_DECK"}
            client.send(str(response).encode())
            wait(0.1)

            response = ...
            response = {"action": "TAKE_CARD"}
            client.send(str(response).encode())
            pass

        elif data["action"] == "TURN_END":
            pass
        elif data["action"] == "ERROR" or data == "":
            print(f"\n{RED_BACKGROUND}{BLACK}A fatal error occured.{RESET}")
            break


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

    try:
        gamerunner()
    except KeyboardInterrupt:
        print(f"{RED_BACKGROUND}{BLACK}Keyboard interrupt.{RESET}")

    print(f"{RED}Stopped Client.{RESET}")


if __name__ == '__main__':
    start_client()
