from database import db
from database import cursor

def add_subreddits():
    sql_select = "SELECT subreddit FROM `post_info` GROUP BY subreddit ASC"
    try:
        cursor.execute(sql_select)
        result = cursor.fetchall()
        for row in result:
            sql_insert = "INSERT INTO subreddit (subreddit, posts, most_active_user, last_post) VALUES ('%s', '0', 'not set yet', '0')" % (row[0])
            try:
                cursor.execute(sql_insert)
            except:
                db.rollback()
        db.commit()
    except:
        pass

add_subreddits()