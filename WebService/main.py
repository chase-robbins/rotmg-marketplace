from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import src

app = Flask(__name__)
app.secret_key = "978u3h4tg897hgbu4rh49p83gf7hq9p34hgq93p4u"
app.permanent_session_lifetime = timedelta(days=5)

db = SQLAlchemy(app)

@app.route("/")
def home():
    itemsReturn = src.listThem()
    return render_template("home.html", items = itemsReturn)

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["email"]
        session["user"] = user
        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        session.permanent = True
        email = request.form["email"]
        password = request.form["password"]
        ign = request.form["ign"]
        session["email"] = email
        session["password"] = password
        session["ign"] = ign
        src.createAcc(ign, email, password)
        return redirect(url_for("home"))
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("register.html")

@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]
        return render_template("user.html")
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.clear()
    flash("You have successfully logged out.", "info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug = True)
