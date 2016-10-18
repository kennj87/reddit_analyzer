import pymysql


def id_used(name):
    db = pymysql.connect("localhost", "root", "admin", "reddit")
    cursor = db.cursor()
    sql_get = "SELECT name FROM post_info WHERE name = '%s'" % (name)
    try:
        cursor.execute(sql_get)
        if not cursor.rowcount:
            return True
        else:
            return False
    except:
        pass

    db.close()