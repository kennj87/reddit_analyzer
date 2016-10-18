import pymysql
import urllib3

db = pymysql.connect("localhost","root","admin","reddit")
cursor = db.cursor()

def get_image_from_database():
    db = pymysql.connect("localhost", "root", "admin", "reddit")
    cursor = db.cursor()
    sql_get = "SELECT post_info.ID,image_process.ID,post_info.url FROM post_info,image_process WHERE post_info.ID = image_process.post_id && image_process.is_processed = 0 LIMIT 1"
    try:
        cursor.execute(sql_get)
        results = cursor.fetchall()
        for row in results:
            image_id = row[0]
            process_id = row[1]
            image_url = row[2]
            print(image_url," ",image_id, " ",process_id)
            download_image(image_url,process_id,image_id)
    except:
        pass

def download_image(url,id,origin_id):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    imagename = "/home/kenneth/dlimage/%s" % (origin_id)
    with open(imagename, 'wb') as f:
        f.write(response.data)
        http.clear()
        update_image_processed(id,origin_id)

def update_image_processed(id,origin_id):
    db = pymysql.connect("localhost", "root", "admin", "reddit")
    cursor = db.cursor()
    sql_update = "UPDATE image_process SET is_processed = 1 WHERE ID = %s" % (id)
    try:
        cursor.execute(sql_update)
        db.commit()
        get_image_from_database()
    except:
        db.rollback()

def run_image():
    pass
    if __name__ == "download_image":
        get_image_from_database()
db.close()
