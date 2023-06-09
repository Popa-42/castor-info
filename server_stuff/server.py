import socket
from time import sleep as wait

import sys

# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, 'C:\\Users\\EGo\PycharmProjects\\castor-info')

import castor.game

from terminal_colors import *
import argparse

parser = argparse.ArgumentParser(description="Castor Server")

parser.add_argument("-c", "--color", help="Uses colored terminal outputs. Terminal must support colors.",
                    action="store_true")

args = parser.parse_args()

colored_terminal: bool = args.color

clients = []
sock: socket.socket = ...
discovery_sock: socket.socket = ...


def send_to_all_clients(action: str):
    global clients, game
    for cl in range(len(clients)):
        send_action(cl, "TURN_END")


def get_response(client_index: int) -> dict:
    response = b""
    response: bytes = clients[client_index][0].recv(2048)
    response: str = response.decode()
    response: dict = eval(response)
    print(response)
    return response


def send_action(client_index: int, action: str):
    msg = {}
    msg = {"action": action}
    clients[client_index][0].send(str(msg).encode())


def gamerunner():
    global game, clients
    while True:
        # Server sendet "TURN_START"
        current_player = game.current_player
        send_action(current_player, "TURN_START")
        print(f"Turn start for player {current_player}, {clients[current_player][1][0]}:{clients[current_player][1][1]}")
        # Server wartet auf Antwort
        try:
            if rspns := get_response(current_player) == "DRAW_ABLAGE":
                print(rspns)
                print(f"{GREEN_BACKGROUND}{BLACK}Ablage!{RESET}")
                wait(0.1)

            if rspns := get_response(current_player) == "DRAW_DECK":
                print(rspns)
                print(f"{DARK_YELLOW_BACKGROUND}{BLACK}Deck!{RESET}")
                response = get_response(current_player)
                print(response)
                pass
        except SyntaxError:
            print()
            print(f"{DARK_YELLOW_BACKGROUND}{BLACK} A connection error occurred. {RESET}")

        # Sendet "TURN_END" an ALLE Spieler und nächsten Spieler in game
        send_action(current_player, "TURN_END")
        end_turn()


def end_turn():
    global game, clients
    # send_to_all_clients("TURN_END")
    game.next_player()


def search_connections(max_clients: int = 4):
    global sock, discovery_sock, clients, game
    # Ende, wenn mehr als max Clients
    while len(clients) < max_clients:
        # Versuche eine Verbindung herzustellen
        recv_data, addr = discovery_sock.recvfrom(2048)
        client_ip = addr[0]

        if colored_terminal:
            print(f"{GREEN}Received UDP packet from {CYAN}{client_ip}:{addr[1]}{RESET}")
        else:
            print(f"Received UDP packet from {client_ip}:{addr[1]}")

        address = (client_ip, 10001)
        return_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        return_socket.sendto("Castor Server".encode(), address)
        return_socket.close()

        if colored_terminal:
            print(f"{GREEN}Sent UDP return packet to {CYAN}{client_ip}{RESET}")
        else:
            print(f"Sent UDP return packet to {client_ip}")

        (conn, addr) = sock.accept()
        clients.append((conn, addr))

        if colored_terminal:
            print(f"{GREEN_BACKGROUND}{BLACK}TCP Connected to {DARK_YELLOW_BACKGROUND}{client_ip}{RESET}\n\n"
                  f"{BLUE}Number of connected Clients: "
                  f"{BOLD}{YELLOW}{len(clients)}{RESET_WEIGHT}{DARK_YELLOW}/{max_clients}{RESET}\n")
        else:
            print(f"TCP Connected to {client_ip}\n\n"
                  f"Number of connected Clients: {len(clients)}/{max_clients}\n")


def new_server():
    global sock, discovery_sock, game
    # TCP Connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_port = 9999
    server_name = ''
    server_address = (server_name, server_port)
    sock.bind(server_address)
    sock.listen()

    if colored_terminal:
        print(f"{GREEN}Started Castor server on port {BOLD}{DARK_YELLOW}{server_port}{RESET}\n")
    else:
        print(f"Started Castor server on port {server_port}\n")

    # SERVER DISCOVERY
    discovery_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    discovery_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    discovery_sock.bind(("", 10000))


def start_server(max_clients):
    global game
    # Create a new server
    new_server()
    # Search for connecting clients
    search_connections(max_clients)

    if colored_terminal:
        print(f"{GREEN_BACKGROUND}{BLACK} Starting the game... {RESET}\n")
    else:
        print(f"Starting the game...\n")

    # MAIN LOOP: The game function
    gamerunner()


if __name__ == '__main__':
    game = castor.game.Game()
    start_server(4)
