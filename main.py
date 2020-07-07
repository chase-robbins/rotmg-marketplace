from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import src
from jinja2 import Environment, PackageLoader, select_autoescape

app = Flask(__name__)
app.secret_key = "978u3h4tg897hgbu4rh49p83gf7hq9p34hgq93p4u"
app.permanent_session_lifetime = timedelta(days=5)

db = SQLAlchemy(app)

@app.route("/")
def home():
    offersReturn = src.listTheOffers()
    return render_template("home.html", offers = offersReturn, Source = src)

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if src.tryLogin(email, password):
            session["UID"] = src.getUID(email)
            session.permanent = True
            return redirect(url_for("user"))
        else:
            return redirect(url_for("login"))
    else:
        if "UID" in session:
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        ign = request.form["ign"]
        if src.createAcc(ign, email, password) == 1:
            session["UID"] = src.getUID(email)
            return redirect(url_for("home"))
        else:
            return redirect(url_for("register"))
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("register.html")

@app.route("/user", methods=["POST", "GET"])
def user():
    if request.method == "POST":
        str = request.form["search"]
        list = src.invSearch(str, session["UID"])
        return render_template("user.html", items = list)
    else:
        if "UID" in session:
            ign = src.getIGN(session["UID"])
            list = src.listItemsFromUID(session["UID"])
            return render_template("user.html", items = list, ign = ign)
        else:
            return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.clear()
    flash("You have successfully logged out.", "info")
    return redirect(url_for("login"))

@app.route("/deposit", methods=["POST", "GET"])
def deposit():
    if request.method == "POST":
        itemid = request.form["id"]
        name = request.form["name"]
        src.testDeposit(itemid, name, session["UID"])
        flash("Deposit successful.")
        return render_template("deposit.html")
    else:
        return render_template("deposit.html")

@app.route("/offer", methods=["POST", "GET"])
def offer():
    if request.method == "POST":
        seeking = request.form["seeking"]
        seekingq = request.form["seekingq"]
        providing = request.form["providing"]
        providingq = request.form["providingq"]
        src.createTestOffer(seeking,seekingq,providing,providingq, session["UID"])
        flash("Offer Posted.")
        return render_template("offer.html")
    else:
        return render_template("offer.html")

#CUSTOM FILTERS:
app.jinja_env.filters['getIGN'] = src.getIGN

if __name__ == "__main__":
    app.run(debug = True)
