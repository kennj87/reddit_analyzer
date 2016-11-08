import pymysql

db = pymysql.connect("localhost","root","admin","reddit")
cursor = db.cursor()

def check_duplicates():
    sql = "SELECT hash,original_id FROM hashes_duplicates"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            sql_dupe = "SELECT ID,hash,post_id, BIT_COUNT(CAST(CONV(hash, 16, 10) AS UNSIGNED) ^ CAST(CONV('%s', 16 ,10) AS UNSIGNED)) AS hamming_distance FROM hashes WHERE post_id <> '%s' HAVING hamming_distance < 4 ORDER BY `hamming_distance` ASC" % (row[0],row[1])
            try:
                cursor.execute(sql_dupe)
                result = cursor.fetchall()
                for rows in result:
                    print("Hash: %s Is equal to: %s (Original: %s - New: %s) Distance: %s" % (row[0],rows[1],row[1],rows[2],rows[3]))
            except:
                pass
    except:
        pass
check_duplicates()
db.close