import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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
    user = db.execute(
        "SELECT * FROM users WHERE id = ?", session["user_id"]
    )[0]
    user["cash"] = round(user["cash"], 2)
    # cash and stock's total value need to be rounded, because of binary floating-point representation.
    #   Computers store decimal numbers in binary floating-point format.
    #   221.7 * 3 might result in 665.0999999999999 instead of 665.10 due to binary floating-point representation.
    stocks = db.execute(
        """
        SELECT symbol, type, price, SUM(shares) as shares, ROUND(price * SUM(shares), 2) as total
        FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0
        """, session["user_id"]
    )
    # GROUP BY symbol, price: Cuz the price fluctuates.
    #   Even the same stock would not hold the same value over time.
    price_cache = {}    # Save the stock:price to avoid different current prices.
    stock_total = 0
    for stock in stocks:
        if stock["type"] == "DEPOSIT":
            continue
        symbol = stock["symbol"]
        if symbol not in price_cache:
            price_cache[symbol] = lookup(symbol)["price"]
        stock["current_price"] = price_cache[symbol]
        stock["current_total"] = round(stock["shares"] * stock["current_price"], 2)
        stock_total += stock["current_total"]
    return render_template("index.html", stocks=stocks, user=user, total_value=round(stock_total + user["cash"], 2))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # Validate input
        symbol = request.form.get("symbol")
        stock = lookup(symbol)
        if not stock:
            return apology("Invalid symbol.")
        try:
            share = int(request.form.get("shares"))
            if share < 0:
                return apology("Shares must be non-negative.")
        except (ValueError, TypeError):
            return apology("Invalid share.")

        # Calculate
        price = stock["price"]
        total_cost = share * price
        cash_before = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"]
        )[0]["cash"]
        # [0]:      Accesses the first and only dictionary in the list returned by db.execute().
        # ["cash"]: And then retrieves the cash value.
        if cash_before < total_cost:
            return apology("Insufficient cash.")
        cash_after = cash_before - total_cost

        # Update info
        if total_cost <= 0:
            flash("Invalid purchase, back to homepage.")
        else:
            db.execute(
                "UPDATE users SET cash = ? WHERE id = ?",
                cash_after, session["user_id"]
            )
            db.execute(
                """
                INSERT INTO transactions
                (user_id, type, symbol, price, shares, total, balance_before, balance_after)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, session["user_id"], "BUY", symbol.upper(), price, share, total_cost, cash_before, cash_after
            )
            flash(f"Bought {share} shares of {symbol.upper()} for {usd(total_cost)}.")
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user = db.execute(
        "SELECT * FROM users WHERE id = ?", session["user_id"]
    )[0]
    stocks = db.execute(
        """
        SELECT symbol, type, price, shares, ROUND(price * shares, 2) as total, timestamp
        FROM transactions WHERE user_id = ? ORDER BY timestamp DESC
        """, session["user_id"]
    )
    price_cache = {}
    # Attention to how price, share and total are recorded for DEPOSIT in transactions
    for stock in stocks:
        if stock["type"] == "DEPOSIT":
            stock["price"] = ""
            stock["shares"] = ""
            stock["current_total"] = stock["total"]
            continue
        symbol = stock["symbol"]
        if symbol not in price_cache:
            price_cache[symbol] = lookup(symbol)["price"]
        stock["current_price"] = price_cache[symbol]
        stock["current_total"] = round(stock["shares"] * stock["current_price"], 2)
    return render_template("history.html", stocks=stocks, user=user)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password", 403)

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
        symbol = request.form.get("symbol")
        stock = lookup(symbol)
        if not stock:
            return apology("Invalid symbol.")
        return render_template("quoted.html", stock=stock)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            return apology("Invalid username/password/confirmation.")
        if password != confirmation:
            return apology("Password confirmation failed.")
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        if len(rows):
            return apology("Username already taken.")

        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password)
        )
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    stocks = db.execute(
        # Retrieve user info
        """
        SELECT symbol, SUM(shares) as shares
        FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0
        """, session["user_id"]
    )

    if request.method == "POST":
        # Validate input
        symbol = request.form.get("symbol")
        if not symbol or symbol not in [stock["symbol"] for stock in stocks]:
            return apology("Invalid symbol.")
        try:
            share = int(request.form.get("shares"))
        except (ValueError, TypeError):
            return apology("Invalid share.")
        if share < 0:
            return apology("Shares must be non-negative.")

        # Calculate
        for s in stocks:
            if s["symbol"] == symbol:
                stock_shares = s["shares"]
                break
        if share > stock_shares:
            return apology("Insufficient share.")
        price = lookup(symbol)["price"]
        revenu = price * share
        cash_before = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"]
        )[0]["cash"]
        cash_after = cash_before + revenu

        # Update user info
        if revenu <= 0:
            flash("Invalid trade, back to homepage.")
        else:
            db.execute(
                "UPDATE users SET cash = ? WHERE id = ?",
                cash_after, session["user_id"]
            )
            # Select the most profitable trades
            db.execute(
                """
                INSERT INTO transactions
                (user_id, type, symbol, price, shares, total, balance_before, balance_after)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, session["user_id"], "SELL", symbol.upper(), price, -share, revenu, cash_before, cash_after
            )
            flash(f"Sold {share} shares of {symbol.upper()} for {usd(revenu)}.")
        return redirect("/")
    else:
        return render_template("sell.html", stocks=stocks)


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        password = request.form.get("current_password")
        if not password:
            return apology("Must provide password", 403)
        user = db.execute(
            "SELECT * FROM users WHERE id = ?", session["user_id"]
        )[0]
        if not check_password_hash(user["hash"], password):
            return apology("Invalid password", 403)
        new_password = request.form.get("new_password")
        if new_password != request.form.get("confirm_password"):
            return apology("Invalid new password", 403)
        hash = generate_password_hash(new_password)
        db.execute(
            "UPDATE users SET hash = ? WHERE id = ?",
            hash, session["user_id"]
        )
        flash("Password changed successfully.")
        return redirect("/")
    else:
        return render_template("change_password.html")


@app.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit():
    if request.method == "POST":
        amount = request.form.get("deposit")
        if not amount:
            flash("No deposit made.")
            return redirect("/")
        try:
            amount = round(float(amount), 2)
            if amount < 0:
                return apology("Deposit must be non-negative.")
        except (ValueError, TypeError):
            return apology("Invalid deposit.")
        cash_before = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"]
        )[0]["cash"]
        cash_after = round(cash_before + amount, 2)
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?",
            cash_after, session["user_id"]
        )
        # Save in History
        db.execute(
            """
                INSERT INTO transactions
                (user_id, type, symbol, price, shares, total, balance_before, balance_after)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, session["user_id"], "DEPOSIT", "CASH", amount, 1, amount, cash_before, cash_after
        )
        flash("Deposited successfully.")
        return redirect("/")
    else:
        return render_template("deposit.html")
