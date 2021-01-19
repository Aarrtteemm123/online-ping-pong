import pyglet

class Player:
    def __init__(self,name,controller,score=0):
        self.name = name
        self.score = score
        self.controller = controller


class Ball(pyglet.shapes.Circle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.speed_x, self.speed_y = 0.0, 0.0

    def update(self,dt):
        self.x += self.speed_x * dt
        self.y += self.speed_y * dt

    def check_bounds(self,max_x, max_y, min_x, min_y):
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
    def __init__(self, speed = 20.0, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.speed = speed
