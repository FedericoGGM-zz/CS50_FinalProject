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



## Sales
### Underneath the hood

## Inventory
### Underneath the hood

## Movements
### Underneath the hood

## Record
### Underneath the hood
