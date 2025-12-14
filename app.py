import sqlite3
import secrets
import uuid
import math

from datetime import datetime
from flask import Flask
from flask import redirect, render_template, request, flash, abort
from flask import session
import markupsafe

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
@app.route("/<int:page>")
def index(page=1):

    workouts_count = workouts.get_workout_count()[0][0]

    page_size = 10
    page_count = math.ceil(workouts_count / page_size)
    page_count = max(page_count, 1)

    all_workouts = workouts.get_workouts(page, page_size)

    return render_template("index.html", workouts=all_workouts, page=page, page_count=page_count)

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        user_id = users.check_login(username, password)

        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")

        flash("ERROR: Username or password not recognized")
        return redirect("/login")

    return render_template("index.html")



@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)


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
    weight = int(request.form["weight"])
    height = int(request.form["height"])
    max_heart_rate = int(request.form["max_heart_rate"])
    ftp_cycling = int(request.form["ftp_cycling"])
    fav_sport = int(request.form["fav_sport"])
    city = int(request.form["user_city"])

    error_msg = None

    if len(first_name) < 2 or len(first_name) > 20:
        error_msg = "ERROR: First name too short or too long."

    elif len(last_name) < 2 or len(last_name) > 40:
        error_msg = "ERROR: Last name too short or too long."

    elif datetime.strptime(date_of_birth, "%Y-%m-%d") < datetime(1900,1,1):
        error_msg = "ERROR: Suspicious birth date."

    elif weight < 30 or weight > 300:
        error_msg = "ERROR: Suspicious weight."

    elif height < 100 or height > 235:
        error_msg = "ERROR: Suspicious weight."

    elif max_heart_rate < 30 or max_heart_rate > 230:
        error_msg = "ERROR: Suspicious maximum heart rate."

    elif ftp_cycling < 50 or ftp_cycling > 500:
        error_msg = "ERROR: Suspicious FTP."

    if error_msg:
        flash(error_msg)
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
        error_msg = None

        if not details:
            error_msg = "Cannot save workout without exercises. Please enter exercises."

        elif begin_time and end_time:
            compare_begintime = datetime.strptime(begin_time, "%Y-%m-%dT%H:%M")
            compare_endtime = datetime.strptime(end_time, "%Y-%m-%dT%H:%M")
            if compare_begintime > compare_endtime:
                error_msg = "ERROR: Cannot save a workout with begin time after end time"

        elif not begin_time or not end_time:
            error_msg = "ERROR: Cannot save a workout without begin time or end time"

        elif len(comments) > 4000:
            error_msg = "ERROR: Comment too long. Maximum length is 4000 characters."

        if error_msg:
            flash(error_msg)
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
@app.route("/user/<int:user_id>/<int:page>")
def show_user(user_id, page=1):


    workouts_count = users.get_user_workout_count(user_id)[0][0]

    page_size = 10
    page_count = math.ceil(workouts_count / page_size)
    page_count = max(page_count, 1)

    user = users.fetch_userdata(user_id)[0]
    if not user:
        abort(404)

    most_common_sport = users.fetch_most_common_sport(user_id)[0]
    most_common_exercise = users.fetch_most_common_exercise(user_id)[0]

    user_workouts = users.fetch_user_workouts(user_id, page, page_size)
    return render_template("user_page.html",
                           user=user,
                           user_workouts=user_workouts,
                           most_common_sport=most_common_sport,
                           most_common_exercise=most_common_exercise,
                           page=page,
                           page_count=page_count,
                           workouts_count=workouts_count)


@app.route("/workouts/<workout_id>")
@app.route("/workouts/<workout_id>/<int:page>")
def show_workout(workout_id, page=1):

    require_login()

    workout_data = workouts.fetch_workout_data(workout_id)
    workout_sport = workout_data[0][0]
    workout_user = workout_data[0][1]
    workout_comment = workout_data[0][2]
    workout_begin_time = workout_data[0][3]
    workout_end_time = workout_data[0][4]
    workout_user_id = workout_data[0][14]
    workout_sport_id = workout_data[0][16]

    comments_count = workouts.fetch_comments_count(workout_id)[0][0]

    page_size = 5
    page_count = math.ceil(comments_count / page_size)
    page_count = max(page_count, 1)

    previous_comments = workouts.fetch_comments(workout_id, page, page_size)

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
                            workout_sport_id=workout_sport_id,
                            page=page,
                            page_count=page_count)


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

    elif source_page == "edit_workout.html":

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


        elif action == "save_workout":

            error_msg = None
            if not details:
                error_msg = "Cannot save workout without exercises. Please enter exercises."

            elif begin_time and end_time:
                compare_begintime = datetime.strptime(begin_time, "%Y-%m-%dT%H:%M")
                compare_endtime = datetime.strptime(end_time, "%Y-%m-%dT%H:%M")
                if compare_begintime > compare_endtime:
                    error_msg = "ERROR: Cannot save a workout with begin time after end time"

            elif not begin_time or not end_time:
                error_msg = "ERROR: Cannot save a workout without begin time or end time"

            elif len(athlete_comment) > 4000:
                error_msg = "ERROR: Comment too long. Maximum length is 4000 characters."


            for _, exercise in details.items():

                if sport_type == "Endurance":
                    if (not exercise["kilometers"]
                        or not exercise["minutes"]
                        or not exercise["avghr"]):
                        error_msg = (
                        "ERROR: Workout information missing. An endurance exercise must \n"
                        "contain kilometers, minutes and average heart rate.")

                elif sport_type == "Strength":
                    if not exercise["sets"] or not exercise["reps"]:
                        error_msg = (
                        "ERROR: Workout information missing. A strength exercise must \n"
                        "contain sets and reps. An empty value is allowed in weights.")

            if error_msg:
                flash(error_msg)
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

            return redirect(f"/workouts/{workout_id}")

        flash("Invalid action")
        return redirect("/")

    flash("Invalid source page")
    return redirect("/")



@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("username", None)

    return redirect("/")
