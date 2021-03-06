import json
import random
import pyglet
from pyglet import shapes
from pyglet.window import key
from config import *

class Game(pyglet.window.Window):

    def __init__(self, player_names, host_name, server=None, client=None):
        super().__init__(width=WINDOW_WIDTH,height=WINDOW_HEIGHT,caption=WINDOW_CAPTION)
        self.server = server
        self.client = client
        self.host_name = host_name
        self.set_icon(pyglet.image.load('menu_icon.ico'))
        self.set_location(WINDOW_POS_X, WINDOW_POS_Y)
        self.number_players = len(player_names)
        self.board = shapes.Rectangle(x=BOARD_POS_X, y=BOARD_POS_Y, width=BOARD_WIDTH, height=BOARD_HEIGHT, color=BOARD_COLOR)
        dx, dy = self.board.x, self.board.y
        w, h = self.board.width, self.board.height
        self.ball = Ball(x=dx + w // 2, y=dy + h // 2, radius=BALL_RADIUS, segments=BALL_SEGMENTS, color=BALL_COLOR)
        self.ball.set_random_speed_direction()
        if self.number_players == 1:
            self.players = [
                Player(player_names[0], Platform('left', x=dx, y=dy + h // 2, width=PLATFORM_WIDTH, height=PLATFORM_HEIGHT)),
                Bot('Bot', Platform('right', x=w + dx - PLATFORM_WIDTH, y=dy + h // 2, width=PLATFORM_WIDTH, height=PLATFORM_HEIGHT))
            ]
            self.labels_lst = [
                self.__get_label(player_names[0], 0, h * 0.25),
                self.__get_label('Bot', 0, h * 0.75)
            ]
        elif self.number_players == 2:
            self.players = [
                Player(player_names[0], Platform('left', x=dx, y=dy + h // 2, width=PLATFORM_WIDTH, height=PLATFORM_HEIGHT)),
                Player(player_names[1], Platform('right', x=w + dx - PLATFORM_WIDTH, y=dy + h // 2, width=PLATFORM_WIDTH, height=PLATFORM_HEIGHT))
            ]
            self.labels_lst = [
                self.__get_label(player_names[0], 0, h * 0.25),
                self.__get_label(player_names[1], 0, h * 0.75)
            ]
        elif self.number_players == 3:
            self.players = [
                Player(player_names[0], Platform('left', x=dx, y=dy + h // 2, width=PLATFORM_WIDTH, height=PLATFORM_HEIGHT)),
                Player(player_names[1], Platform('top', x=dx + w // 2, y=dy + h - PLATFORM_WIDTH, width=PLATFORM_HEIGHT, height=PLATFORM_WIDTH)),
                Bot('Bot', Platform('right', x=w + dx - PLATFORM_WIDTH, y=dy + h // 2, width=PLATFORM_WIDTH, height=PLATFORM_HEIGHT)),
                Player(player_names[2], Platform('bottom', x=dx + w // 2, y=dy, width=PLATFORM_HEIGHT, height=PLATFORM_WIDTH))
            ]
            self.labels_lst = [
                self.__get_label(player_names[0], 0, h * 0.2),
                self.__get_label(player_names[1], 0, h * 0.4),
                self.__get_label(player_names[2], 0, h * 0.6),
                self.__get_label('Bot', 0, h * 0.8)
            ]
        elif self.number_players == 4:
            self.players = [
                Player(player_names[0], Platform('left', x=dx, y=dy + h // 2, width=PLATFORM_WIDTH, height=PLATFORM_HEIGHT)),
                Player(player_names[1], Platform('top', x=dx + w // 2, y=dy + h - PLATFORM_WIDTH, width=PLATFORM_HEIGHT, height=PLATFORM_WIDTH)),
                Player(player_names[2], Platform('right', x=w + dx - PLATFORM_WIDTH, y=dy + h // 2, width=PLATFORM_WIDTH,height=PLATFORM_HEIGHT)),
                Player(player_names[3], Platform('bottom', x=dx + w // 2, y=dy, width=PLATFORM_HEIGHT, height=PLATFORM_WIDTH))
            ]
            self.labels_lst = [
                self.__get_label(player_names[0],0,h * 0.2),
                self.__get_label(player_names[1],0,h * 0.4),
                self.__get_label(player_names[2],0,h * 0.6),
                self.__get_label(player_names[3],0,h * 0.8)
            ]

    def update(self,dt):
        for player in self.players:
            if type(player).__name__ == 'Bot':
                player.step(self.ball, dt)
            else:
                player.platform.update(dt)
            player.platform.check_bounds(self.board.width, self.board.height, self.board.x, self.board.y)
        if self.server is None and self.client is None:
            self.ball.update(dt)
            self.__check_wall_collision()
        if self.server:
            self.ball.update(dt)
            self.__check_wall_collision()
            data = dict(
                ball=dict(x=self.ball.x, y=self.ball.y, speed_x=self.ball.speed_x, speed_y=self.ball.speed_y),
                names=[(pl.name,pl.score) for pl in self.players],
                platforms=[(pl.platform.width, pl.platform.height, pl.platform.x, pl.platform.y) for pl in self.players]
            )
            encode_data = json.dumps(data,default=lambda x: x.__dict__).encode('utf-8')
            for conn in self.server.connections:
                self.server.send(conn, encode_data)
                client_data = self.server.get_data(conn)
                if client_data != b'':
                    result_data = json.loads(client_data.decode('utf-8'))
                    player = next(filter(lambda x: x.name == result_data['name'], self.players), None)
                    player.platform.x, player.platform.y = result_data['platform']['x'],result_data['platform']['y']

        elif self.client:
            player = next(filter(lambda x: x.name == self.host_name, self.players), None)
            data = dict(name=self.host_name,platform=dict(x=player.platform.x,y=player.platform.y))
            response = self.client.send(json.dumps(data,default=lambda x: x.__dict__).encode('utf-8'))
            if response != b' ':
                server_data = json.loads(response.decode('utf-8'))
                self.ball.x,self.ball.y = server_data['ball']['x'],server_data['ball']['y']
                self.ball.speed_x,self.ball.speed_y = server_data['ball']['speed_x'],server_data['ball']['speed_y']
                w, h = self.board.width, self.board.height
                for i, pl in enumerate(self.players):
                    if server_data['names'][i][0] != self.host_name:
                        pl.platform.width, pl.platform.height, pl.platform.x, pl.platform.y = tuple(server_data['platforms'][i])
                if len(server_data['names']) == 2:
                    self.labels_lst = [
                        self.__get_label(server_data['names'][0][0], server_data['names'][0][1], h * 0.25),
                        self.__get_label(server_data['names'][1][0], server_data['names'][1][1], h * 0.75)
                    ]
                else:
                    self.labels_lst = [
                        self.__get_label(server_data['names'][0][0], server_data['names'][0][1], h * 0.2),
                        self.__get_label(server_data['names'][1][0], server_data['names'][1][1], h * 0.4),
                        self.__get_label(server_data['names'][2][0], server_data['names'][2][1], h * 0.6),
                        self.__get_label(server_data['names'][3][0], server_data['names'][3][1], h * 0.8)
                    ]



    def start_game(self):
        pyglet.clock.schedule_interval(self.update, 1 / FPS_LIMIT)
        pyglet.app.run()

    def on_draw(self):
        self.clear()
        self.__draw_labels()
        self.__draw_board()

    def conn_to_platform(self, player_name): # set player for control platform
        player = next(filter(lambda x: x.name == player_name,self.players),None)
        if player is not None:
            self.push_handlers(player.platform.key_handler) # connect player to platform

    def __get_label(self,name,score,y,x=10,anchor_x='left',anchor_y='top'):
        return pyglet.text.Label(f'{name} - {score}',
                                        font_name='Times New Roman', font_size=FONT_SIZE, x=x,
                                        y=y, anchor_x=anchor_x, anchor_y=anchor_y)

    def __check_wall_collision(self):
        w, h = self.board.width, self.board.height
        wall = self.ball.fix_bounds(WINDOW_WIDTH, WINDOW_HEIGHT, BOARD_POS_X, BOARD_POS_Y)
        if wall:
            player = next(filter(lambda x:x.platform.pos == wall,self.players),None)
            if player:
                collision = player.platform.check_ball_collision(self.ball)
                if len(self.players) == 4:
                    if wall == 'left' and collision != wall:
                        self.players[0].score += 1
                        self.labels_lst[0] = self.__get_label(self.players[0].name, self.players[0].score, h * 0.2)
                    elif wall == 'top' and collision != wall:
                        self.players[1].score += 1
                        self.labels_lst[1] = self.__get_label(self.players[1].name, self.players[1].score, h * 0.4)
                    elif wall == 'right' and collision != wall:
                        self.players[2].score += 1
                        self.labels_lst[2] = self.__get_label(self.players[2].name, self.players[2].score, h * 0.6)
                    elif wall == 'bottom' and collision != wall:
                        self.players[3].score += 1
                        self.labels_lst[3] = self.__get_label(self.players[3].name, self.players[3].score, h * 0.8)
                elif len(self.players) == 2:
                    if wall == 'left' and collision != wall:
                        self.players[0].score += 1
                        self.labels_lst[0] = self.__get_label(self.players[0].name, self.players[0].score, h * 0.25)
                    elif wall == 'right' and collision != wall:
                        self.players[1].score += 1
                        self.labels_lst[1] = self.__get_label(self.players[1].name, self.players[1].score, h * 0.75)


    def __draw_labels(self):
        for label in self.labels_lst:
            label.draw()

    def __draw_board(self):
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
        self.frames = 20
        self.virtual_ball = Ball(x=0, y=0, radius=BALL_RADIUS)

    def step(self,ball,dt):
        self.virtual_ball = Ball(x=ball.x, y=ball.y, radius=BALL_RADIUS)
        self.virtual_ball.speed_x, self.virtual_ball.speed_y = ball.speed_x, ball.speed_y
        for __ in range(self.frames):
            self.virtual_ball.update(dt)
            self.virtual_ball.fix_bounds(WINDOW_WIDTH, WINDOW_HEIGHT, BOARD_POS_X, BOARD_POS_Y)

        if (self.platform.pos == 'left' and ball.speed_x < 0) or \
                (self.platform.pos == 'right' and ball.speed_x > 0):

            if self.virtual_ball.y > self.platform.y + self.platform.height / 2:
                self.platform.y += self.platform.speed * dt
            if self.virtual_ball.y < self.platform.y + self.platform.height / 2:
                self.platform.y -= self.platform.speed * dt

        elif (self.platform.pos == 'top' and ball.speed_y > 0) or \
                (self.platform.pos == 'bottom' and ball.speed_y < 0):

            if self.virtual_ball.x > self.platform.x + self.platform.width / 2:
                self.platform.x += self.platform.speed * dt
            if self.virtual_ball.x < self.platform.x + self.platform.width / 2:
                self.platform.x -= self.platform.speed * dt


class Ball(pyglet.shapes.Circle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.speed_x, self.speed_y = 0.0, 0.0

    def set_random_speed_direction(self):
        while self.speed_x == 0 or self.speed_y == 0:
            self.speed_x = random.choice([0, 300, -300])
            self.speed_y = random.choice([0, 300, -300])

    def update(self, dt):
        self.x += self.speed_x * dt
        self.y += self.speed_y * dt

    def fix_bounds(self,max_x, max_y, min_x, min_y):
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
    def __init__(self, pos, speed=200.0, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__pos = pos
        self.speed = speed
        self.__key_handler = key.KeyStateHandler()

    @property
    def key_handler(self):
        return self.__key_handler

    @property
    def pos(self):
        return self.__pos

    def check_ball_collision(self,ball):
        if self.__pos == 'bottom' and self.y < ball.y < self.y + self.width and self.x < ball.x < self.x + self.width:
            return self.__pos
        if self.__pos == 'top' and self.y < ball.y + ball.radius < self.y + self.width and self.x < ball.x < self.x + self.width:
            return self.__pos
        if self.__pos == 'left' and self.y < ball.y < self.y + self.height and self.x < ball.x < self.x + self.height:
            return self.__pos
        if self.__pos == 'right' and self.y < ball.y < self.y + self.height and self.x < ball.x + ball.radius < self.x + self.height:
            return self.__pos

    def check_bounds(self, max_x, max_y, min_x, min_y):
        if (self.__pos == 'left' or self.__pos == 'right') and self.y < min_y:
            self.y = 0
        elif (self.__pos == 'left' or self.__pos == 'right') and self.y > max_y - self.height:
            self.y = max_y - self.height
        elif (self.__pos == 'top' or self.__pos == 'bottom') and self.x < min_x:
            self.x = min_x
        elif (self.__pos == 'top' or self.__pos == 'bottom') and self.x > max_x + self.width:
            self.x = max_x + self.width


    def update(self, dt):
        if self.__pos == 'left' and self.__key_handler[key.LEFT]:
            self.y += self.speed * dt
        elif self.__pos == 'left' and self.__key_handler[key.RIGHT]:
            self.y -= self.speed * dt

        elif self.__pos == 'right' and self.__key_handler[key.LEFT]:
            self.y -= self.speed * dt
        elif self.__pos == 'right' and self.__key_handler[key.RIGHT]:
            self.y += self.speed * dt

        elif self.__pos == 'top' and self.__key_handler[key.LEFT]:
            self.x -= self.speed * dt
        elif self.__pos == 'top' and self.__key_handler[key.RIGHT]:
            self.x += self.speed * dt

        elif self.__pos == 'bottom' and self.__key_handler[key.LEFT]:
            self.x -= self.speed * dt
        elif self.__pos == 'bottom' and self.__key_handler[key.RIGHT]:
            self.x += self.speed * dt
