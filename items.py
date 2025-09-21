import db

def add_userdata(username, firstname, lastname, dateofbirth, height, weight,
                 max_heart_rate, ftp_cycling):
    sql = """UPDATE users SET 
                first_name = ?, 
                last_name = ?, 
                date_of_birth = ?, 
                height = ?, 
                weight = ?,
                max_heart_rate = ?, 
                ftp_cycling = ?,
                where username = ?"""
    db.execute(sql, [firstname, lastname, dateofbirth, height, weight,
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

    
