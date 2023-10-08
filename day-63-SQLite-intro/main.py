from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__ )

db_path = os.path.join(os.path.dirname(__file__), "new-books-collection.db")
db_uri = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
db = SQLAlchemy(app)

class  Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    author = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'

with app.app_context():
    db.create_all()



with app.app_context():
    new_book = Books(id=1, title="Herry Potter", author="J.K. Rowling", rating=9.3)
    db.session.add(new_book)
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