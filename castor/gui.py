import pyglet
import pyglet.window.key as key
from pyglet.window import mouse

display = pyglet.canvas.Display()
screens = display.get_screens()
window = pyglet.window.Window(fullscreen=True,
                              caption="Ursprünglicher Titel",
                              screen=screens[0],
                              style=pyglet.window.Window.WINDOW_STYLE_DIALOG)
# Den Fenstertitel ändern
window.set_caption("Neuer Titel")
# Fullscreen ändern
window.set_fullscreen(False)

label = pyglet.text.Label('Hello, world!',
                          font_name='Comic Sans MS',
                          font_size=36,
                          x=window.width // 2, y=window.height // 2,
                          anchor_x='center', anchor_y='center')


fullscreen = False


def toggle_fullscreen():
    global fullscreen
    if fullscreen:
        window.set_fullscreen(False)
        fullscreen = False
    elif not fullscreen:
        window.set_fullscreen(True)
        fullscreen = True


# Wird jedes Frame geupdatet
@window.event
def on_draw():
    window.clear()
    label.draw()


# Detect whether a key was pressed
# WICHTIG: Immer alle Parameter auflisten, auch wenn sie nicht benutzt werden! (-> wie hier `modifiers`)
@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.F11:
        toggle_fullscreen()


# Detect whether a mouse button was pressed
@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        print('The left mouse button was pressed.')


# Erstelle das Fenster
if __name__ == '__main__':
    pyglet.app.run()
