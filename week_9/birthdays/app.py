import os
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

# Define valid months and days
MONTHS = [i for i in range(1, 13)]
DAYS = [i for i in range(1, 32)]

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get form inputs
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        # Validate inputs
        message = ""
        if not name or not month or not day:
            message = "All fields are required."
        elif int(month) not in MONTHS:
            message = "Month is invalid."
        elif int(day) not in DAYS:
            message = "Day is invalid."
        else:
            # Insert birthday into database
            db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)", name, int(month), int(day))

        # Fetch updated birthdays list
        birthdays = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", message=message, birthdays=birthdays)

    else:
        # Display the entries in the database on index.html
        birthdays = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", birthdays=birthdays)

@app.route("/delete", methods=["POST"])
def delete():
    # Get the id of the birthday to delete
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM birthdays WHERE id = ?", id)
    return redirect("/")
