def add_users(db,cursor):
    sql_select = "SELECT author FROM post_info WHERE author NOT IN (SELECT name from users) GROUP BY author"
    try:
        cursor.execute(sql_select)
        result = cursor.fetchall()
        for row in result:
            sql_insert = "INSERT INTO users (name, posts, created) VALUES ('%s', '1', '0')" % (row[0])
            try:
                cursor.execute(sql_insert)
            except:
                db.rollback()
        db.commit()
    except:
        pass

def update_users_posts(db,cursor):
    sql_initial = "SELECT COUNT(*),post_info.author FROM post_info,users WHERE post_info.author = users.name GROUP BY post_info.author"
    cursor.execute(sql_initial)
    result = cursor.fetchall()
    users = {}
    for row in result:
        users[row[1]] = row[0]
    sql_posts = "SELECT posts,name FROM users"
    cursor.execute(sql_posts)
    results = cursor.fetchall()
    for rows in results:
        if rows[0] != users[rows[1]]:
            sql_update = "UPDATE users SET posts = '%s' WHERE name = '%s'" % (users[rows[1]],rows[1])
            try:
                cursor.execute(sql_update)
            except:
                pass
    db.commit()

def update_users_time(db,cursor):
    sql_update = "UPDATE users,post_info SET users.created = (SELECT post_info.created from post_info WHERE users.name = post_info.author GROUP BY post_info.created LIMIT 1) WHERE post_info.author = users.name AND users.created = 0"
    try:
        cursor.execute(sql_update)
    except:
        pass
    db.commit()