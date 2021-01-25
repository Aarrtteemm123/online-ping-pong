import pyglet
import random
from pyglet import shapes

from game_objects import Ball, Game

FPS_LIMIT = 120.0

window = pyglet.window.Window(width=900,height=600,caption='Ping pong game')
icon = pyglet.image.load('menu_icon.ico')
window.set_icon(icon)
window.set_location(323, 104)
square = shapes.Rectangle(x=200, y=0, width=7, height=600, color=(255,0,255))
game = Game(['Anton'])
game.ball.speed_x = random.choice([0, 250, -250])
game.ball.speed_y = random.choice([0, 250, -250])

for i in game.players:
    window.push_handlers(i.platform.key_handler)


def update(dt):
    # update all objects and send information to players
    for player in game.players:
        player.platform.update(dt)
    game.ball.update(dt)
    game.ball.check_bounds(900,600,200,0)

@window.event
def on_draw():
    window.clear()
    square.draw()
    game.draw_labels()
    game.draw_board()

pyglet.clock.schedule_interval(update,1/FPS_LIMIT)
pyglet.app.run()