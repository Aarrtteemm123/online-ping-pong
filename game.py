import pyglet
import random
from pyglet import shapes
from pyglet.window import key

from game_objects import Ball

FPS_LIMIT = 120.0

window = pyglet.window.Window(width=900,height=600,caption='Ping pong game')
icon = pyglet.image.load('menu_icon.ico')
window.set_icon(icon)
window.set_location(323, 104)
square = shapes.Rectangle(x=200, y=0, width=5, height=600, color=(255,255,255))
ball = Ball(x=0,y=0,radius=50,color=(255,255,255))
ball.speed_x = 200
ball.speed_y = 200
label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

def update(dt):
    ball.check_bounds(900,600,200,0)
    ball.update(dt)

@window.event
def on_draw():
    window.clear()
    label.draw()
    ball.draw()
    square.draw()

pyglet.clock.schedule_interval(update,1/FPS_LIMIT)
pyglet.app.run()