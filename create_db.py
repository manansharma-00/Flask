import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd = "1234",
    )

my_cursor = mydb.cursor()

my_cursor.execute("CREATE DATABASE our_users")
for db in my_cursor:
    print(db)

