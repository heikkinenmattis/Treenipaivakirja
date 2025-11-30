import db



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


def get_workouts():
    sql = """   select distinct         
                        
                        w.workout_id,
                        w.user_id,
                        u.username, 
                        s.sport_name, 
                        datetime(w.begin_time) as begin_time, 
                        datetime(w.end_time) as end_time,
                        case when s.sport_type = 'Strength' then sum(w.sets*w.reps*w.weight) else null end as total_kilograms,
                        case when s.sport_type = 'Endurance' then sum(w.kilometers) else null end as kilometers,
                        s.sport_type,
                        timediff(w.end_time, w.begin_time) as duration,
                        strftime('%d.%m.%Y', w.begin_time) as time_to_present

                from workouts w
                join sports s on w.sport_id = s.sport_id
                join users u on w.user_id = u.id
                join exercises e on w.exercise_id = e.exercise_id
                join exercise_purposes p on w.purpose_id = p.purpose_id 
                group by w.workout_id, u.username, s.sport_name, w.begin_time, w.end_time
                """

    return db.query(sql, [])

