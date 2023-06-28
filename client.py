import socket
from terminal_colors import *

server_ip = ""
server: socket.socket = ...


def get_server_ip():
    return server_ip


def receive():
    data: bytes = server.recv(2048)
    data: str = data.decode().split("}")[0] + "}"
    data: dict = eval(data)
    return data


def receive_card():
    data: bytes = server.recv(2048)
    # {'card': "{'farbe': 1, 'wert': 2}"}
    data: str = data.decode().split("}")[0] + '}"}'
    data: dict = eval(data)
    return data


def send(response: dict):
    global server
    server.send(str(response).encode())


def send_action(action: str):
    response = {"action": action}
    send(response)


def gamerunner():
    while True:
        hand = server.recv(2048).decode()
        print("Hand:", hand)

        data = receive()

        if data["action"] == "TURN_START":
            action = input("Was willst du tun?\n[1] Ablage\n[2] Deck\n > ")

            # Spieler will von der Ablage ziehen
            if action == "1":
                send_action("DRAW_ABLAGE")

                # Empfange eine Karte vom Server
                data = receive_card()
                # print(data["card"])

                # Prüfe, ob auf dem Ablagestapel eine Karte liegt
                if data["card"] != "{'NONE': None}":
                    # Debug
                    print(data["card"])
                    index = input("An welche Stelle soll die Karte gelegt werden?\n > ")
                    try:
                        index = int(index)
                        response = {"action": "KEEP_CARD_AT_INDEX", "index": index}
                        send(response)
                        data = receive()["action"]
                    except ValueError:
                        data = "SEND_INDEX"

                    # Probiere es so lange wieder, bis Index valide
                    while data == "SEND_INDEX":
                        print(f"{RED}Ein Fehler ist aufgetreten.{RESET}")
                        index = input("An welche Stelle soll die Karte gelegt werden?\n > ")
                        try:
                            index = int(index)
                            response = {"action": "KEEP_CARD_AT_INDEX", "index": index}
                            send(response)
                            data = receive()["action"]
                        except ValueError:
                            pass

                    # TODO: Server broadcast - THROWN_CARD + 3s Warten auf Client Throw,
                    #  wenn keine Antwort: Client MUSS eine Karte ziehen

                else:
                    pass

            elif action == "2":
                response = {"action": "DRAW_DECK"}
                send(response)

                response = {"action": "TAKE_CARD"}
                send(response)
            else:
                response = {"action": "NEXT_PLAYER"}
                send(response)

        elif data["action"] == "TURN_END":
            pass
        elif data["action"] == "ERROR" or data == "":
            print(f"\n{RED_BACKGROUND}{BLACK}A fatal error occured.{RESET}")
            break


def start_client():
    global server_ip, server
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

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((addr[0], 9999))
    server_ip = addr[0]
    print(f"{GREEN}Connected to server {DARK_YELLOW_BACKGROUND}{BLACK}{server_ip}{RESET}\n")

    try:
        gamerunner()
    except KeyboardInterrupt:
        print(f"{RED_BACKGROUND}{BLACK}Keyboard interrupt.{RESET}")

    print(f"{RED}Stopped Client.{RESET}")


if __name__ == '__main__':
    start_client()
