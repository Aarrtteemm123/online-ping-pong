import pyglet,random
from pyglet import shapes
from game_objects import  Game
from config import *

window = pyglet.window.Window(width=WINDOW_WIDTH,height=WINDOW_HEIGHT,caption=WINDOW_CAPTION)
icon = pyglet.image.load('menu_icon.ico')
window.set_icon(icon)
window.set_location(WINDOW_POS_X, WINDOW_POS_Y)
square = shapes.Rectangle(x=200, y=0, width=7, height=600, color=(255,0,255))
game = Game(['Pl1','Pl2','Pl3','Pl4'])
while game.ball.speed_x == 0 and game.ball.speed_y == 0:
    game.ball.speed_x = random.choice([0, 250, -250])
    game.ball.speed_y = random.choice([0, 250, -250])

for i in game.players:
    window.push_handlers(i.platform.key_handler)


def update(dt):
    # update all objects and send information to players
    for player in game.players:
        player.platform.update(dt)
    game.ball.update(dt)
    game.ball.check_bounds(WINDOW_WIDTH,WINDOW_HEIGHT,BOARD_POS_X,BOARD_POS_Y)

@window.event
def on_draw():
    window.clear()
    square.draw()
    game.draw_labels()
    game.draw_board()

pyglet.clock.schedule_interval(update,1/FPS_LIMIT)
pyglet.app.run()