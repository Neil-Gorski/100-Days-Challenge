import os
from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, URL, InputRequired, NumberRange
from flask_sqlalchemy import SQLAlchemy

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
db_path = os.path.join(os.path.dirname(__file__), "new-books-collection.db")
db_uri = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
db = SQLAlchemy(app)

all_books = []


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    author = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Book ID:{self.id} | {self.title} | {self.author} | {self.rating}>"

    @property
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__tabel__.columns}


with app.app_context():
    db.create_all()


def get_all_books():
    with app.app_context():
        result = db.session.execute(db.select(Book).order_by(Book.title))
        all_books = result.scalars().all()
        return all_books


def add_new_book(title, author, rating):
    with app.app_context():
        new_book = Book(title=title, author=author, rating=rating)
        db.session.add(new_book)
        db.session.commit()


class BookForm(FlaskForm):
    title = StringField("Book Title", validators=[(DataRequired())])
    author = StringField("Book Author", validators=[(DataRequired())])
    rating = FloatField("Book Rating", validators=[
                        InputRequired(), NumberRange(min=1, max=10)])
    submit = SubmitField('Submit')


@app.route('/')
def home():
    print(get_all_books())

    return render_template('index.html', book_list=get_all_books())


@app.route("/add", methods=['POST', 'GET'])
def add():
    form = BookForm()
    new_book = {}
    if form.validate_on_submit():

        for element in form:
            new_book[element.name] = element.data
        new_book.pop("submit")
        new_book.pop("csrf_token")
        add_new_book(
            title=new_book["title"], author=new_book["author"], rating=new_book["rating"])
        all_books.append(new_book)
        print(all_books)
        return redirect("/")
    return render_template('add.html', form=form)


@app.route('/edit/<id>', methods=['POST', 'GET'])
def edit(id):
    book_to_update = db.get_or_404(Book, id)
    if request.method == "POST":
        new_rating = request.form
        book_to_update.rating = new_rating['rating']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', id=id, title=book_to_update.title, rating=book_to_update.rating)


@app.route("/delete/<id>", methods=["POST", "GET"])
def delete(id):
    # DELETE A RECORD BY ID
    book_to_delete = db.get_or_404(Book, id)
    # Alternative way to select the book to delete.
    # book_to_delete = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
