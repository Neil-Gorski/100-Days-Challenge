import datetime
from flask import Flask, render_template
import random
import requests

app = Flask(__name__)

@app.route("/")
def home():
    rand = random.randint(0,100)
    year = datetime.datetime.now().year
    return render_template("index.html", num=rand, current_year=year)


@app.route("/guess/<name>")
def guess(name):
    r_gender = requests.get(f"https://api.genderize.io?name={name}").json()
    r_age = requests.get(f"https://api.agify.io?name={name}").json()
    name = name.title()
    return render_template("guess.html", age=r_age["age"], gender=r_gender["gender"], name=name)


@app.route("/blog")
def blog():
    all_posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()
    return render_template("blog.html", posts=all_posts)

if __name__ == "__main__":
    app.run(debug=True)
