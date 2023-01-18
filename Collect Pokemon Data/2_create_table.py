import mysql.connector

db = mysql.connector.connect(host="localhost", user="root", password="pwroot", database="pokemon_official_database")

mycursor = db.cursor()
mycursor.execute("CREATE TABLE pokemon_official (id smallint PRIMARY KEY, name varchar(20), height int, weight int, xp int, image_url varchar(100), pokemon_url varchar(100), abilities_1_name varchar(20), abilities_1_bool varchar(5), abilities_2_name varchar(20), abilities_2_bool varchar(5), abilities_3_name varchar(20), abilities_3_bool varchar(5), hp smallint, attack smallint, defence smallint, special_attack smallint, special_defence smallint, speed smallint, type_1 varchar(10), type_2 varchar(10))")
print("Table Created")

mycursor.execute("DESCRIBE pokemon_official")
for i in mycursor:
    print(i)