from turtle import Screen
from paddle import Paddle
from ball import Ball
import time

FPS = 1/24

screen = Screen()
screen.title("Pong")
screen.bgcolor("black")
screen.setup(height=600, width=800)
screen.tracer(0)

paddle_l = Paddle((-350, 0))
paddle_r = Paddle((350, 0))
ball = Ball()

# Key listener
screen.listen()
screen.onkey(paddle_r.go_up, "Up")
screen.onkey(paddle_r.go_down, "Down")
screen.onkey(paddle_l.go_up, "w")
screen.onkey(paddle_l.go_down, "s")

game_is_on = True

while game_is_on:
    time.sleep(FPS)
    ball.move()
    ball.bounce_y()
    ball.bounce_x(paddle_l, paddle_r)
    ball.point()
    screen.update()


screen.exitonclick()
