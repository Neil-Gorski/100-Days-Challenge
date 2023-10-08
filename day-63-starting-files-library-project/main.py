from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, URL, InputRequired, NumberRange

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
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


all_books = []

class BookForm(FlaskForm):
    title = StringField("Book Title", validators=[(DataRequired())])
    author = StringField("Book Author", validators=[(DataRequired())])
    rating = IntegerField("Book Rating", validators=[InputRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField('Submit')



@app.route('/')
def home():
    return render_template('index.html', book_list=all_books)


@app.route("/add", methods=['POST', 'GET'])
def add():
    form = BookForm()
    form_input = {}
    if form.validate_on_submit():
        for element in form:
            form_input[element.name] = element.data
        form_input.pop("submit")
        form_input.pop("csrf_token")    
        all_books.append(form_input)
        print(all_books)
        return redirect("/")
    return render_template('add.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
