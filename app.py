import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

##### Configure application
app = Flask(__name__)

##### Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

##### Configure CS50 Library to use SQLite database
db = SQL("sqlite:///contactus.db")


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
    """Show contacts"""

    user_id = session["user_id"]
    contacts = db.execute("SELECT *, STRFTIME('%d/%m/%Y', last) as last FROM contacts WHERE user_id = ?", user_id)

    if contacts == None:
        return render_template("index.html")

    else:
        return render_template("index.html", contacts = contacts)


@app.route("/search", methods=["GET", "POST"])
def search():
    """Search contacts"""

    if request.method == "GET":
        return redirect("/")

    else:
        user_id = session["user_id"]
        search = request.form.get("search")

        contacts = db.execute("SELECT *, STRFTIME('%d/%m/%Y', last) as last FROM contacts WHERE name LIKE ? AND user_id = ?", "%" + search + "%", user_id)

        return render_template("index.html", contacts = contacts)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "GET":
        session.clear()
        return render_template("register.html")

    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            flash("must provide username")
            return render_template("register.html")

        elif not password:
            flash("must provide password")
            return render_template("register.html")

        elif not confirmation:
            flash("must confirm password")
            return render_template("register.html")

        elif password != confirmation:
            flash("passwords do not match")
            return render_template("register.html")

        hash = generate_password_hash(password)

        if db.execute("SELECT username FROM users WHERE username = ?", username):
            flash("username already exists")
            return render_template("register.html")
        else:
            db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)", username, hash
            )

        new_user = db.execute("SELECT id FROM users WHERE username = ?", username)

        session["user_id"] = new_user[0]["id"]

        return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("must provide username")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("must provide password")
            return render_template("login.html")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            flash("invalid username and/or password")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        session.clear()
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/add-contact", methods=["GET", "POST"])
@login_required
def add_contact():
    """Add contact"""

    user_id = session["user_id"]

    if request.method == "GET":
        contact = []
        return render_template("add-contact.html", contact = contact)

    else:
        db.execute("INSERT INTO contacts (name, passion, work, tel, email, last, notes, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                request.form.get("name"), request.form.get("passion"), request.form.get("work"), request.form.get("first-tel"),
                request.form.get("email"), request.form.get("last"), request.form.get("notes"), user_id)

        return redirect("/")


@app.route("/update-contact")
@login_required
def update_contact():
    """Delete contact"""

    user_id = session["user_id"]
    contact_id = request.args.get("id")

    db.execute("UPDATE contacts SET last = DATE('now') WHERE id = ? AND user_id = ?", contact_id, user_id)

    return redirect("/")


@app.route("/edit-contact", methods=["GET", "POST"])
@login_required
def edit_contact():
    """Edit contact"""

    user_id = session["user_id"]

    if request.method == "GET":
        contact_id = request.args.get("id")
        contact = db.execute("SELECT * FROM contacts WHERE id = ? AND user_id = ?", contact_id, user_id)
        return render_template("edit-contact.html", contact = contact[0])

    else:
        contact_id = request.form.get("contact_id")
        db.execute("UPDATE contacts SET name = ?, passion = ?, work = ?, tel = ?, email = ?, last = ?, notes = ? WHERE id = ? AND user_id = ?",
            request.form.get("name"), request.form.get("passion"), request.form.get("work"), request.form.get("first-tel"),
            request.form.get("email"), request.form.get("last"), request.form.get("notes"), contact_id, user_id)
        return redirect("/")


@app.route("/delete-contact")
@login_required
def delete_contact():
    """Delete contact"""

    user_id = session["user_id"]
    contact_id = request.args.get("id")

    db.execute("DELETE FROM contacts WHERE id = ? AND user_id = ?", contact_id, user_id)

    return redirect("/")


@app.route("/settings")
@login_required
def settings():
    """Settings"""

    return render_template("settings.html")


@app.route("/settings/delete-all", methods=["GET", "POST"])
@login_required
def delete_all():
    """Delete all contacts"""

    if request.method == "GET":
        return render_template("settings.html")

    else:
        user_id = session["user_id"]

        db.execute("DELETE FROM contacts WHERE user_id = ?", user_id)

        return redirect("/")


@app.route("/settings/delete-account", methods=["GET", "POST"])
@login_required
def delete_account():
    """Delete all contacts"""

    if request.method == "GET":
        return render_template("settings.html")

    else:
        user_id = session["user_id"]

        db.execute("DELETE FROM contacts WHERE user_id = ?", user_id)
        db.execute("DELETE FROM users WHERE id = ?", user_id)

        """Log user out"""

        # Forget any user_id
        session.clear()

        # Redirect user to login form
        return redirect("/")


@app.route("/settings/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    """Change Password"""

    if request.method == "GET":
        return render_template("settings.html")

    else:
        user_id = session["user_id"]

        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")

        if new_password == "":
            flash("new password mustn't be empty")
            return render_template("settings.html")

        rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)

        if check_password_hash(rows[0]["hash"], old_password):
            hash = generate_password_hash(new_password)
        else:
            flash("old password incorrect")
            return render_template("settings.html")

        db.execute("UPDATE users SET hash = ? WHERE id = ?", hash, user_id)

        flash("password changed")
        return render_template("settings.html")


@app.route("/settings/change-username", methods=["GET", "POST"])
@login_required
def change_username():
    """Change Username"""

    if request.method == "GET":
        return render_template("settings.html")

    else:
        user_id = session["user_id"]

        old_username = request.form.get("old_username")
        new_username = request.form.get("new_username")

        if new_username == "":
            flash("new username mustn't be empty")
            return render_template("settings.html")

        username = db.execute("SELECT username FROM users WHERE id = ?", user_id)

        if old_username == username[0]["username"]:
            db.execute("UPDATE users SET username = ? WHERE id = ?", new_username, user_id)

        else:
            flash("username does not exist")
            return render_template("settings.html")

        flash("username changed")
        return render_template("settings.html")

