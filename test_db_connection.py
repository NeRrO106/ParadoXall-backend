import pymysql

connection = pymysql.connect(
    host='db-restaurant-test.cr84eusa0dx2.eu-north-1.rds.amazonaws.com',
    user='admin',
    password='andreicosma1234',
    database='restaurant',
    port=3306
)

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT VERSION()")
        result = cursor.fetchone()
        print("Database version:", result[0])
finally:
    connection.close()
