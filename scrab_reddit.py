import praw
import pymysql
from fetch_newest import name_id
from prawoauth2 import PrawOAuth2Mini
from secrets import *
from settings import *

def runs(runs):
    runcount = 0
    runrep = 1
    while runrep == 1:
        db = pymysql.connect("localhost","root","admin","reddit")
        cursor = db.cursor()
        r = praw.Reddit(user_agent = USER_AGENT)
        oauth_helper = PrawOAuth2Mini(r,app_key = APP_KEY,app_secret = APP_SECRET,
                                        access_token = ACCESS_TOKEN,scopes = SCOPES,
                                        refresh_token = REFRESH_TOKEN)
        oauth_helper.refresh()
        subreddit = r.get_subreddit('all')

        author = "none"
        created = 0
        over_18 = 0
        permalink = "none"
        subred = "none"
        thumbnail = "none"
        title = "none"
        url = "none"
        name = "none"
        media = "none"

        def id_used(name):
            db = pymysql.connect("localhost", "root", "admin", "reddit")
            cursor = db.cursor()
            sql_get = "SELECT name FROM post_info WHERE name = '%s'" % (name)
            try:
                cursor.execute(sql_get)
                if not cursor.rowcount:
                    return True
                else:
                    return False
            except:
                pass

        for post in reversed(list(subreddit.get_new(after=name_id))):
            author = str(vars(post)['author'])
            created = int(vars(post)['created'])
            over_18 = int(vars(post)['over_18'])
            permalink = str(vars(post)['permalink'])
            subred = str(vars(post)['subreddit'])
            thumbnail = str(vars(post)['thumbnail'])
            title = str(vars(post)['title'])
            url = str(vars(post)['url'])
            name = str(vars(post)['name'])
            media = str(vars(post)['media'])
            if id_used(name):
                sql = "INSERT INTO `post_info` (`ID`, `author`, `title`, `subreddit`, `url`, `permalink`, `media`, `created`, `thumbnail`, `over_18`, `name`) " \
                    "VALUES (NULL, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                    (author, title, subred, url, permalink, media, created, thumbnail, over_18, name)
                try:
                    cursor.execute(sql)
                    db.commit()
                except:
                    db.rollback()
        db.close()
        runcount = runcount +1
        print(runcount)
        if runcount >= runs:
            runrep = 0