from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route("/")
def home():
    blog_list = requests.get(
        "https://api.npoint.io/eb6cd8a5d783f501ee7d").json()
    return render_template("index.html", blog_list=blog_list)


@app.route("/post/<id_num>")
def get_blog(id_num):
    blogs = requests.get("https://api.npoint.io/eb6cd8a5d783f501ee7d").json()

    # blog = next((blog for blog in blogs if blog['id'] == id_num), None)
    blog_content = None
    for blog in blogs:
        if int(blog["id"]) == int(id_num):
            blog_content = blog

    print(blog_content)
    return render_template("post.html", blog=blog_content)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=['POST', 'GET'])
def contact():
    if request.method == "POST":
        data = request.form
        print(data["name"])
        print(data["email"])
        print(data["phone"])
        print(data["message"])
        return render_template("contact.html", success=True)
    return render_template("contact.html")


@app.route("/from-entry")
def receive_data():
    return "Successfully sent your message"


if __name__ == "__main__":
    app.run(debug=True)
