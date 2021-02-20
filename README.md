# Ceibapp 
## What is?
Ceibapp is an small business oriented inventory managment web application. 
The name cames from one of my favourite trees, *Ceiba Speciosa*, a beautiful local specimen from Argentina.
## Why?
Ceibapp was designed as a solution for a local furniture factory which despite a long tradition in the business it didnt have a digital tool for managing their sales and inventory materials.
## How?
Ceibapp was developed as a final project for the **CS50's Introduction to Computer Science** course. [https://learning.edx.org/course/course-v1:HarvardX+CS50+X/home]
The main goal for this final step was to apply as many concepts learned trough the course as possible, such as:

	 - CS50 ide: software development, debbuging, server running.
	 - Flask, jinja: web application development.
	 - Sqlite, DB Browser, PhpLiteAdmin: database creating, editing and testing.
	 - Python: main language used to run the web app.
	 - Html, CSS: web pages layouts designing and styling.
	 - Javascript: special features manipulating the DOM.
# Using the app
This application has several functions conceived to facilitate repetitive daily tasks and allows you to keep track of: furniture sales, material purchases and other inventory movements.
We will detail each of them below.
## Register
Before start using Ceibapp you must create a new user account and provide a password in order to access in the future. Without an account, you wont be able to work on the app.
### Underneath the hood
In **application.py**, we import generate_password_hash from werkzeug.

Werkzeug is a comprehensive **WSGI** web application library. It began as a simple collection of various utilities for WSGI applications and has become one of the most advanced WSGI utility libraries.

The Web Server Gateway Interface (**WSGI**, pronounced *whiskey*) is a simple calling convention for web servers to forward requests to web applications or frameworks written in the Python programming language.

**generate_password_hash**: Hash a password with the given method and salt with a string of the given length. The format of the string returned includes the method that was used so that check_password_hash() can check the hash.
 
werkzeug.security.**generate_password_hash**(*password, method='pbkdf2:sha256', salt_length=8*)


## Login
Now that you have an account, provide your username and password and finally! You are welcome to begin working with Ceibapp.

### Underneath the hood
In **application.py**, we import **check_password_hash** from werkzeug.

**check_password_hash**: check a password against a given salted and hashed password value. In order to support unsalted legacy passwords this method supports plain text passwords, md5 and sha1 hashes (both salted and unsalted).
Returns  True  if the password matched,  False  otherwise.

Function declaration:
werkzeug.security.**check_password_hash**(*pwhash, password*)

When the user click the "Log in" button, **login** function in application.py takes the username and password and performs a control check.
First, we query the database searching for that username. If we dont get any result, the username dont exist and a error message is displayed.
Then, we check password with the mentioned **check_password_hash** function. If we get false as a result, a error message is displayed.

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



## Sales
  
With this function, you can record each sale made while detailing important data such as: furniture model, customer name, units sold and transaction date. 
In addition, when registering a sale, the app will discount each component of said furniture from the materials in stock. 
You must complete each form field in order to complete the registering. If any field is empty, a error message will be displayed.

### Underneath the hood
Accesing to ***index.html*** via GET request, renders a page where the user can select every furniture model manufactured. This feature is achieved using ***HTML datalist tag*** so the user can eather select the desired model by searching it trough the list or just type some keywords in order to reduce the list lenght.

                  <form action="/" method="post">
                    <div class="form-group">
                        <label for="model1">Choose furniture model</label>
                        <input id="model1" type="text" name="model" list="exampleList" autocomplete="off" autofocus class="form-control">
                        <datalist id="exampleList">
                            {% for mod in models %}
                            <option value="{{ mod.model }}">{{ mod.model }}</option>
                            {% endfor%}
                        </datalist>
                    </div>
In **application.py** the furniture models list is queried from database´s ***furniture table*** and passed to ***index.html*** by Flasks method **render_template()**. 

        else:    
            models = db.execute("SELECT * FROM furniture")
        return render_template("index.html", models=models)
 
 By the other hand, once the user submit the completed forms it generates a POST request method and all this information is stored as variables in **application.py**.
 

        model = request.form.get("model")
        client = request.form.get("client")
        sales = request.form.get("sales")
        date = request.form.get("date")
        clientType = request.form.get("clientType")
        descript = request.form.get("descript")
        meas = request.form.get("meas")

## Inventory
### Underneath the hood

## Movements
### Underneath the hood

## Record
### Underneath the hood
