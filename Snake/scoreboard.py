from turtle import Turtle
ALIGNMENT = "center"
FONT = ("Aral", 14, "normal")
GAME_OVER_FONT = ("Aral", 20, "bold")

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = -1
        self.color("red")
        self.up()
        self.hideturtle()
        self.setpos(0, 270)
        self.update_score()

    def game_over(self):
        self.goto(0, 0)
        self.write(f"Game Over", False, align=ALIGNMENT, font=GAME_OVER_FONT)

    def update_score(self):
        self.clear()
        self.score += 1
        self.write(f"Score: {self.score}", False, align=ALIGNMENT, font=FONT)
