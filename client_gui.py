import client
import pyglet
import threading

window = pyglet.window.Window(700, 500)

text = pyglet.text.Label(
    text="Searching for Castor Server in your network...",
    font_name="Consolas",
    color=(173, 140, 0, 255),
    x=40,
    y=window.height - 20,
    anchor_x="left",
    anchor_y="center"
)

arrows = ...


def make_arrows(i: int):
    global arrows
    arrows = [pyglet.text.Label(
        text=">",
        font_name="Consolas",
        x=20,
        y=window.height - (i+1)*20,
        anchor_x="left",
        anchor_y="center"
    ) for i in range(i)]


outputs: int = 1


@window.event
def on_draw():
    window.clear()
    text.draw()
    make_arrows(outputs)
    for a in arrows:
        a.draw()


if __name__ == "__main__":
    console = threading.Thread(target=lambda: client.start_client()).start()
    pyglet.app.run()
