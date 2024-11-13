import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, success, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


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
    """Show portfolio of stocks"""

    # get userid from users db
    userid = session.get("user_id")

    # get info from finance.db and set it equal to stocks
    stocks = db.execute("SELECT symbol, SUM(shares) AS shares FROM log WHERE userid= ? GROUP BY symbol", userid)

    # calculate total shares value and lookup user cash
    cash = db.execute("SELECT cash FROM users WHERE id = ?", userid)[0]['cash']
    totalsharevalue = 0

    for stock in stocks:
        shares = stock['shares']
        result = lookup(stock['symbol'])

        print("shares: ", shares)
        print("price: ", result['price'])

        totalsharevalue += ( shares * result['price'])

    return render_template("index.html", stocks=stocks, lookup=lookup, usd=usd, cash=cash, totalsharevalue=totalsharevalue)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # if POST
    if request.method == "POST":

        # take in variables symbol and shares
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # check if variable is left empty, apologize
        if not symbol:
            return apology("Must provide a ticker symbol", 400)

        # run stock price lookup and save to variable
        shareprice = lookup(symbol)

        # check if symbol is valid, apologize
        if shareprice is None:
            return apology("Invalid ticker symbol", 403)

        # check if shares is integer>0
        try:
            shares = int(shares)
            if shares <= 0:
                return apology("Invalid number of shares requested", 403)
        except ValueError:
            return apology("Shares must be a positive integer", 403)

        price = shareprice['price']

        # get userid from users db
        userid = session.get("user_id")

        # lookup user's cash
        cash = db.execute("SELECT cash FROM users WHERE id = ?", userid)[0]['cash']

        # compare cash to transactionCost
        if cash < (shares * price):
            return apology("Not enough cash for that transaction", 403)

        # timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # insert data into database - userid, symbol, shares, price (unique index automatic)
        db.execute("INSERT INTO log (userid, symbol, shares, price, timestamp) VALUES (?, ?, ?, ?, strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))", userid, symbol, shares, price)

        # remove cash from user db
        newcash = cash - (shares * price)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", newcash, userid)

        prettyprice = usd(price)

        newcash = usd(newcash)

        #send variables to quote.html via post
        return render_template("buy.html", symbol=symbol, shares=shares, prettyprice=prettyprice, newcash=newcash, timestamp=timestamp)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":

        #check if variable is left empty, apologize
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Must provide a ticker symbol", 400)

        #run stock price lookup and save to variable
        shareprice = lookup(symbol)

        #check if symbol is valid, apologize
        if shareprice is None:
            return apology("Invalid ticker symbol", 403)

        #send variables to quote.html via post
        return render_template("quote.html", shareprice=shareprice)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")



@app.route("/register", methods=["GET", "POST"])
def register():

    # Forget any user_id
    ########################session.clear()

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure password was submitted
        elif not request.form.get("pconfirm"):
            return apology("must confirm password by reentering it", 403)

        # Ensure password was the same both times
        if request.form.get("password") != request.form.get("pconfirm"):
            return apology("your passwords must match", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username is unique and password is correct
        if len(rows) >= 1:
            return apology("User name already taken", 403)

        # If Username is unique and passwords match, create a user in the database
        hashed_pw = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), hashed_pw)

        return success("You did it, you're in!")

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")
