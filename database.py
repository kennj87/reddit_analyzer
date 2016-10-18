import pymysql

db = pymysql.connect("localhost", "root", "admin", "reddit")
cursor = db.cursor()