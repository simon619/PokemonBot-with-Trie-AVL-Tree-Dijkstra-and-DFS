import mysql.connector

db = mysql.connector.connect(host="localhost", user="root", password="pwroot", database="pokemon_official_database")

mycursor = db.cursor()
mycursor.execute("DROP TABLE jessore_distance")
print("Table Has Been Deleted")