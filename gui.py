# Ich habe hier schonmal das Spielfeld mit einem ClickListener für die Karten:
# python
import pyglet

window = pyglet.window.Window(1000, 750)
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
    window.clear()

    draw_horizontal(625, 75, [image for _ in range(4)])
    draw_horizontal(625, 625, [back for _ in range(4)])

    draw_vertical(40, 500, [back for _ in range(4)])
    draw_vertical(800, 500, [back for _ in range(4)])

    back.blit(150, 625)


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


pyglet.app.run()
