import sqlite3
import config
import db
import utils
import time
import uuid
import users
import workouts

from flask import Flask
from flask import redirect, render_template, request, flash
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    all_workouts = workouts.get_workouts()
    return render_template("index.html", workouts=all_workouts)

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
    
    #Using pbkdf2 for developement due to working on Macbook.
    password_hash = generate_password_hash(password1, method='pbkdf2')

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
    userdata = users.fetch_userdata(user_id)[0]

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

    users.add_userdata(username = session_username, first_name = first_name, 
                       last_name = last_name, date_of_birth = date_of_birth, 
                       weight = weight, height = height, 
                       max_heart_rate = max_heart_rate, ftp_cycling = ftp_cycling)

    flash("Käyttäjädata päivitetty")        
    return redirect("/")


@app.route("/workouts.html")
def workouts_page():
    sports = workouts.fetch_sports()
    return render_template("workouts.html", sports=sports, number_of_exercises=1, exercise_details={})

sport_id = 1
#Tämä näyttäis toimivan
@app.route("/confirm_sport", methods=["POST"])
def confirm_sport():
    sports = workouts.fetch_sports()
    
    global sport_id

    sport_id = int(request.form["sport"])
    
    sport_type = workouts.fetch_sport_type(sport_id)[0][0]
    exercises = workouts.fetch_exercises(sport_id)
    purposes = workouts.fetch_purposes(sport_type)


    return render_template("workouts.html", sports=sports, sport_type=sport_type,
                           exercises = exercises, purposes=purposes, sport_id=sport_id, 
                           number_of_exercises=1, exercise_details={})


# Toimii, kun sport_id on globaalina muuttujana. Seuraavaksi
# pitää tehdä sellainen jeccu, että muuttujat html-formilla on nimiluokkaa
# sets_1, sets_2, sets_3 jne, jotta ne voi syöttää takaisin. Lisäksi tuo number of
# exercises pitää palauttaa ykköseen heti kun workout on postattu.

# Muutetaan tämä niin, että alustetaan tyhjä exercise_details kenttineen, joka työnnetään
# html formille. Näin ei tarvitsisi joka kerta käydä formilta katsomassa, onko sanakirjassa tavaraa.
# Lisätietoja esimerkiksi Obsidianista.

number_of_exercises = 1
exercise_details = {}

@app.route("/add_row", methods=["POST"])
def add_row():

    global number_of_exercises
    global sport_id
    global exercise_details

    sports = workouts.fetch_sports()
    sport_type = workouts.fetch_sport_type(sport_id)[0][0]
    exercises = workouts.fetch_exercises(sport_id)
    purposes = workouts.fetch_purposes(sport_type)


    for i in range(0,number_of_exercises):
        print(f"entered for loop for EVERYTHING, iteration round{i}")
        exercise_details[i] = {}
        
        exercise_details[i]["exercise_id"] = int(request.form[f"exercise_{i}"])
        exercise_details[i]["purpose_id"] = int(request.form[f"purpose_{i}"])

        if sport_type == "Endurance":
            exercise_details[i]["minutes"] = request.form[f"minutes_{i}"]
            exercise_details[i]["avghr"] = request.form[f"avghr_{i}"]
            exercise_details[i]["kilometers"] = request.form[f"kilometers_{i}"]

        if sport_type == "Strength":
            exercise_details[i]["sets"] = request.form[f"sets_{i}"]
            exercise_details[i]["reps"] = request.form[f"reps_{i}"]
            exercise_details[i]["weight"] = request.form[f"weight_{i}"]

    print(exercise_details)

    number_of_exercises += 1


    return render_template("workouts.html", sports=sports, sport_type=sport_type,
                           exercises = exercises, purposes=purposes, sport_id=sport_id, 
                           number_of_exercises=number_of_exercises, exercise_details=exercise_details)


 
@app.route("/add_workout", methods=["POST"])
def add_workout():

    global number_of_exercises
    global sport_id
    global exercise_details

    #nämä muuttujat eivät ole tällä formilla.
    print("entered add workout function")    
    sports = workouts.fetch_sports()
    workout_id = str(uuid.uuid4())
    # sport_id = int(request.form["sport"])
    sport_type = workouts.fetch_sport_type(sport_id)[0][0]
    exercises = workouts.fetch_exercises(sport_id)
    purposes = workouts.fetch_purposes(sport_type)

    print("managed to fetch stuff but not times")    

    begin_time = request.form["begin_time"]
    end_time = request.form["end_time"]
    comments = request.form["comments"]
    user_id = session["user_id"]

    #Tähän tulee joku for-looppi, jossa käydään hakemassa exercise_detailsista 
    for _, exercise in exercise_details.items():


        if sport_type == "Endurance":
            print("entered endurance")
            workouts.insert_workout(workout_id = workout_id, user_id = user_id, sport_id = sport_id, 
                                begin_time=begin_time, end_time=end_time, comments=comments,
                                exercise_id = exercise["exercise_id"], purpose_id = exercise["purpose_id"],
                                minutes=exercise["minutes"], avghr = exercise["avghr"], 
                                kilometers = exercise["kilometers"], sets=None, reps=None, weight=None)


        if sport_type == "Strength":
            print("entered strength")
            workouts.insert_workout(workout_id = workout_id, user_id = user_id, sport_id = sport_id, 
                                begin_time=begin_time, end_time=end_time, comments=comments,
                                exercise_id = exercise["exercise_id"], purpose_id = exercise["purpose_id"],
                                sets=exercise["sets"], reps = exercise["reps"], weight = exercise["weight"],
                                minutes=None, avghr=None, kilometers=None)
            
        


    flash("Suoritus päivitetty")
    # return redirect("/")
    return render_template("workouts.html", sports=sports, sport_type=sport_type,
                           exercises = exercises, purposes=purposes, sport_id=sport_id, 
                           number_of_exercises=number_of_exercises, exercise_details=exercise_details)


@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]

    return redirect("/")
