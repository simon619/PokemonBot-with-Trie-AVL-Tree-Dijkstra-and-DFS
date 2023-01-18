import mysql.connector

db = mysql.connector.connect(host="localhost", user="root", password="pwroot", database="pokemon_official_database")

mycursor = db.cursor()
mycursor.execute("DESCRIBE jessore_distance")
col_name = mycursor.fetchall()

mycursor = db.cursor()

mycursor.execute("SELECT DISTINCT(from_point) FROM jessore_distance")
from_rec = mycursor.fetchall()
print(f"Unique From : {from_rec}")

mycursor.execute("SELECT DISTINCT(to_point) FROM jessore_distance")
to_rec = mycursor.fetchall()
print(f"Unique To : {to_rec}")

mycursor.execute("SELECT * FROM jessore_distance")
record = mycursor.fetchall()
print(record)
for i in range(len(record)):
    print(f"From: {record[i][0]}, To: {record[i][1]}, Distance: {record[i][2]}")

