import sqlite3
import config
import uuid
import users
import workouts
import secrets

from flask import Flask
from flask import redirect, render_template, request, flash, abort
from flask import session

from datetime import datetime, timedelta


app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)


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
        
        user_id = users.check_login(username, password)

        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            flash("ERROR: Username or password not recognized")
            return redirect("/login")




@app.route("/register.html")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():

    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        flash("ERROR: The passwords don't match")        
        return render_template("register.html")
    
    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("ERROR: User name already in use")        
        return render_template("register.html")

    flash("User registration succesful")
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
            
        


    flash("Workout added succesfully")

    return render_template("workouts.html", sports=sports, sport_type=sport_type,
                           exercises = exercises, purposes=purposes, sport_id=sport_id, 
                           number_of_exercises=number_of_exercises, exercise_details=exercise_details)



@app.route("/user/<int:user_id>")
def show_user(user_id):

    user = users.fetch_userdata(user_id)[0]
    if not user:
        abort(404)
    
    most_common_sport = users.fetch_most_common_sport(user_id)[0]
    most_common_exercise = users.fetch_most_common_exercise(user_id)[0]

    user_workouts = users.fetch_user_workouts(user_id)
    
    return render_template("user_page.html", user=user, user_workouts=user_workouts,
                           most_common_sport=most_common_sport, 
                           most_common_exercise=most_common_exercise)



@app.route("/workouts/<workout_id>")
def show_workout(workout_id):


    workout_data = workouts.fetch_workout_data(workout_id)
    workout_sport = workout_data[0][0]
    workout_user = workout_data[0][1]
    workout_comment = workout_data[0][2]
    workout_begin_time = workout_data[0][3]
    workout_end_time = workout_data[0][4]

    return render_template("workout_page.html", workout_data=workout_data, workout_sport=workout_sport,
                           workout_user=workout_user, workout_comment=workout_comment, workout_begin_time=workout_begin_time,
                           workout_end_time=workout_end_time)


@app.route("/find_workout")
def find_workout():
    query = request.args.get("query", "").strip()
    results = []

    if query:
        results = workouts.search_workouts(query)

    return render_template("find_workout.html", query=query, results=results)



@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("username", None)

    return redirect("/")
