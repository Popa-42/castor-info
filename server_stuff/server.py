import socket

import castor.game
from terminal_colors import *
import argparse

from castor import *

parser = argparse.ArgumentParser(description="Castor Server")

parser.add_argument("-c", "--color", help="Uses colored terminal outputs. Terminal must support colors.",
                    action="store_true")

args = parser.parse_args()

colored_terminal: bool = args.color

clients = []
sock: socket.socket = ...
discovery_sock: socket.socket = ...


def update():
    global game
    send_to_all_clients(game.export_current_state())


def turn(clientnum):
    print(f"Spieler {clientnum} ist dran.")
    clients[clientnum][0].send("TURN_START".encode())

    response = clients[clientnum][0].recv(2048)
    response = response.decode()

    print(f"Spieler sagt {response}.")

    if response == "DRAW_ABLAGE":
        # Spieler zieht vom Ablagestapel
        # und darf danach nochmal spielen

        # TODO: Gebe Spieler eine Karte

        # TODO: Zeige Spieler eine Karte vom Deck

        response = clients[clientnum][0].recv(2048)
        response = response.decode()

        if response == "TAKE_CARD":
            print("Spieler nimmt die Karte")
            pass
        elif response == "THROW_CARD":
            print("Spieler nimmt die Karte nicht")
            pass

    elif response == "DRAW_DECK":
        card = game.draw_card()
        show_card(clientnum, str(card))

        response = clients[clientnum][0].recv(2048)
        response = response.decode()

        if response == "TAKE_CARD":
            print("Spieler nimmt die Karte")
            pass
        elif response == "THROW_CARD":
            print("Spieler nimmt die Karte nicht")
            pass

    clients[clientnum][0].send("TURN_END".encode())
    print("Zug ist vorbei.")


def show_card(clientnum, card):
    clients[clientnum][0].send(card.encode())


def end_turn(clientnum):
    clients[clientnum][0].send("TURN_END".encode())


def send_to_client(conn, data: bytes):
    conn.send(data)


def send_to_all_clients(data: bytes):
    global clients, game
    for cl in clients:
        cl[0].send(data)


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
                  f"{BLUE}Number of connected Clients: {BOLD}{YELLOW}{len(clients)}{RESET_WEIGHT}{DARK_YELLOW}/{max_clients}{RESET}\n")
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


def start_server(max_clients, tick_function):
    global game
    # Create a new server
    new_server()
    # Search for connecting clients
    search_connections(max_clients)

    if colored_terminal:
        print(f"{GREEN_BACKGROUND}{BLACK} Starting the game... {RESET}\n")
    else:
        print(f"Starting the game...\n")
    turn(3)
    # MAIN LOOP: The game function

    while True:
        try:
            tick_function()
        except KeyboardInterrupt:
            if colored_terminal:
                print(f"\n{RED_BACKGROUND}{BLACK} Server stopped due to keyboard interrupt. {RESET}")
            else:
                print(f"\nServer stopped due to keyboard interrupt.")
            break


if __name__ == '__main__':
    game = castor.game.Game()
    start_server(4, lambda: ...)
