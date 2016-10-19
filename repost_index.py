from database import cursor
from database import db

def check_dupes_all():
    sql_dupes = "SELECT y.id,y.author,y.url,counter FROM post_info y INNER JOIN (SELECT url, COUNT(*) AS counter FROM post_info GROUP BY url HAVING COUNT(*)>1) dt ON y.url=dt.url"
    try:
        cursor.execute(sql_dupes)
        results = cursor.fetchall()
        for row in results:
            sql_lookup_id = "SELECT url FROM post_reposts WHERE url = '%s'" % (row[2])
            try:
                cursor.execute(sql_lookup_id)
                #url is not in the database, lets add it.
                if not cursor.rowcount:
                    sql_insert = "INSERT INTO post_reposts (url, author, post_id, repost_count) VALUES ('%s', '%s', '%s', '%s')" % (row[2], row[1], row[0], row[3]-1)
                    try:
                        cursor.execute(sql_insert)
                    except:
                        db.rollback()
                else:
                    pass
            except:
                pass
        db.commit()
    except:
        pass

def check_dupes_update():
    sql_select = "SELECT url FROM post_reposts"
    try:
        cursor.execute(sql_select)
        results = cursor.fetchall()
        for row in results:
            sql_get_amount = "SELECT COUNT(url) from post_info where url = '%s'" % (row[0])
            try:
                cursor.execute(sql_get_amount)
                result = cursor.fetchall()
                for rows in result:
                    sql_update = "UPDATE post_reposts SET repost_count = '%s' WHERE url = '%s'" % (rows[0]-1, row[0])
                    try:
                        cursor.execute(sql_update)
                    except:
                        pass
                    db.commit()
            except:
                pass

    except:
        pass

def check_dupes_same_subreddit():
    sql_dupes = "SELECT y.id,y.author,y.url,y.subreddit FROM post_info y INNER JOIN (SELECT url, COUNT(*) AS counter FROM post_info GROUP BY url HAVING COUNT(*)>1) dt ON y.url=dt.url AND y.subreddit=dt.subreddit"
    try:
        cursor.execute(sql_dupes)
        results = cursor.fetchall()
        for row in results:
            print(row)
    except:
        pass

check_dupes_all()
check_dupes_update()
db.close()