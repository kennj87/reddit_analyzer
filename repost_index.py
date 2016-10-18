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
                    db.commit()

                else:
                    pass
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
db.close()