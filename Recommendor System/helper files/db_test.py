import pymysql
import pandas as pd

hostname = 'your_hostname'
user = 'your_user'
password = 'your_password'

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