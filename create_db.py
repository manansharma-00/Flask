import pymysql

host = "localhost"
user = "root"
password = "1234"

mydb = pymysql.connect(
    host=host,
    user=user,
    passwd=password,
)

# Create a cursor
my_cursor = mydb.cursor()

my_cursor.execute("CREATE DATABASE IF NOT EXISTS our_users")

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)
