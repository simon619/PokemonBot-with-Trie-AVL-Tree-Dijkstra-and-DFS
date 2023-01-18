import mysql.connector
import csv
import json

db = mysql.connector.connect(host="localhost", user="root", password="pwroot", database="pokemon_official_database")

mycursor = db.cursor()
mycursor.execute("CREATE TABLE jessore_distance (from_point varchar(20), to_point varchar(20), distance int)")

mycursor.execute("DESCRIBE jessore_distance")
for i in mycursor:
    print(i)

jessore_data_into_json = []
with open('jessore_distance.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    for line in csv_reader:
        from_val, to_val, dis = line[0].strip(), line[1].strip(), line[2]
        mycursor.execute("INSERT INTO jessore_distance (from_point, to_point, distance) VALUES (%s, %s, %s)", (from_val, to_val, dis))
        db.commit()

        jessore_data_into_json.append({"source": from_val, "destination": to_val, "distance": dis})

print("Inserted Completed")

with open('jessore_distance_data.json', 'w') as file:
    json.dump(jessore_data_into_json, file, indent=2)

mycursor.execute("SELECT DISTINCT(to_point) FROM jessore_distance")
unique_record = mycursor.fetchall()

dic1, dic2 = {}, {}
for i in range(len(unique_record)):
    dic1[i] = unique_record[i][0]
    dic2[unique_record[i][0]] = i

unique_place_list = [dic1, dic2]

with open('area_id_data.json', 'w') as file:
    json.dump(unique_place_list, file, indent=2)

print("JSON Data Created")


