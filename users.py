def add_users(db,cursor):
    sql_select = "SELECT author FROM post_info WHERE author NOT IN (SELECT name from users) GROUP BY author"
    try:
        cursor.execute(sql_select)
        result = cursor.fetchall()
        for row in result:
            sql_insert = "INSERT INTO users (name, posts, created) VALUES ('%s', '0', '0')" % (row[0])
            try:
                cursor.execute(sql_insert)
            except:
                db.rollback()
        db.commit()
    except:
        pass