from check_if_post_is_image import check_if_image
from download_image import get_image_from_database
from hash_and_remove_file import hash_images
from database import db
from database import cursor
import time

start_time = time.time()
def get_timestamp(time):
    return int(start_time)+(60*time)

def update_controller(timer,func):
    sql_update = "UPDATE controller SET next_run = '%s' WHERE function = '%s'" % (func,timer)
    try:
        cursor.execute(sql_update)
        db.commit()
    except:
        pass

def update_controller_runtime(func,runtime):
    newtime = time.time() - runtime
    sql_update = "UPDATE controller SET runtime = '%s' WHERE function = '%s'" % (newtime, func)
    try:
        cursor.execute(sql_update)
        db.commit()
    except:
        pass

run_it = {
    check_if_image:'image_list',
    hash_images: 'hash_image',
    get_image_from_database:'get_image_from_db'
    }

for key, val in run_it.items():
    time_now = time.time()
    sql_update = "SELECT next_run,update_time FROM controller WHERE function = '%s'" % (val)
    try:
        cursor.execute(sql_update)
        results = cursor.fetchall()
        for update in results:
            if int(time.time() >= update[0]):
                update_controller(val, get_timestamp(update[1]))
                key(db, cursor)
                update_controller_runtime(val, time_now)
            elif int(time.time() <= update[0]):
                pass
    except:
        pass
db.close()