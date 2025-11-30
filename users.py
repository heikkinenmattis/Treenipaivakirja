from werkzeug.security import check_password_hash, generate_password_hash
import db


def create_user(username, password):

    #Using pbkdf2 for developement due to working on Macbook.
    password_hash = generate_password_hash(password, method='pbkdf2')
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])



def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return None

    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]
    if check_password_hash(password_hash, password):
        return user_id
    else:
        return None



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
                        c.city,
                        u.username
                FROM users u 
                LEFT JOIN sports s 
                    on u.fav_sport_id = s.sport_id
                LEFT JOIN cities c
                    on u.city_id = c.city_id
                WHERE u.id = ?"""

    return db.query(sql, [user_id])


def fetch_user_workouts(user_id):
    sql = """select distinct         
                        
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
                        strftime('%d.%m.%Y', w.begin_time) as time_to_present,
                        w.comments

                from workouts w
                join sports s on w.sport_id = s.sport_id
                join users u on w.user_id = u.id
                join exercises e on w.exercise_id = e.exercise_id
                join exercise_purposes p on w.purpose_id = p.purpose_id
                where u.id = ?
                group by w.workout_id, u.username, s.sport_name, w.begin_time, w.end_time
                order by datetime(w.begin_time) DESC """

    return db.query(sql, [user_id])



def fetch_most_common_sport(user_id):

    sql = """   SELECT  s.sport_name, 
                        COUNT(distinct w.workout_id) as sport_count

                FROM workouts w
                JOIN sports s on w.sport_id = s.sport_id
                WHERE w.user_id = ?
                GROUP BY s.sport_name
                ORDER BY sport_count DESC
                LIMIT 1
            """

    return db.query(sql, [user_id])

def fetch_most_common_exercise(user_id):
    sql = """   SELECT  e.exercise_name, 
                        COUNT(e.exercise_name) as exercise_count

                FROM workouts w
                JOIN exercises e on w.exercise_id = e.exercise_id
                WHERE w.user_id = ?
                GROUP BY e.exercise_name
                ORDER BY exercise_count DESC
                LIMIT 1
            """

    return db.query(sql, [user_id])