import praw
from fetch_newest import name_id
from prawoauth2 import PrawOAuth2Mini
from secrets import *
from settings import *
from time import time

def runs(db,cursor):
    r = praw.Reddit(user_agent = USER_AGENT)
    oauth_helper = PrawOAuth2Mini(r,app_key = APP_KEY,app_secret = APP_SECRET,
                                    access_token = ACCESS_TOKEN,scopes = SCOPES,
                                    refresh_token = REFRESH_TOKEN)
    oauth_helper.refresh()
    subreddit = r.get_subreddit('all')

    author = "none"
    created = int(time())
    over_18 = 0
    permalink = "none"
    subred = "none"
    thumbnail = "none"
    title = "none"
    url = "none"
    name = "none"
    media = "none"

    lookup = {}

    sql_fetch = "SELECT name from post_info"
    try:
        cursor.execute(sql_fetch)
        result = cursor.fetchall()
        for row in result:
            lookup[row[0]] = None
    except:
        pass

    for post in reversed(list(subreddit.get_new(limit=1000))):
        author = str(vars(post)['author'])
        created = time()
        over_18 = int(vars(post)['over_18'])
        permalink = str(vars(post)['permalink'])
        subred = str(vars(post)['subreddit'])
        thumbnail = str(vars(post)['thumbnail'])
        title = str(vars(post)['title'])
        url = str(vars(post)['url'])
        name = str(vars(post)['name'])
        media = str(vars(post)['media'])
        if name not in lookup:
            sql = "INSERT INTO `post_info` (`ID`, `author`, `title`, `subreddit`, `url`, `permalink`, `media`, `created`, `thumbnail`, `over_18`, `name`) " \
                "VALUES (NULL, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                (author, title, subred, url, permalink, media, created, thumbnail, over_18, name)
            try:
                cursor.execute(sql)
            except:
                db.rollback()
    db.commit()