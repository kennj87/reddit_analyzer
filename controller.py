from repost_index import check_dupes_all,check_dupes_update
from post_index_no_repost import find_newest_post_no_repost
from subreddit import add_subreddits,update_subreddit_posts,update_subreddit_top_poster_new,update_subreddit_top_poster_update,update_subreddit_time
from users import add_users,update_users_posts,update_users_time
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

run_it = {
    update_subreddit_top_poster_update:'subreddit_posts_top_update',
    update_subreddit_top_poster_new:'subreddit_posts_top_new',
    update_subreddit_posts:'subreddit_posts',
    update_subreddit_time:'subreddit_time',
    add_users:'user_insert',
    update_users_posts:'users_posts',
    update_users_time:'users_time',
    add_subreddits:'subreddit_insert',
    find_newest_post_no_repost:'post_no_repost',
    check_dupes_update:'dupes_update',
    check_dupes_all:'dupes_insert'
    }

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