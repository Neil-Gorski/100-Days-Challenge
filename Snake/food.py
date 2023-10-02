from turtle import Turtle
import random


class Food(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.up()
        self.shapesize(0.5, 0.5)
        self.color("orange")
        self.speed("fastest")
        self.refresh()


    def refresh(self):
        random_x = random.randint(-28, 28)
        random_x = random_x if random_x % 2 == 0 else random_x - 1
        random_x = random_x * 10
        random_y = random.randint(-28, 28)
        random_y = random_y if random_y % 2 == 0 else random_y - 1
        random_y = random_y * 10
        self.goto(random_x, random_y)