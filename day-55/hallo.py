from flask import Flask

app = Flask(__name__)


def make_bold(funtion):
    def wrapper_funtion():
        text = funtion()
        return f"<b>{text}</b>"
    return wrapper_funtion

def make_emphasis(funtion):
    def wrapper_funtion():
        text = funtion()
        return f"<em>{text}</em>"
    return wrapper_funtion


def make_underline(funtion):
    def wrapper_funtion():
        text = funtion()
        return f"<u>{text}</u>"
    return wrapper_funtion


@app.route("/")
def hello_world():
    return "<p>Hello, welt! was ist los</p>"


@app.route("/bye")
@make_bold
@make_underline
@make_emphasis
def bye():
    return "Bye!"


if __name__ == "__main__":
    app.run(debug=True)
