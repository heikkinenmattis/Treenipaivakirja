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
    sql = """   SELECT DISTINCT sport_id, sport_name from sports"""

    return db.query(sql, [])


def fetch_sport_type(sport_id):
    sql = """   SELECT sport_type from sports where sport_id = ?"""

    return db.query(sql, [sport_id])


def insert_workout(workout_id, user_id, sport_id, begin_time, end_time, comments, sets, 
                   reps, weight, minutes, avghr, kilometers, exercise_id, purpose_id):
    sql = """   INSERT INTO workouts (  workout_id,
                                        user_id,
                                        sport_id,
                                        begin_time,
                                        end_time,
                                        comments,
                                        sets,
                                        reps,
                                        weight,
                                        minutes,
                                        avg_hr,
                                        kilometers,
                                        exercise_id,
                                        purpose_id)
                                        
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """
    db.execute(sql, [workout_id, user_id, sport_id,
                     begin_time, end_time, comments,
                     sets, reps, weight, minutes, avghr,
                     kilometers, exercise_id, purpose_id])


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


def get_workouts(page=1, page_size=20):
    starting_point = (page-1) * page_size
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
                order by datetime(w.begin_time) desc
                limit ? offset ?
                """

    return db.query(sql, [page_size, starting_point])

def get_workout_count():
    sql = """   select count(distinct w.workout_id)
                from workouts w
            """

    return db.query(sql, [])


def fetch_workout_data(workout_id):
    sql = """   select  s.sport_name,
                        u.username,
                        w.comments,
                        strftime('%d.%m.%Y %H:%M', w.begin_time) as begin_time,
                        strftime('%d.%m.%Y %H:%M', w.end_time) as end_time,
                        s.sport_type,
                        e.exercise_name,
                        p.purpose_name,
                        w.sets,
                        w.reps,
                        w.weight,
                        w.avg_hr as avghr,
                        w.minutes,
                        w.kilometers,
                        u.id,
                        w.workout_id,
                        s.sport_id,
                        e.exercise_id,
                        p.purpose_id

                from workouts w
                join exercises e on w.exercise_id = e.exercise_id
                join sports s on w.sport_id = s.sport_id
                join users u on w.user_id = u.id
                join exercise_purposes p on w.purpose_id = p.purpose_id 
                where w.workout_id = ?
                order by datetime(w.begin_time) desc

            """

    return db.query(sql, [workout_id])



def search_workouts(query):
    sql = """   select distinct

                        w.workout_id,
                        s.sport_name,
                        u.username,
                        w.comments,
                        strftime('%d.%m.%Y %H:%M', w.begin_time) as begin_time,
                        strftime('%d.%m.%Y %H:%M', w.end_time) as end_time
                        
                from workouts w
                join exercises e on w.exercise_id = e.exercise_id
                join sports s on w.sport_id = s.sport_id
                join users u on w.user_id = u.id
                join exercise_purposes p on w.purpose_id = p.purpose_id 
                where lower(s.sport_name) LIKE ? or lower(e.exercise_name) LIKE ?
                """

    search_word = f"%{query}%"

    return db.query(sql, [search_word, search_word])



def comment_workout(user_id, workout_id, timestamp, content):
    sql = """   insert into comments (user_id, workout_id, timestamp, content)
                    values (?,?,?,?)
                """
    db.execute(sql, [user_id, workout_id, timestamp, content])



def fetch_comments(workout_id, page=1, page_size=5):
    starting_point = (page-1) * page_size
    sql = """   select  c.user_id,
                        u.username,
                        c.workout_id,
                        strftime('%d.%m.%Y %H:%M', c.timestamp) as timestamp,
                        c.content

                from comments c
                join users u on c.user_id = u.id
                where c.workout_id = ?
                order by datetime(c.timestamp) desc
                limit ? offset ?
                """

    return db.query(sql, [workout_id, page_size, starting_point])


def fetch_comments_count(workout_id):
    sql = """   select count(distinct c.id)
                from comments c
                where c.workout_id = ?
                """

    return db.query(sql, [workout_id])


def delete_workout(workout_id):
    sql = """   delete from workouts where workout_id = ?
                """
    db.execute(sql, [workout_id])
