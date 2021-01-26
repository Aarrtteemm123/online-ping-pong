import pyglet
from pyglet import shapes
from pyglet.window import key
from config import *

class Game:
    def __init__(self, player_names):
        self.number_players = len(player_names)
        self.board = shapes.Rectangle(x=BOARD_POS_X, y=BOARD_POS_Y, width=BOARD_WIDTH, height=BOARD_HEIGHT, color=BOARD_COLOR)
        dx, dy = self.board.x, self.board.y
        w, h = self.board.width, self.board.height
        self.ball = Ball(x=dx + w // 2, y=dy + h // 2, radius=BALL_RADIUS, segments=BALL_SEGMENTS, color=BALL_COLOR)
        if self.number_players == 1:
            self.players = [Player(player_names[0], Platform('left', x=dx, y=dy + h // 2, width=PLATFORM_WIDTH, height=PLATFORM_HEIGHT)),
                            Bot('Bot', Platform('right', x=w + dx - PLATFORM_WIDTH, y=dy + h // 2, width=PLATFORM_WIDTH, height=PLATFORM_HEIGHT))]
            self.labels_lst = [
                pyglet.text.Label(f'{player_names[0]} - 0', font_name='Times New Roman', font_size=FONT_SIZE, x=10, y=h * 0.25,
                                  anchor_x='left', anchor_y='top'),
                pyglet.text.Label('Bot - 0', font_name='Times New Roman', font_size=FONT_SIZE, x=10, y=h * 0.75,
                                  anchor_x='left', anchor_y='top'),
            ]
        elif self.number_players == 2:
            self.players = [Player(player_names[0], Platform('left', x=dx, y=dy + h // 2, width=PLATFORM_WIDTH, height=PLATFORM_HEIGHT)),
                            Player(player_names[1],
                                   Platform('right', x=w + dx - PLATFORM_WIDTH, y=dy + h // 2, width=PLATFORM_WIDTH, height=PLATFORM_HEIGHT))]
            self.labels_lst = [
                pyglet.text.Label(f'{player_names[0]} - 0', font_name='Times New Roman', font_size=FONT_SIZE, x=10, y=h * 0.25,
                                  anchor_x='left', anchor_y='top'),
                pyglet.text.Label(f'{player_names[1]} - 0', font_name='Times New Roman', font_size=FONT_SIZE, x=10, y=h * 0.75,
                                  anchor_x='left', anchor_y='top'),
            ]
        elif self.number_players == 3:
            self.players = [Player(player_names[0], Platform('left', x=dx, y=dy + h // 2, width=PLATFORM_WIDTH, height=PLATFORM_HEIGHT)),
                            Player(player_names[1],
                                   Platform('top', x=dx + w // 2, y=dy + h - PLATFORM_WIDTH, width=PLATFORM_HEIGHT, height=PLATFORM_WIDTH)),
                            Bot('Bot', Platform('right', x=w + dx - PLATFORM_WIDTH, y=dy + h // 2, width=PLATFORM_WIDTH, height=PLATFORM_HEIGHT)),
                            Player(player_names[2], Platform('bottom', x=dx + w // 2, y=dy, width=PLATFORM_HEIGHT, height=PLATFORM_WIDTH))]
            self.labels_lst = [
                pyglet.text.Label(f'{player_names[0]} - 0', font_name='Times New Roman', font_size=FONT_SIZE, x=10, y=h * 0.2,
                                  anchor_x='left', anchor_y='top'),
                pyglet.text.Label(f'{player_names[1]} - 0', font_name='Times New Roman', font_size=FONT_SIZE, x=10, y=h * 0.4,
                                  anchor_x='left', anchor_y='top'),
                pyglet.text.Label(f'{player_names[2]} - 0', font_name='Times New Roman', font_size=FONT_SIZE, x=10, y=h * 0.6,
                                  anchor_x='left', anchor_y='top'),
                pyglet.text.Label('Bot - 0', font_name='Times New Roman', font_size=FONT_SIZE, x=10, y=h * 0.8,
                                  anchor_x='left', anchor_y='top'),
            ]
        elif self.number_players == 4:
            self.players = [Player(player_names[0],
                                   Platform('left', x=dx, y=dy + h // 2, width=PLATFORM_WIDTH, height=PLATFORM_HEIGHT)),
                            Player(player_names[1],
                                   Platform('top', x=dx + w // 2, y=dy + h - PLATFORM_WIDTH, width=PLATFORM_HEIGHT,
                                            height=PLATFORM_WIDTH)),
                            Player(player_names[2], Platform('right', x=w + dx - PLATFORM_WIDTH, y=dy + h // 2, width=PLATFORM_WIDTH,
                                                height=PLATFORM_HEIGHT)),
                            Player(player_names[3], Platform('bottom', x=dx + w // 2, y=dy, width=PLATFORM_HEIGHT,
                                                             height=PLATFORM_WIDTH))]
            self.labels_lst = [
                pyglet.text.Label(f'{player_names[0]} - 0', font_name='Times New Roman', font_size=FONT_SIZE, x=10,
                                  y=h * 0.2,
                                  anchor_x='left', anchor_y='top'),
                pyglet.text.Label(f'{player_names[1]} - 0', font_name='Times New Roman', font_size=FONT_SIZE, x=10,
                                  y=h * 0.4,
                                  anchor_x='left', anchor_y='top'),
                pyglet.text.Label(f'{player_names[2]} - 0', font_name='Times New Roman', font_size=FONT_SIZE, x=10,
                                  y=h * 0.6,
                                  anchor_x='left', anchor_y='top'),
                pyglet.text.Label(f'{player_names[3]} - 0', font_name='Times New Roman', font_size=FONT_SIZE, x=10, y=h * 0.8,
                                  anchor_x='left', anchor_y='top'),
            ]

    def check_wall_collision(self):
        w, h = self.board.width, self.board.height
        collision = self.ball.check_bounds(WINDOW_WIDTH,WINDOW_HEIGHT,BOARD_POS_X,BOARD_POS_Y)
        if collision == 'left':
            self.players[0].score += 1
            self.labels_lst[0] = pyglet.text.Label(f'{self.players[0].name} - {self.players[0].score}', font_name='Times New Roman', font_size=FONT_SIZE, x=10, y=h * 0.2, anchor_x='left', anchor_y='top')
        elif collision == 'top':
            self.players[1].score += 1
            self.labels_lst[1] = pyglet.text.Label(f'{self.players[1].name} - {self.players[1].score}',
                                        font_name='Times New Roman', font_size=FONT_SIZE, x=10,
                                        y=h * 0.4, anchor_x='left', anchor_y='top')
        elif collision == 'right':
            self.players[2].score += 1
            self.labels_lst[2] = pyglet.text.Label(f'{self.players[2].name} - {self.players[2].score}',
                                        font_name='Times New Roman', font_size=FONT_SIZE, x=10,
                                        y=h * 0.6, anchor_x='left', anchor_y='top')
        elif collision == 'bottom':
            self.players[3].score += 1
            self.labels_lst[3] = pyglet.text.Label(f'{self.players[3].name} - {self.players[3].score}',
                                        font_name='Times New Roman', font_size=FONT_SIZE, x=10,
                                        y=h * 0.8, anchor_x='left', anchor_y='top')


    def set_score(self,player_name,new_score):
        pass

    def draw_labels(self):
        for label in self.labels_lst:
            label.draw()

    def draw_board(self):
        self.board.draw()
        for player in self.players:
            player.platform.draw()
        self.ball.draw()


class Player:
    def __init__(self, name, platform, score=0):
        self.name = name
        self.platform = platform
        self.score = score


class Bot(Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Ball(pyglet.shapes.Circle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.speed_x, self.speed_y = 0.0, 0.0

    def update(self, dt):
        self.x += self.speed_x * dt
        self.y += self.speed_y * dt

    def check_bounds(self, max_x, max_y, min_x, min_y):
        if self.x < min_x + self.radius:
            self.x = min_x + self.radius
            self.speed_x *= -1
            return 'left'
        elif self.x > max_x - self.radius:
            self.x = max_x - self.radius
            self.speed_x *= -1
            return 'right'
        elif self.y < min_y + self.radius:
            self.y = min_y + self.radius
            self.speed_y *= -1
            return 'bottom'
        elif self.y > max_y - self.radius:
            self.y = max_y - self.radius
            self.speed_y *= -1
            return 'top'


class Platform(pyglet.shapes.Rectangle):
    def __init__(self, pos, speed=50.0, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.pos = pos
        self.speed = speed
        self.key_handler = key.KeyStateHandler()

    def update(self, dt):
        if self.pos == 'left' and self.key_handler[key.LEFT]:
            self.y += self.speed * dt
        elif self.pos == 'left' and self.key_handler[key.RIGHT]:
            self.y -= self.speed * dt

        elif self.pos == 'right' and self.key_handler[key.LEFT]:
            self.y -= self.speed * dt
        elif self.pos == 'right' and self.key_handler[key.RIGHT]:
            self.y += self.speed * dt

        elif self.pos == 'top' and self.key_handler[key.LEFT]:
            self.x -= self.speed * dt
        elif self.pos == 'top' and self.key_handler[key.RIGHT]:
            self.x += self.speed * dt

        elif self.pos == 'bottom' and self.key_handler[key.LEFT]:
            self.x -= self.speed * dt
        elif self.pos == 'bottom' and self.key_handler[key.RIGHT]:
            self.x += self.speed * dt
