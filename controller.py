from repost_index import check_dupes_all,check_dupes_update
from post_index_no_repost import find_newest_post_no_repost
from subreddit import add_subreddits
from users import add_users
from database import db
from database import cursor
import time

start_time = time.time()
def get_timestamp(time):
    return int(start_time)+(60*time)

def update_controller(func,timer,runtime):
    newtime = time.time() - runtime
    sql_update = "UPDATE controller SET next_run = '%s', runtime = '%s' WHERE function = '%s'" % (timer,newtime,func)
    try:
        cursor.execute(sql_update)
        db.commit()
    except:
        pass

run_it = {add_users:'user_insert', add_subreddits:'subreddit_insert', find_newest_post_no_repost:'post_no_repost', check_dupes_update:'dupes_update', check_dupes_all:'dupes_insert'}

for key, val in run_it.items():
    time_now = time.time()
    sql_update = "SELECT next_run,update_time FROM controller WHERE function = '%s'" % (val)
    try:
        cursor.execute(sql_update)
        results = cursor.fetchall()
        for update in results:
            if int(time.time() >= update[0]):
                key(db, cursor)
                update_controller(val, get_timestamp(update[1]), time_now)
            elif int(time.time() <= update[0]):
                pass
    except:
        pass

db.close()