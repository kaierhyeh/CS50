import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


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
        # TODO: Add the user's entry into the database
        name = request.form.get("name")
        month = int(request.form.get("month"))  # .get is the only way to retrieve data and it always returns a string
        day = int(request.form.get("day"))
        if bday_check(name, month, day):
            db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)", \
                                                name, month, day)
        return redirect("/")

    else:
        # TODO: Display the entries in the database on index.html
        birthdays = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", birthdays=birthdays)

def bday_check(name, month, day):
    if not name:
        return False
    if not (1 <= month <= 12):
        return False
    elif month == 2 and not (1 <= day <= 29):
        return False
    elif month in [4, 6, 9, 11] and not (1 <= day <= 30):
        return False
    elif not (1 <= day <= 31):
        return False
    return True
