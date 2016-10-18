from database import cursor
from database import db

def create_posts_no_reposts(id):
    if id == None:
        id = 0
    sql_select = "SELECT MIN(ID),url FROM `post_info` WHERE ID > %s GROUP BY URL ORDER BY MIN(ID) ASC" % (id)
    try:
        cursor.execute(sql_select)
        results = cursor.fetchall()
        for row in results:
            sql_insert = "INSERT INTO post_no_repost (original_id, url) VALUES ('%s', '%s')" % (row[0], row[1])
            try:
                cursor.execute(sql_insert)
            except:
                db.rollback()
        db.commit()
    except:
        pass

def find_newest_post_no_repost():
    sql_select = "SELECT MAX(original_id) FROM post_no_repost"
    try:
        cursor.execute(sql_select)
        result = cursor.fetchall()
        for row in result:
            create_posts_no_reposts(row[0])
    except:
        pass
find_newest_post_no_repost()
db.close()