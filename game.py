import time

import pyglet
from pyglet import shapes

FPS_LIMIT = 120.0
config = pyglet.gl.Config(sample_buffers=1, samples=4)
window = pyglet.window.Window(config=config,width=900,height=600,caption='Ping pong game')
icon = pyglet.image.load('menu_icon.ico')
window.set_icon(icon)
window.set_location(323, 104)
square = shapes.Rectangle(x=200, y=0, width=5, height=600, color=(255,255,255))
label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

def update(dt):
    print('updating...')

@window.event
def on_draw():
    window.clear()
    label.draw()
    square.draw()
    window.switch_to()

pyglet.clock.schedule_interval(update,1/FPS_LIMIT)
pyglet.app.run()