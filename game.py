import pyglet
import random
from pyglet import shapes
from pyglet.window import key

from game_objects import Ball, Game

FPS_LIMIT = 120.0

window = pyglet.window.Window(width=900,height=600,caption='Ping pong game')
icon = pyglet.image.load('menu_icon.ico')
window.set_icon(icon)
window.set_location(323, 104)
square = shapes.Rectangle(x=200, y=0, width=7, height=600, color=(255,0,255))
game = Game(4)
ball = Ball(x=200, y=0,radius=10)
for i in game.players:
    window.push_handlers(i.platform.key_handler)
label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=16,
                          x=0, y=window.height//2,
                          anchor_x='left', anchor_y='top')


def update(dt):
    # update all objects and send information to players
    for player in game.players:
        player.platform.update(dt)

@window.event
def on_draw():
    window.clear()
    # draw all objects
    label.draw()
    square.draw()
    game.draw_board()

pyglet.clock.schedule_interval(update,1/FPS_LIMIT)
pyglet.app.run()