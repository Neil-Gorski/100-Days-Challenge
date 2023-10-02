from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def home():
    blogs = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()
    print(blogs)
    return render_template("index.html", blogs=blogs)


@app.route("/post/<id_num>")
def get_blog(id_num):
    blogs = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

    # blog = next((blog for blog in blogs if blog['id'] == id_num), None)
    blog_content = None
    for blog in blogs:
        if int(blog["id"]) == int(id_num):
            blog_content = blog

    print(blog_content)
    return render_template("post.html", blog=blog_content)


if __name__ == "__main__":
    app.run(debug=True)
