import db

def add_userdata(username, first_name, last_name, date_of_birth, height, weight,
                 max_heart_rate, ftp_cycling):
    sql = """UPDATE users SET 
                first_name = ?, 
                last_name = ?, 
                date_of_birth = ?, 
                height = ?, 
                weight = ?,
                max_heart_rate = ?, 
                ftp_cycling = ?
                where username = ?"""
    db.execute(sql, [first_name, last_name, date_of_birth, height, weight,
                 max_heart_rate, ftp_cycling, username])





def fetch_userdata(user_id):
    sql = """   SELECT  u.first_name, 
                        u.last_name, 
                        u.date_of_birth, 
                        u.height, 
                        u.weight, 
                        u.max_heart_rate, 
                        u.ftp_cycling, 
                        u.fav_sport_id, 
                        s.sport_name, 
                        c.city
                FROM users u 
                LEFT JOIN sports s 
                    on u.fav_sport_id = s.sport_id
                LEFT JOIN cities c
                    on u.city_id = c.city_id
                WHERE u.id = ?"""

    return db.query(sql, [user_id])


def fetch_exercises(sport_id):
    sql = """   SELECT DISTINCT e.exercise_name, e.exercise_id   
                FROM exercises_and_sports es
                JOIN exercises e
                    on es.exercise_id = e.exercise_id
                WHERE es.sport_id = ?
                ORDER BY 1"""

    return db.query(sql, [sport_id])

def fetch_sports():
    sql = """   SELECT DISTINCT sport_id, sport_name from sports where 1 = ?"""

    return db.query(sql, [1])

def fetch_sport_type(sport_id):
    sql = """   SELECT sport_type from sports where sport_id = ?"""

    return db.query(sql, [sport_id])

def insert_workout(workout_id, user_id, sport_id, begin_time, end_time, comments, sets, 
                   reps, weight, minutes, avghr, kilometers, exercise_id, purpose_id):
    sql = """   INSERT INTO workouts (workout_id, user_id, sport_id, begin_time, end_time, comments, sets, reps, weight, minutes, avg_hr, kilometers, exercise_id, purpose_id)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """
    db.execute(sql, [workout_id, user_id, sport_id, begin_time, end_time, comments, sets, reps, weight, minutes, avghr, kilometers, exercise_id, purpose_id])

# def insert_workout(workout_id, user_id, sport_id, begin_time, end_time, comments, sets=None, 
#                    reps=None, weight=None, minutes=None, avghr=None, kilometers=None):
#     sql = """   INSERT INTO workouts (workout_id, user_id, sport_id, begin_time, end_time, comments, sets, reps, weight, minutes, avghr, kilometers)
#                     VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
#                 """
#     db.execute(sql, [workout_id, user_id, sport_id, begin_time, end_time, comments, sets, reps, weight, minutes, avghr, kilometers])


def fetch_purposes(sport_type):
    sql = """   SELECT DISTINCT p.purpose_id, p.purpose_name 
                FROM sports s 
                JOIN exercises_and_sports es 
                    on s.sport_id = es.sport_id 
                JOIN exercises_and_purposes ep 
                    on es.exercise_id = ep.exercise_id 
                JOIN exercise_purposes p 
                    on ep.purpose_id = p.purpose_id 
                where s.sport_type = ? 
            """

    return db.query(sql, [sport_type])



    










