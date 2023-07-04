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
    global hand
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
        elif data["action"] == "HAND":
            hand_str = data["value"]
            hand = eval(hand_str)
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
back = pyglet.resource.image('Firebird/bg.jpg')

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
        window.set_size(1000, 750)

        current_hand = [pyglet.resource.image(f"Firebird/{c}.jpg") for c in hand]
        current_hand.reverse()
        draw_horizontal(625, 75, current_hand)
        for img in current_hand:
            img.width, img.height = 90, 127
            img.anchor_x = img.width / 2
            img.anchor_y = img.height / 2
        draw_horizontal(625, 625, [back for _ in range(4)])
        draw_vertical(40, 500, [back for _ in range(4)])
        draw_vertical(800, 500, [back for _ in range(4)])
        back.blit(150, 625)

    elif hand is ... and server_found:
        window.set_size(700, 250)
        text = pyglet.text.Label(
            text="Waiting for Server to start the game...",
            font_name="Segoe UI",
            font_size=26,
            color=(255, 255, 0, 255),
            x=window.width//2,
            y=window.height//2,
            anchor_x="center",
            anchor_y="center"
        )
        text.draw()
    else:
        window.set_size(700, 250)
        text = pyglet.text.Label(
            text="Searching Server in your network...",
            font_name="Segoe UI",
            font_size=26,
            color=(255, 0, 0, 255),
            x=window.width//2,
            y=window.height//2,
            anchor_x="center",
            anchor_y="center"
        )
        text.draw()


def draw_vertical(x, y, images: list[pyglet.image]):
    imgs = [image.get_transform(rotate=90) for image in images]

    for i, img in enumerate(imgs):
        c = ClickableImage(img, x, y - (card_spacing * i))
        c.draw()
        add_if_not_exist(c)


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

