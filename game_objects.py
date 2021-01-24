import pyglet
from pyglet import shapes
from pyglet.window import key


class Game:
    def __init__(self, number_players):
        self.number_players = number_players
        self.board = shapes.Rectangle(x=200, y=0, width=700, height=600, color=(0, 0, 255))
        dx, dy = self.board.x, self.board.y
        w, h = self.board.width, self.board.height
        self.ball = Ball(x=dx+w//2, y=dy+h//2, radius=10, color=(255, 0, 0))
        if number_players == 1:
            self.players = [Player('Player', Platform('left',x=dx, y=dy + h // 2, width=10, height=200)),
                            Bot('Bot', Platform('right',x=w + dx - 10, y=dy + h // 2, width=10, height=200))]
        elif number_players == 2:
            self.players = [Player('Player 1', Platform('left',x=dx, y=dy + h // 2, width=10, height=200)),
                            Player('Player 2', Platform('right',x=w + dx - 10, y=dy + h // 2, width=10, height=200))]
        elif number_players == 3:
            self.players = [Player('Player 1', Platform('left',x=dx, y=dy + h // 2, width=10, height=200)),
                            Player('Player 2', Platform('top',x=dx + w // 2, y=dy + h - 10, width=200, height=10)),
                            Bot('Bot', Platform('right',x=w + dx - 10, y=dy + h // 2, width=10, height=200)),
                            Player('Player 3', Platform('bottom',x=dx + w // 2, y=dy, width=200, height=10))]
        elif number_players == 4:
            self.players = [Player('Player 1', Platform('left',x=dx, y=dy + h // 2, width=10, height=200)),
                            Player('Player 2', Platform('top',x=dx + w // 2, y=dy + h - 10, width=200, height=10)),
                            Player('Player 3', Platform('right',x=w + dx - 10, y=dy + h // 2, width=10, height=200)),
                            Player('Player 4', Platform('bottom',x=dx + w // 2, y=dy, width=200, height=10))]
        self.labels_lst = []

    def draw_labels(self):
        pass

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
        elif self.x > max_x - self.radius:
            self.x = max_x - self.radius
            self.speed_x *= -1
        if self.y < min_y + self.radius:
            self.y = min_y + self.radius
            self.speed_y *= -1
        elif self.y > max_y - self.radius:
            self.y = max_y - self.radius
            self.speed_y *= -1


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