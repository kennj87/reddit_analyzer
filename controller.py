from repost_index import check_dupes_all,check_dupes_update
from post_index_no_repost import find_newest_post_no_repost
from subreddit import add_subreddits
from users import add_users
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

def run_():
    sql_get = "SELECT next_run,update_time FROM controller WHERE function = 'dupes_insert'"
    try:
        cursor.execute(sql_get)
        result = cursor.fetchall()
        for row in result:
            if int(time.time() >= row[0]):
                update_controller("dupes_insert",get_timestamp(row[1]))
                check_dupes_all(db,cursor)
            elif int(time.time() <= row[0]):
                print("not time to update yet")
    except:
        pass
    sql_update = "SELECT next_run,update_time FROM controller WHERE function = 'dupes_update'"
    try:
        cursor.execute(sql_update)
        results = cursor.fetchall()
        for update in results:
            if int(time.time() >= update[0]):
                update_controller("dupes_update", get_timestamp(update[1]))
                check_dupes_update(db, cursor)
            elif int(time.time() <= update[0]):
                print("not time to update yet")
    except:
        pass
    sql_update = "SELECT next_run,update_time FROM controller WHERE function = 'post_no_repost'"
    try:
        cursor.execute(sql_update)
        results = cursor.fetchall()
        for update in results:
            if int(time.time() >= update[0]):
                update_controller("post_no_repost", get_timestamp(update[1]))
                find_newest_post_no_repost(db,cursor)
            elif int(time.time() <= update[0]):
                print("not time to update yet")
    except:
        pass
    sql_update = "SELECT next_run,update_time FROM controller WHERE function = 'subreddit_insert'"
    try:
        cursor.execute(sql_update)
        results = cursor.fetchall()
        for update in results:
            if int(time.time() >= update[0]):
                update_controller("subreddit_insert", get_timestamp(update[1]))
                add_subreddits(db, cursor)
            elif int(time.time() <= update[0]):
                print("not time to update yet")
    except:
        pass
    sql_update = "SELECT next_run,update_time FROM controller WHERE function = 'user_insert'"
    try:
        cursor.execute(sql_update)
        results = cursor.fetchall()
        for update in results:
            if int(time.time() >= update[0]):
                update_controller("user_insert", get_timestamp(update[1]))
                add_users(db, cursor)
            elif int(time.time() <= update[0]):
                print("not time to update yet")
    except:
        pass
run_()
db.close()
print("--- %s seconds ---" % (time.time() - start_time))