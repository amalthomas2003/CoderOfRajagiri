import pymysql
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "careerconnect",
    "database": "coder"
}
connection = pymysql.connect(**db_config)
cursor = connection.cursor()
cursor.execute("DROP DATABASE IF EXISTS coder")
connection.commit()
cursor.close()
connection.close()
print("Database successfully Deleted")