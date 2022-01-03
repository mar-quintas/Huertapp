import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required
import json

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///huertapp.db")


@app.route("/",  methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""
    if request.method == "POST":
        db.execute("UPDATE users_plants SET sow_date=? WHERE plant_id =? AND user_id = ?", request.form.get('date'), request.form.get('id'), session['user_id'])

        return redirect("/")
    else:
        # Select all the vegetables of the current user if any
        vegetables = db.execute(
            'SELECT * FROM plants JOIN users_plants ON plants.id = users_plants.plant_id WHERE user_id = ?', session['user_id'])

        return render_template("index.html", vegetables=vegetables)


@app.route('/vegetables_catalog', methods=["GET", "POST"])
@login_required
def plants():
    """Display all vegetables the user hasnt selected from the vegetables table as boostrap's cards"""
    vegetables = db.execute(
        'SELECT * FROM plants WHERE id NOT IN(SELECT plant_id FROM users_plants WHERE user_id = ?)', session['user_id'])

    return render_template("vegetables_catalog.html", vegetables=vegetables)

@app.route('/my_garden', methods=["GET", "POST"])
@login_required
def my_garden():
    """Display the garden and add vegetables to it"""
    vegetables = db.execute(
        'SELECT * FROM plants WHERE id IN(SELECT plant_id FROM users_plants WHERE user_id = ?)', session['user_id'])

    return render_template("my_garden.html", vegetables=vegetables)

@app.route('/my_plot', methods=["GET", "POST"])
@login_required
def my_plot():
    """Allow the user to plan a plot of the garden"""
    vegetables = db.execute(
        'SELECT * FROM plants WHERE id IN(SELECT plant_id FROM users_plants WHERE user_id = ?)', session['user_id'])

    return render_template('my_plot.html', vegetables=vegetables)

@app.route('/compatible')
@login_required
def compatible():
    """Check for compatible vegetals provided on initial vegetable"""

    compatible = db.execute('SELECT name, id FROM plants WHERE ID in(SELECT compatible FROM compatible_plants WHERE vegetable = ?)', request.args.get('id'))

    return json.dumps(compatible)

@app.route('/add', methods=["POST"])
@login_required
def add():
    """Add a vegetable to the current user's vegetables"""

    # Check if the user already has that vegetable
    user_veg = []
    for vegetable in db.execute('SELECT plant_id FROM users_plants WHERE user_id=?', session['user_id']):
        user_veg.append(vegetable['plant_id'])
    print(user_veg)

    new_veg = int(request.form.get('id'))

    # Add the vegetable to the user's vegetables
    if new_veg not in user_veg:
        db.execute(
            'INSERT INTO users_plants(user_id, plant_id) VALUES (?,?)', session['user_id'], new_veg)

    return redirect("/vegetables_catalog")

@app.route('/remove', methods=["POST"])
@login_required
def remove():
    """Remove a vegetable from the current user's vegetables"""

    # Check if the user already has that vegetable
    user_veg = []
    for vegetable in db.execute('SELECT plant_id FROM users_plants WHERE user_id=?', session['user_id']):
        user_veg.append(vegetable['plant_id'])

    new_veg = int(request.form.get('id'))

    # Remove the vegetable from the user's vegetables
    if new_veg in user_veg:
        db.execute('DELETE FROM users_plants WHERE user_id=? AND plant_id=?', session['user_id'], new_veg)

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
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
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

    if request.method == "POST":

        username = request.form.get('username')
        # Store the hash generated from the password
        pass_hash = generate_password_hash(request.form.get("password"))

        # Check if username was provided
        if not username:
            return apology("Must provide username")

        # Check if username already exists
        check_user = []
        for dic in db.execute("SELECT username FROM users"):
            check_user.append(dic['username'])

        if username in check_user:
            return apology("Username already exists, please select another")

        # Check if password was provided
        if not request.form.get('password'):
            return apology("Must provide password")

        # Check if password confirmation was provided and matches the original
        if not request.form.get('confirmation') == request.form.get('password'):
            return apology("Must enter same password")

        # Store the username and the password Hash in finance.db
        id = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, pass_hash)

        # Log in the user and remember it
        user_id = db.execute("SELECT id FROM users WHERE username = ?", username)

        session["user_id"] = user_id[0]['id']

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/pass", methods=["GET", "POST"])
@login_required
def password():
    """Change password"""
    if request.method == 'POST':

        rows = db.execute("SELECT * FROM users WHERE id = ?", session['user_id'])

        if not check_password_hash(rows[0]["hash"], request.form.get('password')):
            return apology('Please enter current password')

        if not request.form.get('new_pass'):
            return apology('Please enter new password')

        if check_password_hash(rows[0]["hash"], request.form.get('new_pass')):
            return apology('Please enter a different password')

        if not request.form.get('confirmation'):
            return apology('Please confirm your password')

        if request.form.get('confirmation') != request.form.get('new_pass'):
            return apology('Please enter the same new password')

        pass_hash = generate_password_hash(request.form.get("new_pass"))
        db.execute('UPDATE users SET hash = ? WHERE id = ?', pass_hash, session['user_id'])

        return redirect('/')

    else:
        return render_template('pass.html')


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
