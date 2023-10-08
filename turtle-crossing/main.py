import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard
import random


screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)
level = 1
car_list = []

player = Player()
crash = False
endline = False
# key
screen.listen()
screen.onkeypress(player.move, "w")

game_is_on = True
while game_is_on:
    time.sleep(0.1)
    if not crash or not endline:
        if random.random() > 0.9:
            car_list.append(CarManager(level))
        for car in car_list:
            car.move()
            if player.distance(car) < 20:
                crash = True
        if player.endline():
            endline = True

    if endline:
        player.restart()
        level += 1
        print("End Line")
        endline = False

    screen.update()
