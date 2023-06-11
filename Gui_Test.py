import pyglet

w = pyglet.window.Window(1000, 750)
image = pyglet.resource.image('Platzhalter_Ass.jpg')
im = pyglet.resource.image('Platzhalter_Ruck.jpg')
rueck_image = pyglet.image.load('Platzhalter_Ruck.jpg')

batch = pyglet.graphics.Batch()

# Set anchor points for rotation
image.anchor_x = image.width / 2
image.anchor_y = image.height / 2
im.anchor_x = image.width / 2
im.anchor_x = image.height / 2


@w.event
def on_draw():
    w.clear()

    draw_horizontal(75, image)
    draw_horizontal(625, im)

    draw_vertical(40, im)
    draw_vertical(800, im)

    im.blit(150, 625)


def draw_vertical(x, image):
    rotated_image = image.get_transform(rotate=90)

    rotated_image.blit(x, 500)
    rotated_image.blit(x, 425)
    rotated_image.blit(x, 575)
    rotated_image.blit(x, 350)

def draw_horizontal(y, image):
    image.blit(500, y)
    image.blit(425, y)
    image.blit(575, y)
    image.blit(350, y)


pyglet.app.run()
