import pyglet
import client

window = pyglet.window.Window(700, 500)

bg = pyglet.shapes.Rectangle(
    x=0,
    y=0,
    width=window.width,
    height=window.height,
    color=(255, 255, 255, 255)
)

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
        color=(0, 0, 0, 255),
        x=20,
        y=window.height - (i+1)*20,
        anchor_x="left",
        anchor_y="center"
    ) for i in range(i)]


@window.event
def on_draw():
    window.clear()
    bg.draw()
    text.draw()
    make_arrows(8)
    for a in arrows:
        a.draw()


if __name__ == "__main__":
    pyglet.app.run()
