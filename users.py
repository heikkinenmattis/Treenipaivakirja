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
                        c.city
                FROM users u 
                LEFT JOIN sports s 
                    on u.fav_sport_id = s.sport_id
                LEFT JOIN cities c
                    on u.city_id = c.city_id
                WHERE u.id = ?"""

    return db.query(sql, [user_id])
