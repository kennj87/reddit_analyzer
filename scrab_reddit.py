import praw
from fetch_newest import name_id
from prawoauth2 import PrawOAuth2Mini
from secrets import *
from settings import *
from time import time
import re

def strincount(string):
    i = 0
    e = 0
    for c in string:
        if c == "/":
            e = e + 1
        i = i + 1
        if (e == 2):
            return i

def fixurl(string):
    s = string
    srev = s[::-1]
    fixed = srev[strincount(srev)::]
    return fixed[::-1]

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
        db.commit()
        for row in result:
            lookup[row[0]] = None
    except:
        pass
    for post in reversed(list(subreddit.get_new(limit=1000))):
        author = str(vars(post)['author'])
        created = time()
        over_18 = int(vars(post)['over_18'])
        permalink = str(vars(post)['permalink'])
        permalinkfix = fixurl(permalink)
        subred = str(vars(post)['subreddit'])
        thumbnail = str(vars(post)['thumbnail'])
        title = str(vars(post)['title'])
        titleformat = db.escape(re.sub('[^a-zA-Z0-9 \n\.]','',title))
        url = str(vars(post)['url'])
        name = str(vars(post)['name'])
        if thumbnail == "self":
            url = fixurl(url)
        if name not in lookup:
            sql_insert = "INSERT INTO `post_info` (`author`, `title`, `subreddit`, `url`, `permalink`,`created`, `thumbnail`, `over_18`, `name`)  VALUES ('%s', %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (author, titleformat, subred, url, permalinkfix, created, thumbnail, over_18, name)
            try:
                cursor.execute(sql_insert)
            except:
                db.rollback()
        db.commit()
