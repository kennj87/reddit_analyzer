from scrab_reddit import runs
from database import db,cursor
import threading

def see_if_it_runs():
    if check_if_run():
        runs()
        print("ran scrab")
    threading.Timer(1.0, see_if_it_runs).start()

def check_if_run():
    sql = "SELECT next_run FROM controller WHERE function = 'run'"
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        db.commit()
        for row in result:
            if row[0] == 1:
                return True
            elif row[0] != 1:
                return False
    except:
        pass

see_if_it_runs()
