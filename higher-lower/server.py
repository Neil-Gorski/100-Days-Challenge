from flask import Flask
from random import randint


app = Flask(__name__)

secret_num = randint(0, 9)


@app.route("/")
def home():
    return (f"<h1>Guess a number between 0 and 9</h1>"
            "<img src='https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif'>")


@app.route("/<int:number>")
def guess_number(number):
    if number < secret_num:
        return (f"<h1 style='color:purple;'>The number is too low</h1>"
                "<img src='https://media.giphy.com/media/oJWx7MtpR2qdi/giphy.gif'>")
    elif number > secret_num:
        return (f"<h1 style='color:red;'>The number is too high</h1>"
                "<img src='https://media.giphy.com/media/3o8doVAxrMjXbIHaU0/giphy.gif'>")
    else:
        return (f"<h1 style='color:black;'>You find me!</h1>"
                "<img src='https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif'>")


if __name__ == "__main__":
    app.run(debug=True)
