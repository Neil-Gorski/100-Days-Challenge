from turtle import Turtle
import time


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.up()
        self.turtlesize(stretch_len=1, stretch_wid=1)
        self.direction = [5, 5]
        self.x_movement = 10
        self.y_movement = 10
        self.restart_timer = 24

    def move(self):
        if self.restart_timer:
            self.restart_timer -= 1
        else:
            new_x = self.xcor() + self.x_movement
            new_y = self.ycor() + self.y_movement
            self.goto(new_x, new_y)

    def bounce_y(self):
        if self.ycor() > 280 or self.ycor() < -280:
            self.y_movement *= -1

    def bounce_x(self, paddle_l, paddle_r):
        if self.xcor() > 330 and self.distance(paddle_r) < 50 or self.xcor() < -330 and self.distance(paddle_l) < 50:
            self.x_movement *= -1

    def point(self):
        if self.xcor() > 420 or self.xcor() < -420:
            self.goto(0, 0)
            self.x_movement *= -1
            self.restart_timer = 30
            return True
