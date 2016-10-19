from database import db
from database import cursor

def add_subreddits():
    sql_select = "SELECT author FROM post_info WHERE author NOT IN (SELECT name from users) GROUP BY author"
    try:
        cursor.execute(sql_select)
        result = cursor.fetchall()
        for row in result:
            sql_insert = "INSERT INTO users (name, posts) VALUES ('%s', '0')" % (row[0])
            try:
                cursor.execute(sql_insert)
            except:
                db.rollback()
        db.commit()
    except:
        pass

add_subreddits()
db.close()