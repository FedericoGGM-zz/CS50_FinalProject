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
With this variables we can query the selected furniture model from ***DB furniture table*** , the manufacturing components from ***DB fabrication table*** and pass this information to ***sell.html***.

        furniture = db.execute("SELECT id,model FROM furniture WHERE model = ?", model)
        fabrication = db.execute("SELECT name, fabrication.qty, fabrication.unit FROM fabrication INNER JOIN stock on stock.id = fabrication.supply_id WHERE model_id = ?", furniture[0]['id'])

        for row in fabrication:
            row["sales"] = row["qty"] * sales

        return render_template("sell.html", fabrication=fabrication,furniture=furniture,client=client,sales=sales,date=date,clientType=clientType,descript=descript,meas=meas)

***sell.html*** is an intermediate page where all the sale data is shown in two tables so the user can check if everything is ok. When clicking the submit button,  **sell()** function performs an update of ***DB tables stock, regStock and sell***. 

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

Finally, at the end of the function we are redirected to ***confirm.html*** where ***DB sell table*** is displayed.
## Inventory
In this special feature, the user can check the actual state of the materials inventory. The information is displayed in a three column table: *name of material, quantity and unit*.
In order to prevent inventory shortage, each material has an specific "alert value" predefined in the database. So, if after a sale registering discount the new value is minor than the alert, the actual row will change it color to yellow.
By the other hand, if the new value after a sale discount is minor to zero the row color will change to red.

### Underneath the hood
In **application.py**, ***stock()*** function query the ***DB stock table*** and pass it to ***stock.html*** by Flasks method **render_template()**. 

	    @app.route("/stock", methods=["GET", "POST"])
		@login_required
		def stock():

	    if request.method == "GET":
		stock = db.execute("SELECT * FROM stock")
		return render_template("stock.html",stock=stock)
  
In ***stock.html***, we apply Jinja syntax to display all the inventory materials as a HTML table.
  
	<table id="myTable" class="table table-hover table-bordered table-striped">
	<thead class="thead-dark">
	    <tr>
		<th>Name</th>
		<th>Quantity</th>
		<th>Unit</th>
	    </tr>
	</thead>
	<tbody>
	    {% for row in stock%}
	    <tr id="myRow">
		<td>{{ row.name }}</td>
		<td id="qtyCell">{{ row.qty }}</td>
		<td>{{ row.unit }}</td>
		<td style="display:none;">{{ row.alert }}</td>
	    </tr>
	    {% endfor %}
	</tbody>
    </table>

For the changing color rows feature a javascript code is used. It checks every row value with the ***getElementById()*** method and with an if statement control it change the ***backgroundColor*** property.
        
	<script>
            // Get total number of rows in table
            var x = document.getElementById("myTable").rows.length;
            var i;
            // Iterate every row
            for (i = 1; i < x; i++) {
                // Get Qty cell as object
                var c = document.getElementById("myTable").rows[i].cells[1];
                // Get qty cell value as text
                var cellQty = document.getElementById("myTable").rows[i].cells[1].innerText;
                // Get alert cell value as text
                var cellAlert = document.getElementById("myTable").rows[i].cells[3].innerText;
                // Convert Qty cell value into float
                var floatQty = parseFloat(cellQty);
                // Convert Alert cell value into float
                var floatAlert = parseFloat(cellAlert);
                // Paint yellow every value minor than alert value
                if (floatQty <= floatAlert && floatQty >= 0) {
                    c.style.backgroundColor = "yellow";
                }
                // Paint red every value minor than zero
                if (floatQty < 0) {
                    c.style.backgroundColor = "lightcoral";
                }
            }
        </script>
    



## Movements
### Underneath the hood

## Record
### Underneath the hood
