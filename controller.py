from repost_index import check_dupes_all,check_dupes_update
from database import db
from database import cursor
import time
start_time = time.time()

#check_dupes_all(db,cursor)
check_dupes_update(db,cursor)

db.close()
print("--- %s seconds ---" % (time.time() - start_time))