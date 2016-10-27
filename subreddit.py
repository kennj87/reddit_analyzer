def add_subreddits(db,cursor):
    sql_select = "SELECT subreddit FROM post_info WHERE subreddit NOT IN (SELECT subreddit from subreddit) GROUP BY subreddit"
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

def update_subreddit_posts(db,cursor):
    sql_initial = "SELECT COUNT(*),post_info.subreddit FROM post_info,subreddit WHERE post_info.subreddit = subreddit.subreddit GROUP BY post_info.subreddit"
    cursor.execute(sql_initial)
    result = cursor.fetchall()
    subreddits = {}
    for row in result:
        subreddits[row[1]] = row[0]
    sql_posts = "SELECT posts,subreddit FROM subreddit"
    cursor.execute(sql_posts)
    results = cursor.fetchall()
    for rows in results:
        if rows[0] != subreddits[rows[1]]:
            sql_update = "UPDATE subreddit SET posts = '%s' WHERE subreddit = '%s'" % (subreddits[rows[1]],rows[1])
            try:
                cursor.execute(sql_update)
            except:
                pass
    db.commit()

def update_subreddit_top_poster_new(db,cursor):
    sql = "SELECT COUNT(*) as cnt,author,subreddit FROM post_info WHERE subreddit = subreddit AND author = author GROUP BY author,subreddit ORDER BY cnt ASC"
    cursor.execute(sql)
    result = cursor.fetchall()
    posts = {}
    for row in result:
        posts[row[2]] = row[1]
    sql_get = "SELECT subreddit FROM subreddit where most_active_user = 'not set yet'"
    cursor.execute(sql_get)
    results = cursor.fetchall()
    for rows in results:
        sql_update = "UPDATE subreddit SET most_active_user = '%s' WHERE subreddit = '%s'" % (posts[rows[0]], rows[0])
        try:
            cursor.execute(sql_update)
        except:
            pass
    db.commit()

def update_subreddit_top_poster_update(db,cursor):
    sql = "SELECT COUNT(*) as cnt,author,subreddit FROM post_info WHERE subreddit = subreddit AND author = author GROUP BY author,subreddit ORDER BY cnt ASC"
    cursor.execute(sql)
    result = cursor.fetchall()
    posts = {}
    for row in result:
        posts[row[2]] = row[1]
    sql_get = "SELECT subreddit,most_active_user FROM subreddit"
    cursor.execute(sql_get)
    results = cursor.fetchall()
    for rows in results:
        if rows[1] != posts[rows[0]]:
            sql_update = "UPDATE subreddit SET most_active_user = '%s' WHERE subreddit = '%s'" % (posts[rows[0]], rows[0])
            try:
                cursor.execute(sql_update)
            except:
                pass
    db.commit()