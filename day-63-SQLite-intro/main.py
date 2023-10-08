from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

db_path = os.path.join(os.path.dirname(__file__), "new-books-collection.db")
db_uri = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=False, nullable=False)
    author = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'


with app.app_context():
    db.create_all()


# Read all the books
with app.app_context():
    result = db.session.execute(db.select(Book).order_by("id"))
    all_books = result.scalars()

# Read A Particular Record By Query
with app.app_context():
    book = db.session.execute(db.select(Book).where(
        Book.title == "Herry Potter")).scalar()
    print(book.id)

# Update A Particular Record PRIMARY KEY
with app.app_context():
    book_to_update = db.session.execute(
        db.select(Book).where(Book.id == 2)).scalar()
    book_to_update.title = "Harry Potter and the Chamber of Secrets"
    db.session.commit()

# Delete A Particular Record By PRIMARY KEY
book_id = 4
with app.app_context():
    book_to_delete = db.session.execute(
        db.select(Book).where(Book.id == book_id)).scalar()
    db.session.delete(book_to_delete)
    db.session.commit()


# def create_connection(db_file):
#     """ create a database connection to a SQLite database """
#     conn = None
#     try:
#         conn = sqlite3.connect(db_file)
#         cursor = conn.cursor()
#         # cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title VARCHAR(250) NOT NULL UNIQUE, author VARCHAR(250) NOT NULL, rating FLOAT NOT NULL)")
#         cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J.K. Rowling', '4')")
#         conn.commit()
#         print(sqlite3.version)
#     except Error as e:
#         print(e)
#     finally:
#         if conn:
#             conn.close()


# if __name__ == '__main__':
#     create_connection(r"C:\Users\Neil\PycharmProjects\100-Days-Challenge\day-63-SQLite-intro\books-collection.db")
