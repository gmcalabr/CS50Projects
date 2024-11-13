import os
import json
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///familytree.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show family tree"""

    # grab alert if redirected here from /buy successful purchase
    #    alert = request.args.get("alert")

    # get userid from users db
    userid = session.get("user_id")

    # get info from familytree.db and set it equal to stocks
    people = db.execute("""SELECT people.id, people.first, people.middle, people.last, people.birthdate, people.birthcity, people.deathdate, people.deathcity, people.occupation1, lineage.mother, lineage.father
                        FROM people JOIN lineage ON people.id = lineage.id WHERE userid = ? ORDER BY people.id;""", userid)

    return render_template("index.html", people=people)


@app.route("/editperson", methods=["GET", "POST"])
@login_required
def editperson():

    # if POST
    if request.method == "POST":

        userid = session.get("user_id")
        editPersonId = request.form.get('editPersonId')
        editPersonUserId = db.execute("SELECT userid FROM people WHERE id = ?", editPersonId)[0]['userid']

        if editPersonUserId != userid:
            return apology("Stop trying to tamper with things!", 403)
        if not request.form.get("first"):
            return apology("must provide a first name", 400)
        if not request.form.get("last"):
            return apology("must provide a last name", 400)

        # collect variables
        first = request.form.get("first")
        last = request.form.get("last")
        middle = request.form.get("middle")
        birthdate = request.form.get("birthdate")
        birthcity = request.form.get("birthcity")
        birthcountry = request.form.get("birthcountry")
        deathdate = request.form.get("deathdate")
        deathcity = request.form.get("deathcity")
        deathcountry = request.form.get("deathcountry")
        occupation1 = request.form.get("occupation1")
        occupation2 = request.form.get("occupation2")
        occupation3 = request.form.get("occupation3")


        # insert data into database - userid, symbol, shares, price (unique index automatic)
        db.execute("""UPDATE people SET last = ?, first = ?, middle = ?, birthdate = ?, birthcity = ?, birthcountry = ?, deathdate = ?, deathcity = ?, deathcountry = ?, occupation1 = ?, occupation2 = ?, occupation3 = ? WHERE id = ?""", last, first, middle, birthdate, birthcity, birthcountry, deathdate, deathcity, deathcountry, occupation1, occupation2, occupation3, editPersonId)

        # send alert to index.html
        alert = 'Record has been edited!'

        # send user to index.html with alert
        return redirect(url_for("index", alert=alert))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # grab variables and check the person being edited with the user's id. Prevents the user from editing client-side data and seeing other user's data

        userid = session.get("user_id")
        editPersonId = request.args.get('q')
        editPersonUserId = db.execute("SELECT userid FROM people WHERE id = ?", editPersonId)[0]['userid']

        if editPersonUserId != userid:
            return apology("Stop trying to tamper with things!", 403)

        alert = "None"

        person = db.execute("""SELECT people.id, people.userid, people.first, people.middle, people.last, people.birthdate, people.birthcity, people.deathdate, people.deathcity, people.occupation1, lineage.mother, lineage.father
                            FROM people JOIN lineage ON people.id = lineage.id WHERE people.id = ?;""", editPersonId)

        return render_template('editperson.html', alert=alert, person=person, editPersonId=editPersonId)


@app.route("/firstperson", methods=["GET", "POST"])
@login_required
def firstperson():
    """Add the user's information to the database"""

    # if POST
    if request.method == "POST":

        userid = session.get("user_id")

        # collect variables
        first = request.form.get("first")
        last = request.form.get("last")
        middle = request.form.get("middle")
        birthdate = request.form.get("birthdate")
        birthcity = request.form.get("birthcity")
        birthcountry = request.form.get("birthcountry")
        deathdate = request.form.get("deathdate")
        deathcity = request.form.get("deathcity")
        deathcountry = request.form.get("deathcountry")
        occupation1 = request.form.get("occupation1")
        occupation2 = request.form.get("occupation2")
        occupation3 = request.form.get("occupation3")

        # insert data into database - userid, symbol, shares, price (unique index automatic)
        db.execute("INSERT INTO people (userid, last, first, middle, birthdate, birthcity, birthcountry, deathdate, deathcity, deathcountry, occupation1, occupation2, occupation3) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", userid, last, first, middle, birthdate, birthcity, birthcountry, deathdate, deathcity, deathcountry, occupation1, occupation2, occupation3)

        selfid = db.execute("SELECT max(id) AS id FROM people WHERE userid = ?", userid)[0]['id']

        # 4.Create entry in lineage for new parent
        db.execute("INSERT INTO lineage (id, mother, father) VALUES (?, 0, 0)", selfid)

        # send alert to index.html
        alert = 'You are now in the system. Lets start building your tree by adding your parents!'

        # send user to index.html with alert
        return redirect(url_for("index.html", alert=alert))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("firstperson.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/newperson", methods=["GET", "POST"])
@login_required
def newperson():
    """Add a new person to the database"""

    # if POST
    if request.method == "POST":

        if not request.form.get("relative"):
            apology("Please go back and select a relative, 403")
        if not request.form.get("relation"):
            return apology("must provide a relationship type", 400)
        if not request.form.get("last"):
            return apology("must provide a last name", 400)
        if not request.form.get("first"):
            return apology("must provide a first name", 400)
        if not request.form.get("last"):
            return apology("must provide a last name", 400)

        # 1.collect person variables
        userid = session.get("user_id")
        first = request.form.get("first")
        last = request.form.get("last")
        middle = request.form.get("middle")
        birthdate = request.form.get("birthdate")
        birthcity = request.form.get("birthcity")
        birthcountry = request.form.get("birthcountry")
        deathdate = request.form.get("deathdate")
        deathcity = request.form.get("deathcity")
        deathcountry = request.form.get("deathcountry")
        occupation1 = request.form.get("occupation1")
        occupation2 = request.form.get("occupation2")
        occupation3 = request.form.get("occupation3")

        # 2.insert data into database - userid, symbol, shares, price (unique index automatic)
        db.execute("INSERT INTO people (userid, last, first, middle, birthdate, birthcity, birthcountry, deathdate, deathcity, deathcountry, occupation1, occupation2, occupation3) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", userid, last, first, middle, birthdate, birthcity, birthcountry, deathdate, deathcity, deathcountry, occupation1, occupation2, occupation3)

        # 3.collect lineage variables and insert
        parentid = db.execute("SELECT max(id) AS id FROM people WHERE userid = ?", userid)[0]['id']
        relative = request.form.get("relative")
        childid = relative
        # handle no relative entry
        if not relative:
            # Handle the case where no relative is selected
            apology("Please go back and select a relative, 403")

        # 4.Create entry in lineage for new parent
        db.execute("INSERT INTO lineage (id, mother, father) VALUES (?, 0, 0)", parentid)

        # 5.update child's lineagedb entry
        relation = request.form.get("relation")

        db.execute("UPDATE lineage SET ? = ? WHERE id = ?", relation, parentid, childid)

        # send alert to index.html
        alert = 'New Person Added! Add another?'

        # send user to index.html with alert
        return redirect(url_for("index", alert=alert))

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        # find user's relatives from people db and send them to the dropdown menu
        userid = session.get("user_id")
        relatives = db.execute("SELECT id, first, last, birthdate FROM people WHERE userid = ?", userid)
        childid = request.args.get("childid")
        relation = request.args.get("relation")

        return render_template("newperson.html", relatives=relatives, childid=childid, relation=relation)


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password by reentering it", 400)

        # Ensure password was the same both times
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("your passwords must match", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username is unique and password is correct
        if len(rows) >= 1:
            return apology("User name already taken", 400)

        # If Username is unique and passwords match, create a user in the database
        hashed_pw = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                   request.form.get("username"), hashed_pw)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        alert = "You are now registered!"

        return redirect(url_for("firstperson")) # In case you need this code:, alert=alert))

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        return render_template("register.html")
