from turtle import Screen
from snake import Snake
from food import Food
from scoreboard import Scoreboard
import time


FPS = 20
SLEEP_TIME = 1 / FPS


def quit_game():
    global game_is_on
    game_is_on = False


screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("My Snake Game")
screen.tracer(0)

snake = Snake()
food = Food()
scoreb = Scoreboard()

screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")
screen.onkey(quit_game, "space")

screen.update()

game_is_on = True

while game_is_on:
    screen.update()
    time.sleep(SLEEP_TIME)
    snake.move()

    # Detect collision with food.
    if snake.head.distance(food) < 11:
        food.refresh()
        snake.extend()
        scoreb.update_score()

    # Detect collision with wall.
    if snake.head.xcor() > 280 or snake.head.xcor() < -300 or snake.head.ycor() > 300 or snake.head.ycor() < -280:
        game_is_on = False

    # Detect collision with tail
    for segment in snake.segments[1:]:
        if snake.head.distance(segment) < 10:
            game_is_on = False
            scoreb.game_over()

scoreb.game_over()
screen.exitonclick()
