from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'

# CONNECT TO DB
db_path = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'instance/users.db')}"
app.config['SQLALCHEMY_DATABASE_URI'] = db_path
db = SQLAlchemy()
db.init_app(app)

# CREATE LOGIN MANAGER
login_manager = LoginManager()
login_manager.init_app(app)

# User Loader


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

# CREATE TABLE IN DB


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=['POST', "GET"])
def register():
    if request.form:
        user = request.form.to_dict()

        new_user = User(
            email=user["email"],
            password=generate_password_hash(user["password"], salt_length=8),
            name=user["name"]
        )
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return render_template("secrets.html", user=user)

    return render_template("register.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get("password")

        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()

        if check_password_hash(pwhash=user.password, password=password):
            login_user(user)
            return redirect(url_for("secrets"))

    return render_template("login.html")


@app.route('/secrets')
@login_required
def secrets():
    print(current_user.name)
    return render_template("secrets.html", name=current_user.name)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route('/download')
@login_required
def download():
    return send_from_directory('static', "files/cheat_sheet.pdf")


if __name__ == "__main__":
    app.run(debug=True)
