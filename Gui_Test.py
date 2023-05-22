import pyglet

w = pyglet.window.Window(1000, 750)
image = pyglet.resource.image('Platzhalter_Ass.jpg')

@w.event
def on_draw():
    w.clear()
    image.blit(20,40)
    

pyglet.app.run()
