import requests
from flask import redirect, render_template, session
from functools import wraps


# Sorry, not sorry: Apologizing with style
def apology(message, code=400):
    """Render an apology message because, well, something went wrong... oops."""

    def escape(s):
        """
        Escape special characters to avoid offending the HTML gods.

        Special thanks to the memegen team for this! https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),  # Double dash means serious business
            (" ", "-"),  # Space is the final frontier
            ("_", "__"),  # Snake_case fans rejoice
            ("?", "~q"),  # Question everything
            ("%", "~p"),  # 100% guarantee this works... probably
            ("#", "~h"),  # Hashing things out here
            ("/", "~s"),  # Slash, but make it fancy
            ('"', "''"),  # Double quotes need double attention
        ]:
            s = s.replace(old, new)
        return s

    # Returning the apology with style
    return render_template("apology.html", top=code, bottom=escape(message)), code


# You shall not pass... unless you're logged in
def login_required(f):
    """
    Force users to log in, because security is cool.

    Inspired by Flask's ancient scrolls: https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If they're not logged in, send them to the login page. No freeloaders here!
        if session.get("user_id") is None:
            return redirect("/login")
        # Proceed if you're worthy
        return f(*args, **kwargs)

    return decorated_function


# Let's go stock shopping
def lookup(symbol):
    """Look up stock quote, because pretending to know it doesn't work well."""

    # The mighty API, answering our prayers
    url = f"https://finance.cs50.io/quote?symbol={symbol.upper()}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Uh-oh, something's wrong if we get an error
        quote_data = response.json()  # Turn that JSON gobbledygook into something useful

        # Return the good stuff: stock name, price, and symbol
        return {
            "name": quote_data["companyName"],
            "price": quote_data["latestPrice"],
            "symbol": symbol.upper()
        }
    except requests.RequestException as e:
        # Classic network error – probably the internet's fault
        print(f"Request error: {e}")
    except (KeyError, ValueError) as e:
        # When parsing goes wrong... like a bad puzzle
        print(f"Data parsing error: {e}")
    return None  # Sorry, no stock info for you


# Turn boring numbers into snazzy dollars
def usd(value):
    """Format value as USD because numbers look better with dollar signs."""

    # We love commas and decimals
    return f"${value:,.2f}"  # Show me the money!


# Make those stock prices fancy
def format_stock_prices(stock_data):
    """Make stock prices look like they belong on Wall Street."""

    # Transform each stock into a piece of financial art
    for stock in stock_data:
        stock['price'] = usd(stock['price'])
        stock['total_price'] = usd(stock['total_price'])
    return stock_data  # Now you're trading like a pro!
