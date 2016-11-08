def check_last_id_checked(db,cursor):
    sql_check = "SELECT ID from image_process"
    try:
        cursor.execute(sql_check)
        if cursor.rowcount:
            sql_get = "SELECT post_id from image_process ORDER BY ID DESC LIMIT 1"
            try:
                cursor.execute(sql_get)
                results = cursor.fetchone()
                for row in results:
                    process_id = row
                    return row
            except:
                pass
        else:
            return 0
    except:
        pass

def image_to_db(id,type,db,cursor):
    sql_set = "INSERT INTO image_process (post_id, filetype, is_processed, is_hashed) VALUES ('%s', '%s', '0', '0')" % (id,type)
    try:
        cursor.execute(sql_set)
        db.commit()
    except:
        db.rollback()

def check_if_image(db,cursor):
    last_id = str(check_last_id_checked(db,cursor))
    sql_get = "SELECT url,ID from post_info where ID > "+last_id+""
    try:
        cursor.execute(sql_get)
        results = cursor.fetchall()
        for row in results:
            url = row[0]
            id = row[1]
            if url.endswith('.jpg'):
                image_to_db(id,"jpg",db,cursor)
            elif url.endswith('.png'):
                image_to_db(id,"png",db,cursor)
            elif "i.reddituploads.com" in url:
                image_to_db(id,"jpg",db,cursor)
    except:
        pass
