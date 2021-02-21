import os

from cs50 import SQL

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

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
db = SQL("sqlite:///giuntas.db")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    if request.method == "POST":

        model = request.form.get("model")
        client = request.form.get("client")
        sales = request.form.get("sales")
        date = request.form.get("date")
        clientType = request.form.get("clientType")
        descript = request.form.get("descript")
        meas = request.form.get("meas")

        if not model:
            return render_template("error.html", message="Missing furniture model")

        if not client:
            return render_template("error.html", message="Missing client´s name")

        if not sales:
            return render_template("error.html", message="Missing N° of sales")

        if not date:
            return render_template("error.html", message="Missing sales date")

        if not clientType:
            return render_template("error.html", message="Missing sales Client Type")

        sales = int(sales)
        
        furniture = db.execute("SELECT id,model FROM furniture WHERE model = ?", model)

        fabrication = db.execute("SELECT name, fabrication.qty, fabrication.unit FROM fabrication INNER JOIN stock on stock.id = fabrication.supply_id WHERE model_id = ?", furniture[0]['id'])

        for row in fabrication:
            row["sales"] = row["qty"] * sales

        return render_template("sell.html", fabrication=fabrication,furniture=furniture,client=client,sales=sales,date=date,clientType=clientType,descript=descript,meas=meas)

    else:

        models = db.execute("SELECT * FROM furniture")

        return render_template("index.html", models=models)


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():

    if request.method == "POST":

        model = request.form.get("model")
        client = request.form.get("client")
        sales = int(request.form.get("sales"))
        date = request.form.get("date")
        clientType = request.form.get("clientType")
        descript = request.form.get("descript")
        meas = request.form.get("meas")
        motive = "Sale"

        # Select furniture components
        id_model = db.execute("SELECT id FROM furniture WHERE model = ?", model)
        fabrication = db.execute("SELECT supply_id, qty, unit FROM fabrication WHERE model_id = ?", id_model[0]["id"])

        for row in fabrication:

            row["sales"] = row["qty"] * sales

            stock = db.execute("SELECT name,qty FROM stock WHERE id = ?", row["supply_id"])

            discVal = stock[0]["qty"] - row["sales"]

            # Update stock qty value
            db.execute("UPDATE stock SET qty = ? WHERE id = ?", discVal, row["supply_id"])

            # Update regStock table with new sale
            db.execute("INSERT INTO regStock (motive,destination,item,qty,date) VALUES (?,?,?,?,?)", motive, client, stock[0]["name"], row["sales"],date)

        db.execute("INSERT INTO sell (client,clientType,model,sell_qty,date,descript,meas) VALUES (?,?,?,?,?,?,?)", client, clientType, model, sales, date, descript, meas)

        return redirect("/confirm")


@app.route("/confirm", methods=["GET", "POST"])
@login_required
def confirm():

    if request.method == "GET":

        stock = db.execute("SELECT * FROM sell")

        return render_template("confirm.html",stock=stock)


@app.route("/stock", methods=["GET", "POST"])
@login_required
def stock():

    if request.method == "GET":

        stock = db.execute("SELECT * FROM stock")

        return render_template("stock.html",stock=stock)


@app.route("/movements", methods=["GET", "POST"])
@login_required
def movements():

    option = ["Sale","Purchase","Milestone","Adjust","Supplier"]
    
    if request.method == "POST":
        
        # Get user data from request form
        motive = request.form.get("motive")
        
        stock = db.execute("SELECT * FROM regStock WHERE motive = ?", motive)
        
        return render_template("movements.html",stock=stock,option=option)
        
    
    if request.method == "GET":
        
        stock = db.execute("SELECT * FROM regStock")

        return render_template("movements.html",stock=stock,option=option)



@app.route("/register", methods=["GET", "POST"])
@login_required
def register():

    if request.method == "POST":

        # Get user data from request form
        motive = request.form.get("motive")
        destination = request.form.get("destination")
        user_qty = request.form.get("qty")
        date = request.form.get("date")
        item = request.form.get("item")
        item2 = request.form.get("supItem")

        # Check user inputs
        if not motive:
            return render_template("error.html", message="Missing registration MOTIVE")

        if not destination:
            return render_template("error.html", message="Missing registration DESTINATION")

        if not user_qty:
            return render_template("error.html", message="Missing registration QTY")

        if not date:
            return render_template("error.html", message="Missing registration DATE")

        user_qty = int(user_qty)

        if user_qty < 0:
            return render_template("error.html", message="Registration item QTY cannot be NEGATIVE")

        # If MILESTONE selected, just insert data to regStock
        if motive == "Milestone":

            if user_qty != 0:
                return render_template("error.html", message="By selecting Milestone, qty must be 0 (zero)")

            if item != "-":
                return render_template("error.html", message="By selecting Milestone, item must be -")

            # Insert MILESTONE user data
            db.execute("INSERT INTO regStock (motive,destination,item,qty,date) VALUES (?,?,?,?,?)", motive, destination, item, user_qty, date)

            return redirect("/movements")

        # Else, with any other selection substract qty from stock
        else:
            # If not a special material, do this
            if item != None:

                # Select item qty in stock
                stock = db.execute("SELECT qty FROM stock WHERE name = ?", item)

                # Default value if Adjust is chosen
                updateVal = user_qty

                # If this option, do an addition
                if motive == "Purchase":

                    updateVal = stock[0]["qty"] + user_qty

                # Else if this option, do a substraction
                elif motive == "Supplier":

                    updateVal = stock[0]["qty"] - user_qty

                # Update stock qty value
                db.execute("UPDATE stock SET qty = ? WHERE name = ?", updateVal, item)

                # Insert inventory movement in regStock
                db.execute("INSERT INTO regStock (motive,destination,item,qty,date) VALUES (?,?,?,?,?)", motive, destination, item, user_qty, date)

            # Else just insert special item
            else:

                # Insert inventory movement in regStock
                db.execute("INSERT INTO regStock (motive,destination,item,qty,date) VALUES (?,?,?,?,?)", motive, destination, item2, user_qty, date)

            # Return to display page
            return redirect("/movements")

    if request.method == "GET":

        option = ["Purchase","Milestone","Adjust","Supplier"]

        stock = db.execute("SELECT name FROM stock")

        return render_template("register.html",stock=stock,option=option)


@app.route("/reguser", methods=["GET", "POST"])
def reguser():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        """Register user"""
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("error.html", message="Must provide a username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("error.html", message="Must provide a password")

        # Ensure password was confirmed
        elif not request.form.get("confirmation"):
            return render_template("error.html", message="Must provide confirmation password")

        elif request.form.get("password") != request.form.get("confirmation"):
            return render_template("error.html", message="Password confirmation doesnt match")

        # Generate hash of the password
        hashvalue = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
        username = request.form.get("username")
        t = (username, hashvalue)
        # Check if there any user with that name
        userDict = db.execute("SELECT * FROM users WHERE username = ?", t[0])

        if not userDict:
            # New username, Insert new user data
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", t[0], t[1])
            return redirect("/")

        else:
            return render_template("error.html", message="User already exist")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("reguser.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("error.html", message="Must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("error.html", message="Must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("error.html", message="Check username or password")

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