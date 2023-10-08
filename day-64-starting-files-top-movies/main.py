import os
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests


'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
db_path = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'movies.db')}"
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config["SQLALCHEMY_DATABASE_URI"] = db_path
Bootstrap5(app)
db = SQLAlchemy(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return f"<Movie: {self.title}>"

    @property
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__tabel__.columns}


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    all_movies = None
    with app.app_context():
        result = db.session.execute(db.select(Movie).order_by(Movie.title))
        all_movies = result.scalars().all()
    return render_template("index.html", movies=all_movies)


if __name__ == '__main__':
    app.run(debug=True)
