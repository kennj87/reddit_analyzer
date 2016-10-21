def check_dupes_all(db,cursor):
    sql_dupes = "SELECT y.id,y.author,y.url,counter FROM post_info y INNER JOIN (SELECT url, COUNT(url) AS counter FROM post_info GROUP BY url HAVING COUNT(url)>1) dt ON y.url=dt.url"
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

def check_dupes_update(db,cursor):
    sql_select = "SELECT url FROM post_reposts"
    try:
        cursor.execute(sql_select)
        results = cursor.fetchall()
        for row in results:
            sql_update = "UPDATE post_reposts SET repost_count = (SELECT COUNT(url) FROM post_info WHERE url = '%s')-1 WHERE url = '%s'" % (row[0],row[0])
            try:
                pass
                cursor.execute(sql_update)
                db.commit()
            except:
                pass
    except:
        pass

def check_dupes_same_subreddit(db,cursor):
    sql_dupes = "SELECT y.id,y.author,y.url,y.subreddit FROM post_info y INNER JOIN (SELECT url, COUNT(url) AS counter FROM post_info GROUP BY url HAVING COUNT(url)>1) dt ON y.url=dt.url AND y.subreddit=dt.subreddit"
    try:
        cursor.execute(sql_dupes)
        results = cursor.fetchall()
        for row in results:
            print(row)
    except:
        pass
