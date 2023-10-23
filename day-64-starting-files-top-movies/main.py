import os
from flask import Flask, render_template, redirect, url_for, request, session
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField
from wtforms.validators import DataRequired, NumberRange
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

MOVIE_DB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
MOVIE_DB_API_KEY = "5e6542c14afd44060154d78b613a49a6"
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer)
    review = db.Column(db.String)
    img_url = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return f"<Movie: {self.title}>"

    @property
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__tabel__.columns}


class RatingForm(FlaskForm):
    rating = DecimalField("Your Rating Out of 10 e.g. 6.4",
                          places=1,
                          validators=[DataRequired(),
                                      NumberRange(min=1, max=10)])
    review = StringField("Your Review", validators=[DataRequired()])
    submit = SubmitField("Done")


class AddForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    result = db.session.execute(db.select(Movie).order_by(Movie.rating))
    all_movies = result.scalars().all()  # convert ScalarResult to Python List

    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()

    return render_template("index.html", movies=all_movies)


@app.route("/edit/<int:id>", methods=['POST', 'GET'])
def edit(id):
    form = RatingForm()
    movie_to_update = db.get_or_404(Movie, id)
    if form.validate_on_submit():
        new_data = request.form
        movie_to_update.rating = new_data['rating']
        movie_to_update.review = new_data['review']
        db.session.commit()
        return redirect("/")
    return render_template("edit.html", form=form, id=id)


@app.route("/delete/<int:id>", methods=['POST', 'GET'])
def delete(id):
    movie_to_delete = db.get_or_404(Movie, id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect("/")


@app.route("/add", methods=['POST', 'GET'])
def add_movie():
    form = AddForm()
    if form.validate_on_submit():
        movie_title = form.title.data
        response = requests.get(MOVIE_DB_SEARCH_URL, params={
                                "api_key": MOVIE_DB_API_KEY, "query": movie_title}).json()["results"]
        print(response)
        data = response
        return render_template("select.html", options=data)

    return render_template("add.html", form=form)


@app.route("/select", methods=["GET", "POST"])
def select():
    movie_list = session["movie_list"]
    return render_template("select.html", movie_list=movie_list)


@app.route("/find")
def find_movie():
    movie_api_id = request.args.get("id")
    if movie_api_id:
        movie_api_url = f"https://api.themoviedb.org/3/movie/{movie_api_id}"
        response = requests.get(movie_api_url, params={
                                "api_key": MOVIE_DB_API_KEY})
        data = response.json()
        new_movie = Movie(
            title=data["title"],
            year=data["release_date"],
            img_url=f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}",
            description=data["overview"],
            rating=1,
            ranking=2,
            review="Woohoo"



        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)
