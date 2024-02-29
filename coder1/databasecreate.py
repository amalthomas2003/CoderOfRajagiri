
import pymysql

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "careerconnect",
    "database": "mysql"
}


connection = pymysql.connect(**db_config)
cursor = connection.cursor()

new_database_name = "coder"
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {new_database_name}")

db_config["database"]="coder"
connection = pymysql.connect(**db_config)
cursor = connection.cursor()

cursor.execute("""create table if not exists top(
               id int auto_increment primary key,
               top_img MEDIUMBLOB
                )"""
               
               )

cursor.execute("""create table if not exists bottom(
               id int auto_increment primary key,
               bottom_img MEDIUMBLOB
                )"""
               
               )

cursor.execute("""create table if not exists shoes(
               id int auto_increment primary key,
               shoes_img MEDIUMBLOB
                )"""
               
               )



connection.commit()
cursor.close()
connection.close()

print("database created success")