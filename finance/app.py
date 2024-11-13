import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd, commonstart, commonend

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

    # grab alert if redirected here from /buy successful purchase
    alert = request.args.get("alert")

    # get userid from users db
    userid = session.get("user_id")

    # get info from finance.db and set it equal to stocks
    stocks = db.execute(
        "SELECT symbol, SUM(shares) AS shares FROM log WHERE userid = ? AND symbol != 'cash injection' GROUP BY symbol", userid)

    # calculate total shares value and lookup user cash
    cash = db.execute("SELECT cash FROM users WHERE id = ?", userid)[0]['cash']
    totalsharevalue = 0

    for stock in stocks:
        shares = stock['shares']
        if shares is None:
            shares = 0
        result = lookup(stock['symbol'])

        totalsharevalue += (shares * result['price'])

    return render_template("index.html", alert=alert, stocks=stocks, lookup=lookup, usd=usd, cash=cash, totalsharevalue=totalsharevalue)


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    # if POST
    if request.method == "POST":

        # collect variables
        injection = request.form.get("injection")
        userid = session.get("user_id")

        # check if injection is left empty, apologize
        if not injection:
            return apology("Must enter an amount to inject into your account", 400)

        # check if shares is integer>0
        try:
            injection = int(injection)
            if injection <= 0:
                return apology("Invalid dollar value", 400)
        except ValueError:
            return apology("Injection value must be a positive integer", 400)

        # lookup user's cash
        cash = db.execute("SELECT cash FROM users WHERE id = ?", userid)[0]['cash']

        # add injection to cash and post to users and log
        cash = cash + injection
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, userid)
        db.execute("INSERT INTO log (userid, symbol, shares, price, timestamp) VALUES (?, ?, ?, ?, strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))",
                   userid, 'cash injection', '0', injection)

        # send alert to index.html
        alert = 'injected'

        # send user to index.html with alert
        return redirect(url_for("index", alert=alert))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("add.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # if POST
    if request.method == "POST":

        # collect variables
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        userid = session.get("user_id")

        # call commonstart --return {"price": price, "cash": cash}
        csresponse = commonstart(symbol, shares, userid)

        # Check if csresponse is a dictionary
        if isinstance(csresponse, dict):

            # check user's cash levels before allowing transaction
            if csresponse['cash'] < (csresponse['price']) * int(shares):
                return apology("Insufficient funds", 403)

        # call commonend --return None
        commonend(symbol, shares, userid, csresponse['price'], csresponse['cash'])

        # send alert to index.html
        alert = 'bought'

        # send user to index.html with alert
        return redirect(url_for("index", alert=alert))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():

    # get userid
    userid = session.get("user_id")

    # get info from finance.db and set it equal to stocks
    stocks = db.execute(
        "SELECT symbol, shares, price, timestamp FROM log WHERE userid= ? ORDER BY timestamp", userid)

    return render_template("history.html", stocks=stocks, usd=usd)


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":

        # check if variable is left empty, apologize
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Must provide a ticker symbol", 400)

        # run stock price lookup and save to variable
        shareprice = lookup(symbol)

        # check if symbol is valid, apologize
        if shareprice is None:
            return apology("Invalid ticker symbol", 400)

        # send variables to quote.html via post
        return render_template("quote.html", shareprice=shareprice)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


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

        alert = "success"

        return redirect(url_for("index", alert=alert))

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # if POST
    if request.method == "POST":

        # collect variables
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        userid = session.get("user_id")

        # check if the requested symbol is owned by the user
        stocks = db.execute(
            "SELECT symbol, SUM(shares) AS shares FROM log WHERE userid = ? AND symbol != 'cash injection' GROUP BY symbol", userid)

        owns_stock = False
        for stock in stocks:
            if symbol == stock['symbol']:
                owns_stock = True
                break

        if not owns_stock:
            return apology("You don't own that stock", 403)

        # call commonstart --return {"price": price, "cash": cash}
        csresponse = commonstart(symbol, shares, userid)

        # lookup user's cash
        usershares = db.execute("SELECT shares FROM log WHERE symbol = ?", symbol)[0]['shares']

        # check user's share count before attempting to sell more than they have
        if usershares < int(shares):
            return apology("You don't have that many shares", 403)

        # invert shares to represent sale
        shares = -int(shares)

        # call commonend --return None
        commonend(symbol, shares, userid, csresponse['price'], csresponse['cash'])

        # send alert to index
        alert = 'sold'

        # send user to index.html with alert
        return redirect(url_for("index", alert=alert))

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        # lookup user's stocks owned
        userid = session.get("user_id")
        stocks = db.execute(
            "SELECT symbol, SUM(shares) AS shares FROM log WHERE userid = ? AND symbol != 'cash injection' GROUP BY symbol", userid)

        return render_template("sell.html", stocks=stocks)
