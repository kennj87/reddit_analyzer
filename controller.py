from repost_index import check_dupes_all,check_dupes_update
from database import db
from database import cursor
import time
start_time = time.time()

#check_dupes_all(db,cursor)
#check_dupes_update(db,cursor)
def get_timestamp(time):
    return int(start_time)+(60*time)

def update_controller(func,time):
    sql_update = "UPDATE controller SET next_run = '%s' WHERE function = '%s'" % (time,func)
    try:
        cursor.execute(sql_update)
        db.commit()
    except:
        pass

def run_dupes_all():
    sql_get = "SELECT next_run,update_time FROM controller WHERE function = 'dupes_update'"
    try:
        cursor.execute(sql_get)
        result = cursor.fetchall()
        for row in result:
            if int(time.time() >= row[0]):
                update_controller("dupes_update",get_timestamp(row[1]))
                #check_dupes_all()
            elif int(time.time() <= row[0]):
                print("not time to update yet")


    except:
        pass

run_dupes_all()
db.close()
print("--- %s seconds ---" % (time.time() - start_time))