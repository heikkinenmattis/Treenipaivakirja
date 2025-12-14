import random
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM workouts")
db.execute("DELETE FROM comments")

user_count = 10000
workout_count = 10**6
comment_count = 10**7

for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (username) VALUES (?)",
               ["user" + str(i)])

for i in range(1, workout_count + 1):
    sportid = random.randint(1,4)
    user_id = random.randint(1, user_count)

    if sportid == 1 or sportid == 2:
        exercise_id = random.randint(8,11)
        purposes = [1,10]
        purpose_id = random.choice(purposes)
    else:
        strength_ex_id = [1,2,3,4,5,6,7,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]
        purposes = [1,2,3,4,5,6,7,8,9,11]
        exercise_id = random.choice(strength_ex_id)
        purpose_id = random.choice(purposes)

    db.execute("INSERT INTO workouts (workout_id, begin_time, sport_id, user_id, exercise_id, purpose_id) VALUES (?,datetime('now'),?,?,?,?)",
            ["workout" + str(i), sportid, user_id, exercise_id, purpose_id])

for i in range(1, comment_count + 1):
    user_id = random.randint(1, user_count)
    workout_id_nr = random.randint(1, workout_count)
    workout_id = "workout" + str(workout_id_nr)
    db.execute("""INSERT INTO comments (content, timestamp, user_id, workout_id)
                  VALUES (?, datetime('now'), ?, ?)""",
               ["message" + str(i), user_id, workout_id])

db.commit()
db.close()
