import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd, format_stock_prices

# It's Flask time!
app = Flask(__name__)

# Custom filter to make things look more like money
app.jinja_env.filters["usd"] = usd

# Make Flask store session stuff on the filesystem, not in cookies (cookies are for snacks)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Use CS50's library to talk to the database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Prevent the browser from hoarding cache like a dragon guarding gold"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show off the user's awesome stock portfolio"""

    # Get the user's stock data... if they have any
    stock_data = db.execute(
        "SELECT symbol, SUM(shares) shares, price, SUM(total_price) total_price FROM \
        stocks WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"])

    # Get their cash... probably not as much as they'd like
    user_data = db.execute(
        "SELECT cash FROM users WHERE id = ?", session["user_id"])
    account_data = db.execute(
        "SELECT SUM(total_price) paid FROM stocks WHERE user_id = ?", session["user_id"])
    total_cash = user_data[0]['cash']

    if account_data[0]['paid']:
        total_cash = account_data[0]['paid'] + user_data[0]['cash']

    stock_data = format_stock_prices(stock_data)

    return render_template("index.html",
                           stocks=stock_data,
                           cash=usd(user_data[0]['cash']),
                           total=usd(total_cash))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy stocks, become a mogul... or just lose some money, who knows"""

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Must have symbol, duh
        if not symbol:
            return apology("must provide symbol")
        if not shares:
            return apology("must provide shares")
        if not shares.isdigit():
            return apology("num of shares not valid")

        shares = int(shares)

        # Nobody likes negative shares, except for short-sellers
        if shares <= 0:
            return apology("num of shares not valid")

        stock_data = lookup(symbol)

        if not stock_data:
            return apology("Symbol not found")

        user_data = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"])

        total_price = stock_data['price'] * shares
        cash = user_data[0]["cash"] - total_price

        if user_data[0]["cash"] < total_price:
            return apology("Not enough cash to complete the purchase")

        # Insert stock transaction and update user's cash
        db.execute(
            "INSERT INTO stocks (user_id, symbol, price, shares, total_price) \
            VALUES (?, ?, ?, ?, ?)",
            session["user_id"],
            stock_data['symbol'],
            stock_data['price'],
            shares, total_price
        )
        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                   cash, session["user_id"])

        flash("Purchase completed successfully!")

        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show off the user's stock history. Hope it's not too embarrassing"""

    stock_data = db.execute(
        "SELECT symbol, shares, price, total_price, date_created \
         FROM stocks WHERE user_id = ?", session["user_id"])

    stock_data = format_stock_prices(stock_data)

    return render_template("history.html", stocks=stock_data)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in. No login, no fun."""

    # Make sure the session is cleared for a fresh start
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("must provide username")

        if not password:
            return apology("must provide password")

        # Look up the user in the database
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", username
        )

        # Check if the username exists and if the password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username and/or password")

        # Log them in by storing the user ID in the session
        session["user_id"] = rows[0]["id"]

        return redirect("/")

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log the user out. Bye-bye session!"""

    session.clear()

    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Give stock quotes to users who don't know the prices off the top of their heads"""

    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("must provide a symbol")

        quote_data = lookup(symbol)

        if quote_data:
            return render_template("quoted.html",
                                   price=usd(quote_data['price']),
                                   symbol=quote_data['symbol'])

        return apology("Symbol not found")

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register new users so they can start losing money too"""

    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username")
        if not password:
            return apology("must provide password")
        if not confirmation:
            return apology("must confirm password")
        if password != confirmation:
            return apology("password and confirmation do not match")

        existing_users = db.execute(
            "SELECT id FROM users WHERE username = ?", username
        )

        if len(existing_users) >= 1:
            return apology("Username already exists")

        password_hash = generate_password_hash(password)

        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)", username, password_hash
        )

        return redirect("/")

    return render_template("register.html")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Add more cash because we all know you need it"""

    if request.method == "POST":
        cash = request.form.get("cash")
        if not cash:
            return apology("must provide cash")

        user_data = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"])
        total_cash = int(cash) + user_data[0]['cash']

        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                   total_cash, session["user_id"])

        flash("Cash added successfully!")

        return redirect("/")

    return render_template("add.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell those stocks before they tank!"""

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must provide symbol")
        if not shares:
            return apology("must provide shares")
        if int(shares) <= 0:
            return apology("num of shares not valid")

        stock_data = lookup(symbol)

        if not stock_data:
            return apology("Symbol not found")

        user_data = db.execute(
            "SELECT SUM(s.shares) shares, SUM(s.total_price) price, u.cash FROM users u \
            INNER JOIN stocks s ON s.user_id = u.id WHERE u.id = ? \
            AND symbol = ? GROUP BY s.symbol, u.cash",
            session["user_id"],
            symbol)

        if not user_data:
            return apology("Symbol not found")

        shares = int(shares)
        if user_data[0]['shares'] < shares:
            return apology("Not enough shares to complete the sale")

        total_price = stock_data['price'] * shares
        new_cash = total_price + user_data[0]['cash']

        db.execute(
            "INSERT INTO stocks (user_id, symbol, price, shares, total_price) \
            VALUES (?, ?, ?, ?, ?)",
            session["user_id"],
            stock_data['symbol'],
            stock_data['price'],
            -shares,
            -total_price
        )
        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                   new_cash, session["user_id"])

        flash("Sale completed successfully!")
        return redirect("/")

    # Handle GET request to render sell.html
    user_stocks = db.execute(
        "SELECT symbol, SUM(shares) AS shares FROM stocks WHERE user_id = ? GROUP BY symbol HAVING shares > 0",
        session["user_id"]
    )

    return render_template("sell.html", stocks=user_stocks)
