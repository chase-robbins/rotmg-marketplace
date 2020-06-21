from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import src
from jinja2 import Environment, PackageLoader, select_autoescape

app = Flask(__name__)
app.secret_key = "978u3h4tg897hgbu4rh49p83gf7hq9p34hgq93p4u"
app.permanent_session_lifetime = timedelta(days=5)

db = SQLAlchemy(app)

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        search = request.form["item"]
        if search != "":
            searchID = src.getItemID(search)
            offersReturn = src.searchOffers(searchID)
        if "UID" in session:
            itemIds = src.getAllItems()
            list = src.listItemsFromUID(session["UID"]).fetchall()
            if search == "":
                offersReturn = src.listTheOffers()
            return render_template("home.html", offers = offersReturn, items = list, invUsed = len(list), itemIds = itemIds, capacity = src.getCapacity(session["UID"]))
        else:
            return render_template("home.html", offers = offersReturn)
    else:
        offersReturn = src.listTheOffers()
        if "UID" in session:
            itemIds = src.getAllItems()
            list = src.listItemsFromUID(session["UID"]).fetchall()
            return render_template("home.html", offers = offersReturn, items = list, invUsed = len(list), itemIds = itemIds, capacity = src.getCapacity(session["UID"]))
        else:
            return render_template("home.html", offers = offersReturn)

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
    if "UID" in session:
        activeOffers = src.getActiveOffers(session["UID"])
        ign = src.getIGN(session["UID"])
        list = src.getItemsForInventory(session["UID"])
        return render_template("user.html", items = list, ign = ign, activeOffers = activeOffers, invUsed = src.getInvUsed(session["UID"]), capacity = src.getCapacity(session["UID"]))
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
        src.testDeposit(itemid, session["UID"])
        flash("Deposit successful.")
        return render_template("deposit.html")
    else:
        return render_template("deposit.html")

@app.route("/offer", methods=["POST", "GET"])
def offer():
    if request.method == "POST":
        src.createTestOffer(seeking,seekingq,providing,providingq, session["UID"])
        flash("Offer Posted.")
        return render_template("offer.html")
    else:
        if "UID" in session:
            list = src.listItemsFromUID(session["UID"])
            itemIds = src.getAllItems()
            return render_template("offer.html", items = list, itemIds = itemIds)
        else:
            return render_template("offer.html")

@app.route("/offer/<offerid>", methods=["POST", "GET"])
def offerid(offerid):
    buying = src.getOfferData(offerid)[0][0]
    selling = src.getOfferData(offerid)[1][0]
    return render_template("offerid.html", buying = buying, selling = selling, id = offerid)

@app.route("/postoffer", methods=['POST'])
def postOffer():
        buying = []
        selling = []
        data = request.get_json(force=True)
        for item in data:
            if item['value'] == '' or int(item['value']) < 1:
                return jsonify({'message': 'Quantity can not be zero.'})
            item['name'] = item['name'].replace('buying-quantity-', 'b-').replace('selling-quantity-', 's-')
            #1 = buy, 2 = sell
            if item['name'][:2] == 'b-':
                buying.append(str(item['value']) + "x" + src.getItemID(item['name'][2:]))
            else:
                selling.append(str(item['value']) + "x" + src.getItemID(item['name'][2:]))

        id = session['UID']
        return jsonify({'message': src.createOffer(id, buying, selling)})

@app.route("/withdraw", methods=['POST'])
def withdraw(itemID):
        src.withdraw(itemID, session["UID"])

@app.route("/offeraction", methods=["POST"])
def offerAction():
    if request.form['submit_button'] == 'accept':
        flash(src.acceptOffer(request.form['offerID'], session["UID"]))
    if request.form['submit_button'] == 'delete':
        flash(src.deleteOffer(request.form['offerID'], session["UID"]))
    return redirect(url_for("home"))

#CUSTOM FILTERS:
app.jinja_env.filters['getIGN'] = src.getIGN
app.jinja_env.filters['getItemName'] = src.getItemName
app.jinja_env.filters['getItemImage'] = src.getItemImage
app.jinja_env.filters['str'] = str
app.jinja_env.filters['parseOffer'] = src.parseOffer
app.jinja_env.filters['len'] = len
app.jinja_env.filters['getOfferData'] = src.getOfferData
app.jinja_env.filters['log'] = print
app.jinja_env.filters['getOfferOwner'] = src.getOfferOwner
app.jinja_env.filters['getOfferOwnerId'] = src.getOfferOwnerId



if __name__ == "__main__":
    app.run(debug = True)
