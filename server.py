import socket
import time

from castor.game import *

from terminal_colors import *
import argparse

# Farbiges Terminal
parser = argparse.ArgumentParser(description="Castor Server")
parser.add_argument("-c", "--color", help="Uses colored terminal outputs. Terminal must support colors.",
                    action="store_true")
args = parser.parse_args()
colored_terminal: bool = args.color

# Globale Variablen
clients = []
sock: socket.socket = ...
discovery_sock: socket.socket = ...


def new_server():
    """Erstelle einen neuen Server"""
    global sock, discovery_sock, game
    # TCP Connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_port = 9999
    server_name = ''
    server_address = (server_name, server_port)
    try:
        sock.bind(server_address)
    except OSError:
        print(f"{DARK_RED_BACKGROUND}{BLACK}OSError{RESET}")
        exit()
    sock.listen()

    if colored_terminal:
        print(f"{GREEN}Started Castor server on port {BOLD}{DARK_YELLOW}{server_port}{RESET}\n")
    else:
        print(f"Started Castor server on port {server_port}\n")

    # SERVER DISCOVERY
    discovery_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    discovery_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    discovery_sock.bind(("", 10000))


def search_connections(max_clients: int = 4):
    """Suche nach Clients"""
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


def try_conn(function):
    """Exit, wenn ConnectionResetError"""
    try:
        function()
        return True
    except ConnectionResetError:
        print(f"\n{DARK_RED_BACKGROUND}                                   {RESET}")
        print(f"{DARK_RED_BACKGROUND}{YELLOW}  - - - - - {BOLD}FATAL ERROR{RESET_WEIGHT} - - - - -  {RESET}")
        print(f"{DARK_RED_BACKGROUND}                                   {RESET}")
        print(f"\n{RED}Server lost connection to a Client.{RESET}")
        print(f"\n{RED}Stopping Server...{RESET}")
        exit()


def send_to_all_clients(action: str):
    """Sendet eine Nachricht an alle Clients"""
    global clients, game
    for cl in range(len(clients)):
        send_action(cl, action)


def send(client_index: int, msg):
    """Sendet eine Nachricht an einen bestimmten Client"""
    clients[client_index][0].send(str(msg).encode())


def get_response(client_index: int) -> dict:
    """Empfange eine Nachricht von einem bestimmten Client"""
    response: bytes = clients[client_index][0].recv(2048)
    response: str = response.decode().split("}")[0] + "}"
    try:
        response: dict = eval(response)
    except SyntaxError:
        print(f"{RED_BACKGROUND}{BLACK}An evaluation error occurred.{RESET}")
        print(f"{RED}Stopping Server...{RESET}")
        exit()
    return response


def send_action(client_index: int, action: str):
    """Sende eine Aktion an einen bestimmten Client"""
    msg = {"action": action}
    send(client_index, msg)


def send_card(client_index: int, card: str):
    """Sende eine Karte an einen bestimmten Client"""
    msg = {"card": card}
    send(client_index, msg)


def gamerunner():
    global game, clients

    # Spiel: Teile allen Spielern Karten aus
    game.deal_cards_to_all()

    # Broadcast an alle Clients: Äußere beiden Karten
    for c in range(4):
        hand = game.players[c].get_hand()
        send(c, hand)

    while True:
        current_player = game.current_player
        try_conn(lambda: send_action(current_player, "TURN_START"))
        print(
            f"\n{DARK_BLUE_BACKGROUND}Turn start for player {current_player}, "
            # IP-Adresse und Port
            f"{DARK_YELLOW}{BOLD}{clients[current_player][1][0]}:{clients[current_player][1][1]}{RESET}")
        # Server wartet auf Antwort
        resp = get_response(current_player)

        # Spieler will von der Ablage ziehen
        if resp['action'] == "DRAW_ABLAGE":
            # Debug
            print(f"{GREEN_BACKGROUND}{BLACK}Ablage!{RESET}")

            game.throw_card_to_ablage(game.draw_card())

            # Karte vom Ablagestapel ziehen und senden
            card = game.draw_ablage()
            if card:
                send_card(current_player, str(card))

                resp = get_response(current_player)
                print(resp)
                if resp["action"] == "KEEP_CARD_AT_INDEX":
                    index = int(resp["index"])
                    print(game.get_current_player().get_hand())
                    success = game.get_current_player().swap_card_with_index(card, index)
                    print("Success:", success)

                    while not success:
                        send_action(current_player, "SEND_INDEX")
                        resp = get_response(current_player)
                        index = int(resp["index"])
                        success = game.get_current_player().swap_card_with_index(card, index)

                    print("Neue Hand:", game.get_current_player().get_hand())

                    send_action(current_player, "SUCCESS")
                    time.sleep(0.5)

                    send(current_player,
                         "{'action': 'GET_CARDS', 'hand': " + f"{game.get_current_player().get_hand()}" +
                         ", 'ablage': " + f"{game.get_oberste_ablage()}" + "}"
                         )

            else:
                response = {"card": "{'NONE': None}"}
                send(current_player, response)

        elif resp['action'] == "DRAW_DECK":
            print(f"{DARK_YELLOW_BACKGROUND}{BLACK}Deck!{RESET}")
            print(f"")
            card = game.draw_card()
            resp = get_response(current_player)

            if resp['action'] == "TAKE_CARD":
                send_card(current_player, str(card))
                # TODO: player selects hand slot

            elif resp['action'] == "THROW_CARD":
                game.throw_card_to_ablage(card)
                # TODO: broadcast to all players for ingamethrow

            else:
                print(resp)
        elif resp['action'] == "NEXT_PLAYER":
            pass
        else:
            print(resp)

        # Sendet "TURN_END" an ALLE Spieler und nächsten Spieler in game
        send_action(current_player, "TURN_END")
        end_turn()


def end_turn():
    """Beende den Zug des aktiven Spielers und bestimme den nächsten Spieler"""
    global game, clients
    game.next_player()


def start_server(max_clients):
    """Setze einen neuen Castor Server auf, suche nach Clients und starte das Spiel"""
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
    game = Game()
    start_server(4)
