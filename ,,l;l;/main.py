from flask import Flask, render_template, request, session, redirect

from user import createusertable, User
from post import createposttable, Post

import secrets

createposttable()
createusertable()

app = Flask("main")
app.secret_key = secrets.token_hex(32)

@app.route("/")
def indexpage():
    posts = Post.getallposts()
    username = session.get("username", None)
    user = None
    if username:
        user = User.getbyusername(username)                
    return render_template("index.html", posts=posts, user=user)

@app.route("/registration", methods=["POST","GET"])
def registerpage():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form.get("username").lower()
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        user=User.getbyusername(username)
        if user:
            return render_template(
                "register.html", error="такойпользовательужеесть"
            )
        if password != confirm_password:
            return render_template(
                "register.html", error='паролиразные'

            )
        User.create(username, password)
        session["username"] = username
        return redirect("/")

@app.route("/login")
def login_page():
    return


@app.route("/profile")
def profile_page():
    return

app.run(host="0.0.0.0", port=8080)