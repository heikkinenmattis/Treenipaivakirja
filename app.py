import sqlite3
import secrets
import uuid
import re

from datetime import datetime
from flask import Flask
from flask import redirect, render_template, request, flash, abort
from flask import session

import config
import users
import workouts

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

    if len(username) < 4 or len(username) > 20:
        flash("ERROR: Username must be at least four characters long")
        return render_template("register.html")

    if not username or not password1 or not password2:
        flash("ERROR: Username or password not entered")
        return render_template("register.html")

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
    require_login()

    user_id = session["user_id"]
    userdata = users.fetch_userdata(user_id)[0]
    sports = workouts.fetch_sports()
    cities = users.fetch_cities()

    return render_template("user_attributes.html", userdata=userdata,
                           sports=sports, cities=cities)

@app.route("/add_user_data", methods=["POST"])
def add_user_data():
    require_login()
    check_csrf()

    session_username = session["username"]
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    date_of_birth = request.form["date_of_birth"]
    weight = request.form["weight"]
    height = request.form["height"]
    max_heart_rate = request.form["max_heart_rate"]
    ftp_cycling = request.form["ftp_cycling"]
    fav_sport = int(request.form["fav_sport"])
    city = int(request.form["user_city"])

    if len(first_name) < 2 or len(first_name) > 20:
        flash("ERROR: First name too short or too long.")
        return redirect("/user_attributes.html")

    if len(last_name) < 2 or len(last_name) > 40:
        flash("ERROR: Last name too short or too long.")
        return redirect("/user_attributes.html")

    if not re.search("^(19|20)\d{2}$", date_of_birth):
        flash("ERROR: Suspicious birth date.")
        return redirect("/user_attributes.html")

    if weight < 30 or weight > 300:
        flash("ERROR: Suspicious weight.")
        return redirect("/user_attributes.html")

    if height < 100 or height > 235:
        flash("ERROR: Suspicious weight.")
        return redirect("/user_attributes.html")

    if max_heart_rate < 30 or max_heart_rate > 230:
        flash("ERROR: Suspicious maximum heart rate.")
        return redirect("/user_attributes.html")

    if ftp_cycling < 50 or ftp_cycling > 500:
        flash("ERROR: Suspicious FTP.")
        return redirect("/user_attributes.html")

    users.add_userdata(username=session_username,
                       first_name=first_name,
                       last_name=last_name,
                       date_of_birth=date_of_birth,
                       weight=weight,
                       height=height,
                       max_heart_rate=max_heart_rate,
                       ftp_cycling=ftp_cycling,
                       fav_sport=fav_sport,
                       city=city)

    flash("User data updated succesfully")
    return redirect("/")


@app.route("/workouts.html")
def workouts_page():
    require_login()

    session.pop("sport_id", None)
    session.pop("exercise_details", None)
    session.pop("number_of_exercises", None)

    session["sport_id"] = 1
    session["number_of_exercises"] = 0
    session["exercise_details"] = {}

    sports = workouts.fetch_sports()
    return render_template("workouts.html",
                           sports=sports,
                           number_of_exercises=session["number_of_exercises"],
                           exercise_details=session["exercise_details"])


@app.route("/confirm_sport", methods=["POST"])
def confirm_sport():
    require_login()
    check_csrf()

    sports = workouts.fetch_sports()
    session["sport_id"] = int(request.form["sport"])
    details = session.get("exercise_details", {})
    n = session.get("number_of_exercises", 0)

    sport_type = workouts.fetch_sport_type(session["sport_id"])[0][0]
    exercises = workouts.fetch_exercises(session["sport_id"])
    purposes = workouts.fetch_purposes(sport_type)

    flash("Sport confirmed succesfully")
    return render_template("workouts.html",
                           sports=sports,
                           sport_type=sport_type,
                           exercises=exercises,
                           purposes=purposes,
                           sport_id=session["sport_id"],
                           number_of_exercises=n,
                           exercise_details=details)



@app.route("/add_workout", methods=["POST"])
def add_workout():

    action = request.form["button_action"]
    require_login()
    check_csrf()

    spid = session.get("sport_id", 1)
    sports = workouts.fetch_sports()
    sport_type = workouts.fetch_sport_type(spid)[0][0]
    exercises = workouts.fetch_exercises(spid)
    purposes = workouts.fetch_purposes(sport_type)

    details = session.get("exercise_details", {})
    n = session.get("number_of_exercises", 0)

    for i in range(0,n):
        key = str(i)
        details[key] = {}

        details[key]["exercise_id"] = int(request.form[f"exercise_{i}"])
        details[key]["purpose_id"] = int(request.form[f"purpose_{i}"])

        if sport_type == "Endurance":
            details[key]["minutes"] = request.form[f"minutes_{i}"]
            details[key]["avghr"] = request.form[f"avghr_{i}"]
            details[key]["kilometers"] = request.form[f"kilometers_{i}"]

        if sport_type == "Strength":
            details[key]["sets"] = request.form[f"sets_{i}"]
            details[key]["reps"] = request.form[f"reps_{i}"]
            details[key]["weight"] = request.form[f"weight_{i}"]

    begin_time = request.form["begin_time"]
    end_time = request.form["end_time"]
    comments = request.form["comments"]
    user_id = session["user_id"]


    if action == "add_exercise":

        session["exercise_details"] = details
        n += 1
        session["number_of_exercises"] = n

        return render_template("workouts.html",
                                sports=sports,
                                sport_type=sport_type,
                                exercises=exercises,
                                purposes=purposes,
                                sport_id=spid,
                                number_of_exercises=n,
                                exercise_details=details,
                                begin_time=begin_time,
                                end_time=end_time,
                                athlete_comment=comments)

    if action == "save_workout":
        workout_id = str(uuid.uuid4())
        if not details:
            flash("Cannot save workout without exercises. Please enter exercises.")

            return render_template("workouts.html",
                                    sports=sports,
                                    sport_type=sport_type,
                                    exercises=exercises,
                                    purposes=purposes,
                                    sport_id=spid,
                                    number_of_exercises=n,
                                    exercise_details=details)

        if not begin_time or not end_time:
            flash("ERROR: Cannot save a workout without begin time or end time")
            return render_template("workouts.html",
                                sports=sports,
                                sport_type=sport_type,
                                exercises=exercises,
                                purposes=purposes,
                                sport_id=spid,
                                number_of_exercises=n,
                                exercise_details=details)         

        compare_begintime = datetime.strptime(begin_time, "%Y-%m-%dT%H:%M")
        compare_endtime = datetime.strptime(end_time, "%Y-%m-%dT%H:%M")
        if compare_begintime > compare_endtime:
            flash("ERROR: Cannot save a workout with begin time after end time")
            return render_template("workouts.html",
                                    sports=sports,
                                    sport_type=sport_type,
                                    exercises=exercises,
                                    purposes=purposes,
                                    sport_id=spid,
                                    number_of_exercises=n,
                                    exercise_details=details)

        if len(comments) > 4000:
            flash("ERROR: Comment too long. Maximum length is 4000 characters.")
            return render_template("workouts.html",
                        sports=sports,
                        sport_type=sport_type,
                        exercises=exercises,
                        purposes=purposes,
                        sport_id=spid,
                        number_of_exercises=n,
                        exercise_details=details)

        for _, exercise in details.items():

            if sport_type == "Endurance":

                if not exercise["kilometers"] or not exercise["minutes"] or not exercise["avghr"]:
                    flash("ERROR: Workout information missing. An endurance exercise must \n"
                            "contain kilometers, minutes and average heart rate.")

                    return render_template("workouts.html",
                                sports=sports,
                                sport_type=sport_type,
                                exercises=exercises,
                                purposes=purposes,
                                sport_id=spid,
                                number_of_exercises=n,
                                exercise_details=details)

                workouts.insert_workout(workout_id=workout_id,
                                        user_id=user_id,
                                        sport_id=spid,
                                        begin_time=begin_time,
                                        end_time=end_time,
                                        comments=comments,
                                        exercise_id=exercise["exercise_id"],
                                        purpose_id=exercise["purpose_id"],
                                        minutes=exercise["minutes"],
                                        avghr=exercise["avghr"],
                                        kilometers=exercise["kilometers"],
                                        sets=None,
                                        reps=None,
                                        weight=None)

            if sport_type == "Strength":

                if not exercise["sets"] or not exercise["reps"]:
                    flash("ERROR: Workout information missing. A strength exercise must \n"
                            "contain sets and reps. An empty value is allowed in weights.")

                    return render_template("workouts.html",
                        sports=sports,
                        sport_type=sport_type,
                        exercises=exercises,
                        purposes=purposes,
                        sport_id=spid,
                        number_of_exercises=n,
                        exercise_details=details)

                workouts.insert_workout(workout_id=workout_id,
                                        user_id=user_id,
                                        sport_id=spid,
                                        begin_time=begin_time,
                                        end_time=end_time,
                                        comments=comments,
                                        exercise_id=exercise["exercise_id"],
                                        purpose_id=exercise["purpose_id"],
                                        sets=exercise["sets"],
                                        reps=exercise["reps"],
                                        weight=exercise["weight"],
                                        minutes=None,
                                        avghr=None,
                                        kilometers=None)

        flash("Workout added succesfully")
        session.pop("sport_id", None)
        session.pop("exercise_details", None)
        session.pop("number_of_exercises", None)

        return render_template("workouts.html",
                                sports=sports,
                                sport_type=sport_type,
                                exercises=exercises,
                                purposes=purposes,
                                sport_id=spid,
                                number_of_exercises=n,
                                exercise_details=details)




@app.route("/reset_workout", methods=["POST"])
def reset_workout():
    return workouts_page()


@app.route("/user/<int:user_id>")
def show_user(user_id):

    user = users.fetch_userdata(user_id)[0]
    if not user:
        abort(404)

    most_common_sport = users.fetch_most_common_sport(user_id)[0]
    most_common_exercise = users.fetch_most_common_exercise(user_id)[0]

    user_workouts = users.fetch_user_workouts(user_id)
    return render_template("user_page.html",
                           user=user,
                           user_workouts=user_workouts,
                           most_common_sport=most_common_sport,
                           most_common_exercise=most_common_exercise)



@app.route("/workouts/<workout_id>")
def show_workout(workout_id):

    require_login()

    workout_data = workouts.fetch_workout_data(workout_id)
    workout_sport = workout_data[0][0]
    workout_user = workout_data[0][1]
    workout_comment = workout_data[0][2]
    workout_begin_time = workout_data[0][3]
    workout_end_time = workout_data[0][4]
    workout_user_id = workout_data[0][14]
    workout_sport_id = workout_data[0][16]

    previous_comments = workouts.fetch_comments(workout_id)

    return render_template("workout_page.html",
                            workout_data=workout_data,
                            workout_sport=workout_sport,
                            workout_user=workout_user,
                            workout_comment=workout_comment,
                            workout_begin_time=workout_begin_time,
                            workout_end_time=workout_end_time,
                            workout_id=workout_id,
                            previous_comments=previous_comments,
                            workout_user_id=workout_user_id,
                            workout_sport_id=workout_sport_id)


@app.route("/add_comment", methods=["POST"])
def add_comment():

    require_login()
    check_csrf()

    workout_id = request.form["workout_id"]
    comment_content = request.form["comment_content"]
    comment_timestamp = str(datetime.now())

    if len(comment_content) > 4000:
        flash("Comment too long. Maximum length is 4000 characters")
        return show_workout(workout_id=workout_id)

    workouts.comment_workout(user_id=session["user_id"],
                             workout_id=workout_id,
                             timestamp=comment_timestamp,
                             content=comment_content)

    flash("Comment added succesfully")

    return show_workout(workout_id=workout_id)


@app.route("/find_workout")
def find_workout():

    require_login()

    query = request.args.get("query", "").strip()
    results = []

    if query:
        results = workouts.search_workouts(query)

    return render_template("find_workout.html",
                           query=query,
                           results=results)


@app.route("/delete_workout", methods=["POST"])
def delete_workout():

    require_login()
    check_csrf()

    workout_id = request.form["workout_id"]
    source_page = request.form["source_page"]

    if source_page == "user_page.html":
        user_id = request.form["user_id"]
        workouts.delete_workout(workout_id)
        return show_user(user_id=user_id)

    if source_page == "workout_page.html":
        workouts.delete_workout(workout_id)
        return redirect("/")


@app.route("/edit_workout", methods=["POST"])
def edit_workout():

    require_login()
    check_csrf()

    workout_id = request.form["workout_id"]
    sport_id = request.form["sport_id"]
    source_page = request.form["source_page"]

    sport_type = workouts.fetch_sport_type(sport_id)[0][0]
    purposes = workouts.fetch_purposes(sport_type)
    exercises = workouts.fetch_exercises(sport_id)

    workout_data = workouts.fetch_workout_data(workout_id)
    details_from_db = {str(i): dict(row) for i, row in enumerate(workout_data)}

    athlete_comment = workout_data[0][2]

    db_time_format = "%d.%m.%Y %H:%M"
    html_time_format = "%Y-%m-%dT%H:%M"
    begin_time = workout_data[0][3]
    end_time = workout_data[0][4]
    begin_time = datetime.strftime(datetime.strptime(begin_time, db_time_format), html_time_format)
    end_time = datetime.strftime(datetime.strptime(end_time, db_time_format), html_time_format)

    if source_page == "workout_page.html":

        return render_template("edit_workout.html", 
                                workout_id=workout_id,
                                sport_id=sport_id,
                                purposes=purposes,
                                exercises=exercises,
                                exercise_details=details_from_db,
                                number_of_exercises=len(workout_data),
                                sport_type=sport_type,
                                begin_time=begin_time,
                                end_time=end_time,
                                athlete_comment=athlete_comment)

    if source_page == "edit_workout.html":

        action = request.form["button_action"]
        details = session.get("workout_details", {})
        n = session.get("number_of_exercises", len(workout_data))

        for i in range(0,n):

            key = str(i)
            details[key] = {}

            details[key]["exercise_id"] = int(request.form[f"exercise_{i}"])
            details[key]["purpose_id"] = int(request.form[f"purpose_{i}"])

            if sport_type == "Endurance":
                details[key]["minutes"] = request.form[f"minutes_{i}"]
                details[key]["avghr"] = request.form[f"avghr_{i}"]
                details[key]["kilometers"] = request.form[f"kilometers_{i}"]

            if sport_type == "Strength":
                details[key]["sets"] = request.form[f"sets_{i}"]
                details[key]["reps"] = request.form[f"reps_{i}"]
                details[key]["weight"] = request.form[f"weight_{i}"]

        session["exercise_details"] = details

        begin_time = request.form["begin_time"]
        end_time = request.form["end_time"]
        athlete_comment = request.form["comments"]


        if action == "add_exercise":
            n += 1
            session["number_of_exercises"] = n

            return render_template("edit_workout.html",
                                    workout_id=workout_id,
                                    sport_id=sport_id,
                                    purposes=purposes,
                                    exercises=exercises,
                                    exercise_details=details,
                                    number_of_exercises=n,
                                    sport_type=sport_type,
                                    begin_time=begin_time,
                                    end_time=end_time,
                                    athlete_comment=athlete_comment)


        if action == "save_workout":

            if not details:
                flash("Cannot save workout without exercises. Please enter exercises.")
                return render_template("edit_workout.html",
                        workout_id=workout_id,
                        sport_id=sport_id,
                        purposes=purposes,
                        exercises=exercises,
                        exercise_details=details,
                        number_of_exercises=n,
                        sport_type=sport_type,
                        begin_time=begin_time,
                        end_time=end_time,
                        athlete_comment=athlete_comment)



            if not begin_time or not end_time:
                flash("ERROR: Cannot save a workout without begin time or end time")
                return render_template("edit_workout.html",
                        workout_id=workout_id,
                        sport_id=sport_id,
                        purposes=purposes,
                        exercises=exercises,
                        exercise_details=details,
                        number_of_exercises=n,
                        sport_type=sport_type,
                        begin_time=begin_time,
                        end_time=end_time,
                        athlete_comment=athlete_comment)

            compare_begintime = datetime.strptime(begin_time, "%Y-%m-%dT%H:%M")
            compare_endtime = datetime.strptime(end_time, "%Y-%m-%dT%H:%M")
            if compare_begintime > compare_endtime:
                flash("ERROR: Cannot save a workout with begin time after end time")
                return render_template("edit_workout.html",
                        workout_id=workout_id,
                        sport_id=sport_id,
                        purposes=purposes,
                        exercises=exercises,
                        exercise_details=details,
                        number_of_exercises=n,
                        sport_type=sport_type,
                        begin_time=begin_time,
                        end_time=end_time,
                        athlete_comment=athlete_comment)

            if len(athlete_comment) > 4000:
                flash("ERROR: Comment too long. Maximum length is 4000 characters.")
                return render_template("edit_workout.html",
                        workout_id=workout_id,
                        sport_id=sport_id,
                        purposes=purposes,
                        exercises=exercises,
                        exercise_details=details,
                        number_of_exercises=n,
                        sport_type=sport_type,
                        begin_time=begin_time,
                        end_time=end_time,
                        athlete_comment=athlete_comment)


            for _, exercise in details.items():
                if sport_type == "Endurance":
                    if (not exercise["kilometers"]
                        or not exercise["minutes"]
                        or not exercise["avghr"]):

                        flash("ERROR: Workout information missing. An endurance exercise must \n"
                                "contain kilometers, minutes and average heart rate.")

                        return render_template("edit_workout.html",
                                workout_id=workout_id,
                                sport_id=sport_id,
                                purposes=purposes,
                                exercises=exercises,
                                exercise_details=details,
                                number_of_exercises=n,
                                sport_type=sport_type,
                                begin_time=begin_time,
                                end_time=end_time,
                                athlete_comment=athlete_comment)

                if sport_type == "Strength":

                    if not exercise["sets"] or not exercise["reps"]:

                        flash("ERROR: Workout information missing. A strength exercise must \n"
                                "contain sets and reps. An empty value is allowed in weights.")

                        return render_template("edit_workout.html",
                                workout_id=workout_id,
                                sport_id=sport_id,
                                purposes=purposes,
                                exercises=exercises,
                                exercise_details=details,
                                number_of_exercises=n,
                                sport_type=sport_type,
                                begin_time=begin_time,
                                end_time=end_time,
                                athlete_comment=athlete_comment)

            user_id = session["user_id"]
            workouts.delete_workout(workout_id)
            for _, exercise in details.items():

                if sport_type == "Endurance":

                    workouts.insert_workout(workout_id=workout_id, 
                                            user_id=user_id,
                                            sport_id=sport_id, 
                                            begin_time=begin_time,
                                            end_time=end_time,
                                            comments=athlete_comment,
                                            exercise_id=exercise["exercise_id"],
                                            purpose_id=exercise["purpose_id"],
                                            minutes=exercise["minutes"],
                                            avghr=exercise["avghr"], 
                                            kilometers=exercise["kilometers"],
                                            sets=None,
                                            reps=None,
                                            weight=None)

                if sport_type == "Strength":
                    workouts.insert_workout(workout_id=workout_id, 
                                            user_id=user_id,
                                            sport_id=sport_id,
                                            begin_time=begin_time,
                                            end_time=end_time,
                                            comments=athlete_comment,
                                            exercise_id=exercise["exercise_id"],
                                            purpose_id=exercise["purpose_id"],
                                            sets=exercise["sets"],
                                            reps=exercise["reps"],
                                            weight=exercise["weight"],
                                            minutes=None,
                                            avghr=None,
                                            kilometers=None)

            flash("Workout updated succesfully")
            session.pop("sport_id", None)
            session.pop("exercise_details", None)
            session.pop("number_of_exercises", None)

            return show_workout(workout_id=workout_id)



@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("username", None)

    return redirect("/")
