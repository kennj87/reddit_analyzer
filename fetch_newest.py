import pymysql

db = pymysql.connect("localhost","root","admin","reddit")
cursor = db.cursor()

def fetch_newest():
    sql_get = "SELECT name FROM post_info ORDER BY ID DESC limit 1"
    try:
        cursor.execute(sql_get)
        results = cursor.fetchone()
        for row in results:
            name_id = row
    except:
        print("Unable to find data")

name_id = fetch_newest()

db.close()