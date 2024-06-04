import pymysql
import pandas as pd
hostname = 'sql12.freesqldatabase.com'
user = 'sql12711667'
password = 'vmrGDRbZvm'

db = pymysql.connections.Connection(
    host = hostname,
    user = user,
    password = password,
)

cursor = db.cursor()
cursor.execute('show databases;')
cursor.execute('use sql12711667;')
cursor.execute('desc user_ratings;')

for i in cursor:
    print(i)
db.close()