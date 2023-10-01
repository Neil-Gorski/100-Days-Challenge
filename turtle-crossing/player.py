from turtle import Turtle
STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 10
FINISH_LINE_Y = 280


class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.penup()
        self.color("black")
        self.goto(STARTING_POSITION)
        self.seth(90)

    def move(self):
        print("Move")
        self.forward(MOVE_DISTANCE)

    def endline(self):
        if self.ycor() >= 280:
            return True

    def restart(self):
        self.goto(STARTING_POSITION)
