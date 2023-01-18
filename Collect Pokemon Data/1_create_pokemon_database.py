import mysql.connector

db = mysql.connector.connect(host="localhost", user="root", password="pwroot")
mycursor = db.cursor()

mycursor.execute("CREATE DATABASE pokemon_official_database")

print("Database Created")