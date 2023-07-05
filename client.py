import socket
from terminal_colors import *

import pyglet

import threading


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                    C L I E N T   E N G I N E
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

server_ip = ""
server: socket.socket = ...

hand: list[str] = ...
ablage_karte: str = ...
server_found = False


def get_server_ip():
    return server_ip


def receive():
    data: bytes = server.recv(2048)
    data: str = data.decode().split("}")[0] + "}"
    try:
        data: dict = eval(data)
    except SyntaxError:
        print(f"{RED_BACKGROUND}{BLACK}Lost connection to the server.{RESET}")
        print(f"{RED}Stopping Client...{RESET}")
        pyglet.app.exit()
        exit()
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
    global hand, ablage_karte
    hand_str = server.recv(2048).decode()
    hand = eval(hand_str)
    print("Hand:", hand)

    while True:
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
        elif data["action"] == "GET_CARDS":
            cards_str = data["value"]
            hand = eval(cards_str)["hand"]
        elif data["action"] == "ERROR" or data == "":
            print(f"\n{RED_BACKGROUND}{BLACK}A fatal error occured.{RESET}")
            pyglet.app.exit()
            break


def start_client():
    global server_ip, server, server_found
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
        pyglet.app.exit()
        return

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((addr[0], 9999))
    server_ip = addr[0]
    print(f"{GREEN}Connected to server {DARK_YELLOW_BACKGROUND}{BLACK}{server_ip}{RESET}\n")
    server_found = True

    try:
        gamerunner()
    except KeyboardInterrupt:
        print(f"{RED_BACKGROUND}{BLACK}Keyboard interrupt.{RESET}")
        pyglet.app.exit()

    print(f"{RED}Stopped Client.{RESET}")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                            G  U  I
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


window = pyglet.window.Window(700, 250)
image = pyglet.resource.image("Firebird/#1.jpg")
back = pyglet.resource.image('Firebird/bg.png')

back.width, back.height = 90, 127
image.width, image.height = 90, 127

batch = pyglet.graphics.Batch()

# Set anchor points for rotation
image.anchor_x = image.width / 2
image.anchor_y = image.height / 2
back.anchor_x = image.width / 2
back.anchor_x = image.height / 2

card_spacing = 100


class ClickableImage(pyglet.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self_x = self.x - self.width / 2
            self_y = self.y - self.height / 2
            if self_x <= x <= self_x + self.width and self_y <= y <= self_y + self.height:
                print(image)
                print("Image clicked at coordinates ({}, {})".format(x, y))

    def draw(self):
        self.image.blit(self.x, self.y)


def add_if_not_exist(obj):
    for c in cards:
        if c.x == obj.x and c.y == obj.y:
            return
    cards.append(obj)


cards = []


@window.event
def on_draw():
    global hand, server_found
    window.clear()

    if hand is not ... and server_found:
        # Spiel gestartet
        window.set_size(1000, 750)

        # Bildkarten
        current_hand = [pyglet.resource.image(f"Firebird/{c}.jpg") for c in hand]
        current_hand.reverse()
        draw_horizontal(625, 75, current_hand)
        for img in current_hand:
            img.width, img.height = 90, 127
            img.anchor_x = img.width / 2
            img.anchor_y = img.height / 2

        # Rückseiten: Andere Spieler
        draw_horizontal(625, 625, [back for _ in range(4)])
        draw_vertical(40, 500, [back for _ in range(4)])
        draw_vertical(800, 500, [back for _ in range(4)])

        # Nachziehstapel
        back.blit(150, 625)

        # Ablagestapel
        if ablage_karte is not Ellipsis:
            ablage = pyglet.resource.image(f"Firebird/{ablage_karte}.jpg")
        else:
            ablage = pyglet.resource.image(r"Firebird/#2.jpg")
        ablage.width, ablage.height = 90, 127
        ablage.anchor_x, ablage.anchor_y = ablage.width//2, ablage.height//2
        ablage.blit(460, 300)

    elif hand is ... and server_found:
        # Server gefunden und verbunden; warten auf Spielstart
        bg = pyglet.shapes.Rectangle(
            x=0,
            y=0,
            width=window.width,
            height=window.height,
            color=(13, 17, 23, 255)
        )
        text1 = pyglet.text.Label(
            text="Searching for Server in your network...",
            font_name="Consolas",
            font_size=16,
            x=50,
            y=window.height - 20,
            anchor_x="left",
            anchor_y="top",
        )
        text2 = pyglet.text.Label(
            text=f"Connected to Server {server.getpeername()[0]}:{server.getpeername()[1]}",
            font_name="Consolas",
            font_size=16,
            x=50,
            y=window.height - 50,
            anchor_x="left",
            anchor_y="top",
        )
        text3 = pyglet.text.Label(
            text="Waiting for Server to start the game...",
            font_name="Consolas",
            font_size=16,
            x=50,
            y=window.height - 80,
            anchor_x="left",
            anchor_y="top",
        )
        bg.draw()
        text1.draw()
        text2.draw()
        text3.draw()
    else:
        # Noch kein Server gefunden
        bg = pyglet.shapes.Rectangle(
            x=0,
            y=0,
            width=window.width,
            height=window.height,
            color=(13, 17, 23, 255)
        )
        chevron = pyglet.text.Label(
            text=">",
            font_name="Consolas",
            font_size=16,
            x=20,
            y=window.height - 20,
            anchor_x="left",
            anchor_y="top"
        )
        text = pyglet.text.Label(
            text="Searching for Server in your network...",
            font_name="Consolas",
            font_size=16,
            x=50,
            y=window.height - 20,
            anchor_x="left",
            anchor_y="top"
        )
        chevron.draw()
        bg.draw()
        text.draw()


def draw_vertical(x: int, y: int, images: list[pyglet.image]):
    imgs = [pyglet.sprite.Sprite(image, x, y) for image in images]

    for i, img in enumerate(imgs):
        img.rotation = 90
        img.x, img.y = x, y - (card_spacing * i)
        img.draw()
        add_if_not_exist(img)


def draw_horizontal(x, y, images: list[pyglet.image]):
    for i, img in enumerate(images):
        c = ClickableImage(img, x - (card_spacing * i), y)
        c.draw()
        add_if_not_exist(c)


@window.event
def on_mouse_press(x, y, button, modifiers):
    for c in cards:
        c.on_mouse_press(x, y, button, modifiers)


if __name__ == '__main__':
    engine = threading.Thread(target=start_client)

    engine.start()
    pyglet.app.run()

