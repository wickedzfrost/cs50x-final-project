from datetime import datetime
import random

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, generate, check, genword, genword_special
from stack import track, reset_stack

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///users.db")


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
    return render_template("index.html")


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


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        name = request.form.get("username")
        password = request.form.get("password")
        c_password = request.form.get("confirmation")
        if not name or not password or not c_password:
            return apology("Username or password cannot be empty!")
        elif password != c_password:
            return apology("Password do not match!")
        elif db.execute("SELECT username FROM users WHERE username = (?);", name):
            return apology("Username taken!")
        elif len(password) < 6:
            return apology("Please use a longer password!")
        else:
            db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?);",
                name,
                generate_password_hash(password),
            )
            session["user_id"] = db.execute(
                "SELECT id FROM users WHERE username = (?)", name
            )[0]["id"]
            return redirect("/")


@app.route("/play", methods=["GET", "POST"])
@login_required
def play():
    ls = generate()
    dict = ls[0]
    word = ""
    definition = ""
    for key, value in dict.items():
        word = key
        definition = value
    reset_stack()
    return render_template("play.html", word=word, definition=definition, score=0)


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    username = db.execute("SELECT username FROM users WHERE id = (?);", session["user_id"])[0]["username"]
    return render_template("settings.html", name=username)


@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    score_ls = db.execute("SELECT score, time FROM scores WHERE id = (?);", session["user_id"])
    score_ls.reverse()
    return render_template("history.html", score=score_ls)


@app.route("/scores", methods=["GET", "POST"])
@login_required
def scores():
    info = db.execute("SELECT username, score FROM scores JOIN users ON scores.id = users.id ORDER BY score DESC LIMIT 5")
    print(info)
    return render_template("scores.html", info=info)


@app.route("/rules", methods=["GET", "POST"])
@login_required
def rules():
    return render_template("rules.html")


@app.route("/script", methods=["GET", "POST"])
@login_required
def script():
    input = check(request.get_data())
    if input != "False":
        return input
    else:
        return "FALSE"


@app.route("/genword", methods=["POST"])
@login_required
def gen_word():
    mora = request.get_data()
    return genword(mora)


@app.route("/genword_special", methods=["POST"])
@login_required
def gen_word_s():
    mora = request.get_data()
    return genword_special(mora)


@app.route("/submit", methods=["POST"])
@login_required
def submit():
    user_input = request.get_data()
    var = track(user_input)
    return var


@app.route("/submit_score", methods=["POST"])
@login_required
def score():
    score = request.get_data()
    score = int(score[6:len(score)])
    curr = datetime.now()
    curr = curr.strftime("%d/%m/%Y %H:%M:%S")
    db.execute("INSERT INTO scores VALUES (?, ?, ?);", session["user_id"], score, curr)
    score = "0"
    return score


@app.route("/un", methods=["GET", "POST"])
@login_required
def un():
    if request.method == "POST":
        name = request.form.get("username")
        confirm = request.form.get("confirm")
        if name == confirm:
            if db.execute("SELECT username FROM users WHERE username = (?);", name):
                return apology("Username taken!")
            original_name = db.execute("SELECT username FROM users WHERE id = (?);", session["user_id"])[0]["username"]
            db.execute("UPDATE users SET (username) = (?) WHERE username = (?);", name, original_name)
            return render_template("settings.html", name=name)
        else:
            return apology("Username not same")
    else:
        username = db.execute("SELECT username FROM users WHERE id = (?);", session["user_id"])[0]["username"]
        return render_template("un.html", name=username)


@app.route("/ps", methods=["GET", "POST"])
@login_required
def ps():
    if request.method == "POST":
        current = request.form.get("current")
        new = request.form.get("new")
        confirm = request.form.get("confirm")
        curr = db.execute("SELECT hash FROM users WHERE id = (?);", session["user_id"])[0]["hash"]
        if not check_password_hash(curr, current):
            return apology("Invalid current password")
        else:
            if len(new) < 6:
                return apology("Please use a longer password!")

            if new == confirm:
                db.execute("UPDATE users SET (hash) = (?) WHERE id = (?);", generate_password_hash(new), session["user_id"])
                return render_template("ps.html", flash_message="true")
            else:
                return apology("New password does not match")
    else:
        return render_template("ps.html")
