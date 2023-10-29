from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
import random
import urllib.parse


'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''
db_path = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'instance/cafes.db')}"
app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = db_path
db = SQLAlchemy()
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        """
        Converts the object to a dictionary representation.

        Returns:
            dict: A dictionary representation of the object, where the keys are the column names of the table and the values are the corresponding attribute values of the object.
        """
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()


def str_to_bool(v):
    if v in ['True', ' true', 'T', 't', 'Yes', 'yes', 'y', '1']:
        return True
    else:
        return False


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random")
def get_random_cafe():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    random_cafe = random.choice(all_cafes)
    # Simply convert the random_cafe data record to a dictionary of key-value pairs.
    return jsonify(cafe=random_cafe.to_dict())


@app.route('/all')
def get_all_cafes():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    all_cafes_dict = [cafe.to_dict() for cafe in all_cafes]
    return jsonify(cafes=all_cafes_dict)


@app.route('/search')
def search_cafes_location():
    location = request.args.get("loc")
    cafes = Cafe.query.filter_by(location=location).all()
    if len(cafes) == 0:
        error = {
            "error": {
                "Not Found": "Sorry, we don't have a cafe at that location"
            }
        }
        return jsonify(error)
    cafes = [cafe.to_dict() for cafe in cafes]
    return jsonify(cafes=cafes)
# HTTP POST - Create Record


@app.route("/add", methods=["POST", "GET"])
def add_cafe():
    if request.method == "POST":
        new_cafe = Cafe(
            name=request.form.get("name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("loc"),
            has_sockets=str_to_bool(request.form.get("has_sockets")),
            has_toilet=str_to_bool(request.form.get("has_toilet")),
            has_wifi=str_to_bool(request.form.get("has_wifi")),
            can_take_calls=str_to_bool(request.form.get("can_take_calls")),
            seats=request.form.get("seats"),
            coffee_price=urllib.parse.unquote(
                request.form.get("coffee_price")),
        )
        print(urllib.parse.unquote(request.form.get("coffee_price")))
        db.session.add(new_cafe)
        db.session.commit()
        return jsonify(response={"success": "Successfully added the new Cafe."})
    return jsonify(error={"Not added": "Sorry, some data is missing."})


# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    new_cafe_price = urllib.parse.unquote(request.form.get("cafe_price"))
    cafe = db.get_or_404(Cafe, cafe_id)
    if cafe:
        cafe.coffee_price = new_cafe_price
        db.session.commit()
        return jsonify(response={"success": "Successfully added the new Cafe."})
    else:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."})

# HTTP DELETE - Delete Record


@app.route("/report-closed/<cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    cafe = db.get_or_404(Cafe, cafe_id)
    if cafe:
        if request.args.get("api-key") == "TopSecretAPIKey":
            cafe = db.get_or_404(Cafe, cafe_id)
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted Cafe."})
        else:
            return jsonify(error={"error": "Sorry, that's not allowed. Make sure you have the correct api_key."})
    else:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."})


if __name__ == '__main__':
    app.run(debug=True)
