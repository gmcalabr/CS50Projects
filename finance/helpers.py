import csv
import datetime
import pytz
import requests
import urllib
import uuid

from flask import redirect, render_template, request, session
from functools import wraps

from cs50 import SQL

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def success(message, code=200):
    """Render success page to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("success.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""
    url = f"https://finance.cs50.io/quote?symbol={symbol.upper()}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP error responses
        quote_data = response.json()
        return {
            "name": quote_data["companyName"],
            "price": quote_data["latestPrice"],
            "symbol": symbol.upper()
        }
    except requests.RequestException as e:
        print(f"Request error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Data parsing error: {e}")
    return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


def commonstart(symbol, shares, userid):
    # check if variable is left empty, apologize
    if not symbol:
        return apology("Must provide a ticker symbol", 400)

    # run stock price lookup and save to variable
    shareprice = lookup(symbol)

    # Check if symbol is valid, apologize
    if shareprice is None or 'price' not in shareprice:
        return apology("Invalid ticker symbol", 403)

    # check if shares is integer>0
    try:
        shares = int(shares)
        if shares <= 0:
            return apology("Invalid number of shares requested", 403)
        if not shares.isdigit() or int(shares) <= 0:
            return apology("Invalid number of shares requested", 403)
    except ValueError:
        return apology("Shares must be a positive integer", 403)

    # convert price to shareprice
    price = shareprice['price']

    # lookup user's cash
    cash = db.execute("SELECT cash FROM users WHERE id = ?", userid)[0]['cash']

    return {"price": price, "cash": cash}


def commonend(symbol, shares, userid, price, cash):
    # insert data into database - userid, symbol, shares, price (unique index automatic)
    db.execute("INSERT INTO log (userid, symbol, shares, price, timestamp) VALUES (?, ?, ?, ?, strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))",
               userid, symbol, shares, price)

    # change cash from user db
    newcash = cash - (int(shares) * price)
    db.execute("UPDATE users SET cash = ? WHERE id = ?", newcash, userid)

    return None
