from turtle import Turtle
from random import randint

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10


class CarManager(Turtle):
    def __init__(self, lvl):
        super().__init__()
        self.shape("square")
        self.penup()
        self.color(COLORS[randint(0, 5)])
        self.shapesize(1, 2)
        self.goto(320, randint(-240, 250))
        self.seth(180)
        self.lvl = lvl

    def move(self):
        self.forward(MOVE_INCREMENT * self.lvl)

