import sqlite3
import config
import db
import utils
import items
import time

from flask import Flask
from flask import redirect, render_template, request, flash
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        
        sql = "SELECT password_hash FROM users WHERE username = ?"
        password_hash = db.query(sql, [username])[0][0]

        if check_password_hash(password_hash, password):
            
            sql = "SELECT id FROM users WHERE username = ?"
            user_id = db.query(sql, [username])[0][0]

            session["username"] = username
            session["user_id"] = user_id       

            return redirect("/")
        else:
            flash("VIRHE: väärä tunnus tai salasana")
            return redirect("/")


@app.route("/register.html")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():

    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        flash("VIRHE: Salasanat eivät ole samat")        
        return render_template("index.html")
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        flash("VIRHE: tunnus on jo varattu")        
        return render_template("index.html")

    flash("Tunnus luotu")
    return render_template("index.html")


@app.route("/user_attributes.html")
def user_attributes():
    # To prefill forms, let's fetch existing user data first.
    user_id = session["user_id"]
    username = session["username"]
    userdata = items.fetch_userdata(user_id)[0]

    return render_template("user_attributes.html", userdata=userdata)

@app.route("/add_user_data", methods=["POST"])
def add_user_data():

    # Fetch user name. It is unique so it can be used in the building phase.
    session_username = session["username"]

    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    dateofbirth = request.form["dateofbirth"]
    weight = request.form["weight"]
    height = request.form["height"]
    max_heart_rate = request.form["maxhr"]
    ftp_cycling = request.form["ftp"]

    # fav_sport tulee dropdownista
    # gender tulee dropdownista
    # city tulee dropdownista

    items.add_userdata(username = session_username, firstname = firstname, 
                       lastname = lastname, dateofbirth = dateofbirth, 
                       weight = weight, height = height, 
                       max_heart_rate = max_heart_rate, ftp_cycling = ftp_cycling)

    flash("Käyttäjädata päivitetty")        
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]

    return redirect("/")
