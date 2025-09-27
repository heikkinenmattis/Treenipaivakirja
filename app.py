import sqlite3
import config
import db
import utils
import items
import time
import uuid

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

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    date_of_birth = request.form["date_of_birth"]
    weight = request.form["weight"]
    height = request.form["height"]
    max_heart_rate = request.form["max_heart_rate"]
    ftp_cycling = request.form["ftp_cycling"]

    # fav_sport yet to come from a dropdown
    # city yet to come from a dropdown

    items.add_userdata(username = session_username, first_name = first_name, 
                       last_name = last_name, date_of_birth = date_of_birth, 
                       weight = weight, height = height, 
                       max_heart_rate = max_heart_rate, ftp_cycling = ftp_cycling)

    flash("Käyttäjädata päivitetty")        
    return redirect("/")


@app.route("/workouts.html")
def workouts():
    sports = items.fetch_sports()
    return render_template("workouts.html", sports=sports)
    

@app.route("/add_workout", methods=["POST"])
def add_workout():

    # Keep the form this way. Don't fetch the sport from db. 
    # It can be fixed later. This can be quick and dirty for now.
    # Fetch the exercises for the sport and try to make that small bit work. This is fairly easy.

        
    sports = items.fetch_sports()
    workout_id = str(uuid.uuid4())
    sport_id = int(request.form["sport"])
    sport_type = items.fetch_sport_type(sport_id)[0][0]
    exercises = items.fetch_exercises(sport_id)
    purposes = items.fetch_purposes(sport_type)
    

    begin_time = request.form["begin_time"]
    end_time = request.form["end_time"]
    comments = request.form["comments"]
    user_id = session["user_id"]

    # print(f"comments: {comments}, begin_time: {begin_time}, end_time: {end_time}, user_id = {user_id}, sport_id: {sport_id}, workout_id: {workout_id}")

    items.insert_workout(workout_id = workout_id, user_id = user_id, sport_id = sport_id, 
                         begin_time=begin_time, end_time=end_time, comments=comments)

    flash("Suoritus päivitetty")
    #return redirect("/")
    return render_template("workouts.html", exercises = exercises, sport_type = sport_type, 
                           sport_id = sport_id, sports=sports, purposes=purposes)

@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]

    return redirect("/")
