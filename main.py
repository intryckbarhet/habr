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
        # Добавляем информацию о лайках для каждого поста
        for post in posts:
            post.is_liked = Post.is_liked_by_user(user.id, post.id)
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

@app.route("/logout")
def logoutpage():
    del session["username"]
    return redirect('/login')

@app.route("/login", methods=['POST', 'GET'])
def loginpage():
    if request.method == 'GET':
        return render_template("login.html")
    if request.method == 'POST':
        username = request.form.get("username").lower()
        password = request.form.get("password")
        
        user = User.getbyusername(username)
        if not user:
            return render_template('login.html', error='нет юзера')
        if user.password == password:
            session["username"] = username
            return redirect("/")
        else:
            return render_template('login.html', error='другой пароль')

@app.route("/profile", methods=['POST', 'GET'])
def profilepage():
    username = session.get("username")
    user = User.getbyusername(username)
    if not username:    
        return redirect("/login")
    
    if request.method == 'GET':
        posts = Post.getallpostsbyauthor(user.id)
        # Добавляем информацию о лайках для каждого поста
        for post in posts:
            post.is_liked = Post.is_liked_by_user(user.id, post.id)
        return render_template('profile.html', user=user, posts=posts)
    
@app.route("/like/<int:post_id>", methods=["POST"])
def likepost(post_id):
    username = session.get("username")
    if not username:
        return redirect("/login")
    user = User.getbyusername(username)
    Post.togglelike(user.id, post_id)
    return redirect("/")

app.run(host="0.0.0.0", port=8080, debug=True)